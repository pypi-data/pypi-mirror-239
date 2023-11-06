from .datamodel import Catalog

# Create an ML-STAC Catalog
ml_catalog = Catalog(name="train", n_items=100)

# Create JSON Schema
# import json
# with open('mlstac-spec/catalog-spec/squema.json', 'w') as f:
#     json.dump(ml_catalog.model_json_schema(), f, indent=4)
