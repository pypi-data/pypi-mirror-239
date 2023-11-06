from mlstac.sample.datamodel import Sample, SampleMetadata, SampleTensor
from mlstac.collection.datamodel import Collection, Provider, Providers, Split
from mlstac.api.main import load, download
from mlstac.api.datasets import LocalDataset, StreamDataset

from mlstac.api.nest_asyncio import apply as nest_asyncio_apply


# Patch asyncio to make its event loop reentrant.
nest_asyncio_apply()


# Huggingface utils
def hf_getlink(repoinfo, split="train"):
    return f'{str(repoinfo)}/resolve/main/{split}/'