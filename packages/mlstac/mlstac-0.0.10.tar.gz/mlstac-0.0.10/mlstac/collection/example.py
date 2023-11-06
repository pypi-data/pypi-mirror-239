from datetime import datetime

from ..catalog.dataclass import Catalog
from .dataclass import (Author, Authors, Collection, Extent, HyperLink,
                        License, Licenses, Reviewer, Reviewers, SpatialExtent,
                        TemporalExtent)


ml_catalog = Collection(    
    title = "CloudSEN12",
    description = "Cloud detection",
    license = "CC-BY-4.0",
    path = "/home/gonzalo/",
    providers = Providers(
        providers = [
            Provider(name="Javier", roles=["author"], url="www.google.com")
        ]
    ),
    links = "www.google.com",
    ml_train = Split(n_items=100, link="www.google.com"),
    ml_val = Split(n_items=100, link="www.google.com"),
    ml_test = Split(n_items=100, link="www.google.com"),
    ml_task = "TensorToTensor"
)

ml_catalog.id

ml_catalog.add_curator(
    name="Javier",
    url="www.google.com",
)

ml_catalog.add_labels(
    labels={"cloud": 1, "no-cloud": 0}
)


ml_catalog.add_reviewer(
    name="Javier",
    score=2,
    url="https://google.com/"
)

ml_catalog.add_dimensions(
    W = {"axis": 0, "description": "width"},
    H = {"axis": 1, "description": "height"},
    C = {"axis": 2, "description": "channels"},
    T = {"axis": 3, "description": "time"}            
)

ml_catalog.add_spectral_information(
    bands = {
        "red": {
            "description": "Red band",
            "index": 0,            
        },
        "vv": {
            "description": "Single co-polarization, vertical transmit/vertical receive",
            "unit": "dB",
            "wavelengths": [0.056, 0.056],
            "index": 1
        }
    },
    sensor = "sentinel-2",
    axis = 3    
)

ml_catalog.add_raw_data_url(
    url = "https://google.com/"
)

ml_catalog.add_discussion_url(
    url = "https://google.com/"
)

ml_catalog.add_split_strategy(
    split_strategy = "random"
)


# Create JSON Schema
# import json
# with open('mlstac-spec/collection/squema.json', 'w') as f:
#     json.dump(ml_catalog.model_json_schema(), f, indent=4)


# save collection
import json
with open('mlstac-spec/collection/example.json', 'w') as f:
    json.dump(ml_catalog.model_dump(), f, indent=4)