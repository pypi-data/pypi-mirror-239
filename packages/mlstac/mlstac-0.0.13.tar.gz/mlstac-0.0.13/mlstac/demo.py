import pathlib
import mlstac
import numpy as np

secret = "https://huggingface.co/datasets/jfloresf/burn-cems-1/resolve/main/main.json"
train_db = mlstac.load(
    secret=secret,
    framework="numpy",
    stream=False,
    device="cpu",
    data_dir=pathlib.Path("/home/gonzalo/deno")
)


batch = train_db[0]
input = batch["input"]
target = batch["target"]
extra = batch["extra"]

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3)
ax[0].imshow(np.moveaxis(input[[3, 2, 1], :, :], 0, -1)*3)
ax[1].imshow(target[0, :, :])
ax[2].imshow(np.moveaxis(input[[3, 2, 1], :, :], 0, -1)*3)
plt.show()

import time
from tqdm import tqdm
with tqdm(total=100) as pbar:
    for i in range(10):
        time.sleep(0.1)
        pbar.update(10)
pbar.close()


aaa = dict(ml_aa=10, ml_b=20)
aaa = {k.replace("ml_", "ml:"): v for k, v in aaa.items()}

# to pypi
!python setup.py sdist bdist_wheel
!twine upload dist/*



import json
with open('curated/main.json', 'w') as f:
    json_file = ml_catalog.model_dump()
    json_file = {k.replace("ml_", "ml:"): v for k, v in json_file.items()}
    json_file = {k: json_file[k] for k in sorted(json_file, key=lambda x: (not x.startswith("ml:"), x))}

# Sort keys to make it more readable first stac keys, then ml keys
# the ml keys have the suffix ml: to avoid conflicts with stac keys


 