from mlstac.sample.datamodel import Sample, SampleMetadata, SampleTensor
from mlstac.catalog.datamodel import Catalog
from mlstac.collection.datamodel import (
    Author,
    Authors,
    Collection,
    Extent,
    HyperLink,
    License,
    Licenses,
    Reviewer,
    Reviewers,
    SpatialExtent,
    TemporalExtent,
)
from mlstac.api.main import load, download
from mlstac.api.datasets import LocalDataset, StreamDataset

from mlstac.api.nest_asyncio import apply as nest_asyncio_apply

# Patch asyncio to make its event loop reentrant.
nest_asyncio_apply()
