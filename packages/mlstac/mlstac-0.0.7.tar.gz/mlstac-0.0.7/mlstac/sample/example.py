from datetime import datetime
import numpy as np

from .datamodel import Sample, SampleMetadata, SampleTensor

# Set the ML-STAC sample metadata
sample_metadata = SampleMetadata(
    id=40000,
    geotransform=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    crs="SR-ORG:4326",
    start_datetime=datetime(2021, 1, 1, 0, 0, 0),
    end_datetime=None,
    extra={"dd":"dd"}
)

# Set the ML-STAC sample tensors
sample_tensors = SampleTensor(
    input=np.array([1, 2, 3]), target=np.array([1, 2, 3]), extra=None
)

# Set the ML-STAC item
sample = Sample(metadata=sample_metadata, tensor=sample_tensors)
sample.save(path="/home/gonzalo/")
sample.checksum()

# Write the squema
with open("mlstac/sample/squema.json", "w") as f:
    f.write(sample.model_schema_json(indent=2))
