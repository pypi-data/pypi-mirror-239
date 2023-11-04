import re
from datetime import datetime
from typing import Dict, List, Literal, Optional

import pydantic

from ..catalog.datamodel import Catalog

__split_strategy__ = Literal[
    "random sampling",
    "spatial stratified random sampling",
    "spatiotemporal stratified random sampling",
    "other",
]
__cvtask__ = Literal[
    "multi-class classification",
    "binary classification",
    "object detection",
    "multi-class semantic segmentation",
    "binary semantic segmentation",
    "instance segmentation",
    "image to image",
    "multi-image to image",
    "image to multi-image",
    "multi-image to multi-image",
    "regression",
    "multi-task",
    "other",
]

__bands__ = Literal[
    "aerosol",
    "blue",
    "green1",
    "green",
    "yellow",
    "red",
    "rededge1",
    "rededge2",
    "rededge3",
    "nir",
    "nir2",
    "watervapor",
    "cirrus",
    "swir1",
    "swir2",
    "thermal1",
    "thermal2",
    "hv",
    "hh",
    "vv",
    "vh",
    "sar-derived",
    "dem",
    "dem-derived",
    "landcover",
    "landcover-derived",
    "other",
]

__sensor__ = Literal[
    "sentinel-2 msi",
    "landsat-8 oli/tirs",
    "landsat-8 oli",
    "landsat-8 tirs",
    "landsat-7 etm+",
    "landsat-7 etm+ only slc-off",
    "landsat-5 tm",
    "landsat-4 tm",
    "landsat-1 to 5 mss",
    "modis",
    "modis-derived",
    "sentinel-1 sar",
    "aerial",
    "uav",
    "aster",
    "hyperion",
    "cbers",
    "planetscope",
    "rapideye",
    "spot 1 to 5",
    "spot 6/7",
    "ikonos",
    "worldview-2",
    "worldview-3",
    "other",
]

__dtype__ = Literal[
    "bool", "uint8", "int8", "uint16", "int16", "int32", "float16", "float32", "float64"
]


class HyperLink(pydantic.BaseModel):
    link: str

    @pydantic.field_validator("link")
    @classmethod
    def check_link(cls, v):
        if not re.match(r"^https?://", v):
            raise ValueError("link must be a valid URL")
        return v


class Reviewer(pydantic.BaseModel):
    name: str
    orcid: Optional[str] = None
    score: Literal[0, 1, 2, 3, 4, 5]
    issue_link: HyperLink

    @pydantic.field_validator("orcid")
    @classmethod
    def check_orcid(cls, v):
        if v is not None:
            if not re.match(r"^https://orcid.org/", v):
                raise ValueError("orcid must be a valid URL")
        return v

    @pydantic.field_validator("score")
    @classmethod
    def check_score(cls, v):
        if v not in [0, 1, 2, 3, 4, 5]:
            msg = "%s%s%s" % (
                "score must be a integer between 0 and 5",
                " (0: very poor, 1: poor, 2: fair, 3: good)",
                " 4: very good, 5: excellent)",
            )
            raise ValueError(msg)
        return v


class Reviewers(pydantic.BaseModel):
    reviewers: Optional[List[Reviewer]] = None


class License(pydantic.BaseModel):
    name: str
    link: HyperLink


class Licenses(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")
    licenses: List[License]
    additional_comments: Optional[str] = None

    @pydantic.field_validator("licenses")
    @classmethod
    def check_licenses(cls, v):
        if len(v) == 0:
            raise ValueError("licenses must be a list with at least one element")
        return v


class SpatialExtent(pydantic.BaseModel):
    bbox: List[float]

    @pydantic.field_validator("bbox")
    @classmethod
    def check_bbox(cls, v):
        if len(v) != 4:
            msg = "%s%s" % (
                "bbox must be a list with 4 ",
                "elements: [minx, miny, maxx, maxy]",
            )
            raise ValueError(msg)
        return v


class TemporalExtent(pydantic.BaseModel):
    interval: List[datetime]

    @pydantic.field_validator("interval")
    @classmethod
    def check_interval(cls, v):
        if len(v) != 2:
            msg = "%s%s" % (
                "interval must be a list with 2 ",
                "elements: [start_datetime, end_datetime]",
            )
            raise ValueError(msg)

        if v[0] >= v[1]:
            raise ValueError("end_datetime must be after start_datetime")

        return v


class Extent(pydantic.BaseModel):
    spatial: SpatialExtent
    temporal: TemporalExtent


class Author(pydantic.BaseModel):
    name: str
    orcid: Optional[str] = None
    organization: Optional[str] = None

    @pydantic.field_validator("orcid")
    @classmethod
    def check_orcid(cls, v):
        if v is not None:
            if not re.match(r"^https://orcid.org/", v):
                raise ValueError("orcid must be a valid URL")
        return v


class Authors(pydantic.BaseModel):
    authors: List[Author]
    additional_comments: Optional[str] = None
    curated_by: HyperLink
    reference: HyperLink


class Collection(pydantic.BaseModel):
    """ML-STAC Catalog dataclass."""

    model_config = pydantic.ConfigDict(extra="allow")

    # General information
    mlstac_version: str
    name: str
    train: Catalog
    val: Catalog
    test: Catalog

    # Additional information
    authors: Authors
    licenses: Licenses
    split_strategy: __split_strategy__
    cv_task: __cvtask__
    sensor: __sensor__
    bands: List[__bands__]
    review: Reviewers
    extent: Extent
    dtype_input: __dtype__
    dtype_target: __dtype__
    dtype_reference: __dtype__
    size: int
    keywords: List[str]
    description: str
    extra: Dict[str, str]
    issue_link: HyperLink

    @pydantic.field_validator("mlstac_version")
    @classmethod
    def check_mlstac_version(cls, v):
        regex_exp = re.compile(r"^[0-9]+.[0-9]+.[0-9]+$")
        if not regex_exp.match(v):
            msg = "%s%s" % (
                "mlstac_version must be from the ",
                "form <major>.<minor>.<patch>",
            )
            raise ValueError(msg)

    @pydantic.field_validator("name")
    @classmethod
    def check_name(cls, v):
        regex_exp = re.compile(r"^[a-zA-Z0-9]+$")
        if not regex_exp.match(v):
            raise ValueError("name must be a string with only letters and numbers")
        return v

    @pydantic.field_validator("split_strategy")
    @classmethod
    def check_split_strategy(cls, v):
        if v not in __split_strategy__.__args__:
            raise ValueError("split_strategy is not valid.")
        return v

    @pydantic.field_validator("cv_task")
    @classmethod
    def check_cv_task(cls, v):
        if v not in __cvtask__.__args__:
            raise ValueError("cv_task is not valid.")
        return v

    @pydantic.field_validator("sensor")
    @classmethod
    def check_sensor(cls, v):
        if v not in __sensor__.__args__:
            raise ValueError("sensor is not valid.")
        return v

    @pydantic.field_validator("bands")
    @classmethod
    def check_bands(cls, v):
        for band in v:
            if band not in __bands__.__args__:
                raise ValueError("bands is not valid.")
        return v

    @pydantic.field_validator("dtype_input", "dtype_target", "dtype_reference")
    @classmethod
    def check_dtype_input(cls, v):
        if v not in __dtype__.__args__:
            raise ValueError("dtype_input is not valid.")
        return v

    @pydantic.field_validator("keywords")
    @classmethod
    def check_keywords(cls, v):
        if len(v) == 0:
            raise ValueError("keywords must be a list with at least one element")
        return v

    @pydantic.field_validator("extra")
    @classmethod
    def check_extra(cls, v):
        # only integers, floats and strings bool are allowed
        to_eval = (int, float, str, bool)
        condition = all(isinstance(x, to_eval) for x in v.values())
        if not condition:
            raise ValueError("extra values must be integers, floats, strings or bools.")
