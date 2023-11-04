from datetime import datetime

from ..catalog.dataclass import Catalog
from .dataclass import (Author, Authors, Collection, Extent, HyperLink,
                        License, Licenses, Reviewer, Reviewers, SpatialExtent,
                        TemporalExtent)

# Create an ML-STAC Catalog
ml_catalog = Collection(
    mlstac_version="0.1.0",
    name="cloudsen12",
    train=Catalog(name="train", n_items=100),
    val=Catalog(name="val", n_items=20),
    test=Catalog(name="test", n_items=20),
    authors=Authors(
        authors=[
            Author(
                name="Javier",
                orcid="https://orcid.org/0000-0001-0000-0000",
                organization="UPM",
            ),
            Author(
                name="Luis",
                orcid="https://orcid.org/0000-0002-0000-0000",
                organization="UPM",
            ),
            Author(
                name="Lola",
                orcid="https://orcid.org/0000-0003-0000-0000",
                organization="IPL",
            ),
        ],
        additional_comments=(
            "The authors agree to publish the dataset under "
            + "the ML-STAC specification."
        ),
        curated_by=HyperLink(link="https://github.com/csaybar"),
        reference=HyperLink(link="https://cloudsen12.github.io/"),
    ),
    licenses=Licenses(
        licenses=[
            License(
                name="CC-BY-4.0",
                link=HyperLink(link="https://creativecommons.org/licenses/by/4.0/"),
            )
        ],
        additional_comments=(
            "The authors agree to change the license from CC-BY-4.0 "
            + "to CC-BY-SA-4.0."
        ),
    ),
    split_strategy="spatial stratified random sampling",
    cv_task="multi-class semantic segmentation",
    sensor="sentinel-2 msi",
    bands=[
        "aerosol",
        "blue",
        "green",
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
    ],
    review=Reviewers(
        reviewers=[
            Reviewer(
                name="Javier",
                orcid="https://orcid.org/0000-0001-0000-0000",
                score=2,
                comments="The dataset is not good",
                issue_link=HyperLink(link="https://github.com/r-spatial/rgee/issues/1"),
            )
        ]
    ),
    extent=Extent(
        spatial=SpatialExtent(bbox=[-180, -90, 180, 90]),
        temporal=TemporalExtent(interval=[datetime(2019, 1, 1), datetime(2020, 1, 1)]),
    ),
    dtype_input="uint16",
    dtype_target="uint8",
    dtype_reference="uint8",
    size=100,
    keywords=["cloud-detection", "cloud-segmentation"],
    description=(
        "CloudSEN12 is a LARGE dataset (~1 TB) for cloud semantic "
        + "understanding that consists of 49,400 image patches (IP) "
        + "that  are evenly spread throughout all continents except "
        + "Antarctica. Each IP covers 5090 x 5090 meters and "
        + "contains data from Sentinel-2 levels 1C and 2A, hand-crafted "
        + "annotations of thick and thin clouds and cloud shadows, "
        + "Sentinel-1 Synthetic Aperture Radar (SAR), digital "
        + "elevation model, surface water occurrence, land cover "
        + "classes, and cloud mask results from six cutting-edge "
        + "cloud detection algorithms."
    ),
    extra={"github": "https://github.com/cloudsen12", "dummy": "dummy"},
    issue_link=HyperLink(link="https://github.com/r-spatial/rgee/issues/2"),
)

# Create JSON Schema
# import json
# with open('mlstac-spec/collection/squema.json', 'w') as f:
#     json.dump(ml_catalog.model_json_schema(), f, indent=4)
