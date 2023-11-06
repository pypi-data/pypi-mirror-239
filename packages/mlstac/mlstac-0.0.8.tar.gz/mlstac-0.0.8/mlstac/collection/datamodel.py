import re
from datetime import datetime
from typing import Dict, List, Literal, Optional, Union

import pathlib
import pydantic
import requests

class HyperLink(pydantic.BaseModel):
    url: str

    @pydantic.field_validator("url")
    @classmethod
    def check_link(cls, v):
        regex_exp = re.compile(r"^(https?|ftp)://\S+|www\.\S+")
        if not regex_exp.match(v):
            raise ValueError("link must be a valid URL")
        
        # most be a public url and return 200        
        r = requests.get(v)
        if r.status_code != 200:
            raise ValueError("link must be a valid URL")
                
        return v

class Provider(pydantic.BaseModel):
    name: str
    description: Optional[str] = None
    roles: Optional[List[str]] = None
    url: Optional[str] = None

class Providers(pydantic.BaseModel):
    providers: List[Provider]

class Labels(pydantic.BaseModel):
    labels: Dict[str, int]

class Reviewer(pydantic.BaseModel):
    name: str
    score: Literal[0, 1, 2, 3, 4, 5]
    url: str
    
    @pydantic.field_validator("url")
    def check_url(cls, v):
        HyperLink(url=v)
        return v
    
class Reviewers(pydantic.BaseModel):
    reviewers: Optional[List[Reviewer]] = None

class Dimension(pydantic.BaseModel):
    axis: int
    description: Optional[str]
    
class Dimensions(pydantic.BaseModel):
    dimensions: Dict[str, Dimension]
    dtype: Optional[str] = None
    shape: Optional[List[int]] = None
    offsets: Optional[List[int]] = None

class SpectralBand(pydantic.BaseModel):
    band: str
    
    @pydantic.field_validator("band")
    def check_band(cls, v):
                
        bands = (
            "aerosol", "blue", "green1", "green", "yellow", "red",
            "rededge1", "rededge2", "rededge3", "nir", "nir2",
            "watervapor", "swir1", "swir2", "thermal", "thermal1",
            "thermal2", "cirrus"
        )
        
        if v not in bands:
            return {
                "standard": None,
                "description": None,
                "unit": None,
                "wavelengths": [None, None],
                "index": None
            }
        
        standard = (
                "A", "B", "G1", "G", "Y", "R", "RE1", "RE2", "RE3", "N", "N2",
                "WV", "S1", "S2", "T", "T1", "T2", "C"            
        )
        
        wavelengths = (
            (400, 455), (450, 530), (510, 550), (510, 600), (585, 625),
            (620, 690), (695, 715), (730, 750), (765, 795), (760, 900),
            (850, 880), (935, 960), (1550, 1750), (2080, 2350),
            (10400, 12500), (10600, 11190), (11500, 12510), (13600, 13800)
        )
            
        index = [index for index, x in enumerate(bands) if (v == x)][0]
            
        return {
            "standard": standard[index],
            "description": None,
            "wavelengths": wavelengths[index],
            "unit": "nm",
            "index": None
        }

class Spectral(pydantic.BaseModel):
    bands: Dict[str, SpectralBand]
    axis: Optional[int] = None
    sensor: Optional[str] = None

class SplitStrategy(pydantic.BaseModel):
    name: Literal["random", "stratified", "systematic", "other"]

class Split(pydantic.BaseModel):
    """ML-STAC Catalog dataclass."""
    n_items: int
    link: str

    @pydantic.field_validator("n_items")
    def n_items_must_be_valid(cls, value: int) -> int:
        """n_items must be positive"""
        # must be positive
        if value <= 0:
            raise ValueError("n_items must be positive")
        return value


class Collection(pydantic.BaseModel):
    
    stac_version: str = '1.0.0'
    mlstac_version: str = '0.1.0'
        
    # Required fields -------------------------------
    title: str
    description: str
    license: str
    providers: Providers
    path: Union[str, pathlib.Path]
    
    ml_train: Split
    ml_val: Split
    ml_test: Split    
    ml_task: Literal[
        "TensorClassification", "TensorRegression",
        "TensorSegmentation", "ObjectDetection",
        "TensorToTensor", "TensorToText",
        "TextToTensor"
    ]
    
    # Opt fields ------------------------------------
    links: Optional[str] =  "localhost"
    keywords: Optional[List[str]] = None
    ml_labels: Optional[Labels] = None
    ml_curator: Optional[Provider] = None    
    ml_reviewers: Optional[Reviewers] = Reviewers(reviewers=[])
    ml_dimensions: Optional[dict] = None
    ml_spectral_bands: Optional[Spectral] = None
    ml_split_strategy: Optional[str] = None
    ml_raw_data_url: Optional[str] = None
    ml_discussion_url: Optional[str] = None
    
    # Automatic fields ------------------------------------
    extent: Optional[dict] = None
    ml_datacube: Optional[dict] = None
    size: Optional[int] = None
    metadata_train: Optional[str] = None
    metadata_test: Optional[str] = None
    metadata_val: Optional[str] = None
    
    
    def add_curator(
        self, 
        name: str,
        description: Optional[str] = None,
        roles: Optional[List[str]] = None,
        url:Optional[str] = None,
    ):
        self.ml_curator = Provider(
            name=name,
            description=description,
            roles=roles,
            url=HyperLink(url=url).url
        )       
        print("Curator added to self.ml_curator") 
        return None
        

    def add_labels(self, labels: Dict[str, int]) -> None:
        self.ml_labels = Labels(labels=labels)        
        print("Labels added to self.ml_labels")        
        return None

    def add_reviewer(
        self, 
        name: str,
        score: Literal[0, 1, 2, 3, 4, 5],
        url: str
    ):
        dataset_review = self.ml_reviewers.model_dump()["reviewers"]
        new_review = Reviewer(
            name=name,
            score=score,
            url=url
        ).model_dump()
        dataset_review.append(new_review)
        
        # remove duplicates
        dataset_review = [dict(t) for t in {tuple(d.items()) for d in dataset_review}]
        
        self.ml_reviewers = Reviewers(reviewers=dataset_review)
        
        print("Reviewer added to self.ml_reviewers")
        
        return None

    def add_dimensions(self, **kwargs: dict):
        dimensions = dict()
        for key, value in kwargs.items():
            dimensions[key] = Dimension(**value).model_dump()
        
        self.ml_dimensions = Dimensions(dimensions=dimensions)
        
        print("Dimensions added to self.ml_dimensions")
        
        return None

    def add_spectral_information(
        self,
        bands: Optional[Dict[str, dict]],
        axis: Optional[int],
        sensor: Optional[str]
    ):        
        spectral_bands = dict()
        for band, value  in bands.items():
            
            # Get extra information if band is in the awesome-spectral-indices
            band_info = SpectralBand(band=band)
            
            # Add extra information
            for key, value in value.items():
                band_info.band[key] = value
                
            spectral_bands[band] = band_info
            
        self.ml_spectral_bands = Spectral(
            bands=spectral_bands,
            axis=axis,
            sensor=sensor
        )
        
        print("Specral information added to self.ml_spectral_bands")
        return None

    def add_raw_data_url(self, url: str):
        self.ml_raw_data_url = HyperLink(url=url).url
        print("Raw information added to self.ml_raw_data_url")
        return None

    def add_discussion_url(self, url: str):
        self.ml_discussion_url = HyperLink(url=url).url
        print("Discussion added to self.ml_discuss_url")
        return None
    
    def add_split_strategy(self, split_strategy: str):
        self.ml_split_strategy = SplitStrategy(name=split_strategy).name
        print("Split added to self.ml_split")
        return None
