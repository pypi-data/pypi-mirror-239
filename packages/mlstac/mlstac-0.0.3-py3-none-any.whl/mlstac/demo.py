import pathlib

import mlstac

secret = "https://huggingface.co/datasets/jfloresf/burn-cems-1/resolve/main/main.json"
train_db = mlstac.load(
    secret=secret,
    framework="torch",
    stream=True,
    device="cpu",
    data_dir=pathlib.Path("/home/gonzalo/deno"),
)
