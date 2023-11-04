import json
import pathlib
import urllib
from tempfile import NamedTemporaryFile
from typing import Union

from mlstac.api.datasets import LocalDataset, StreamDataset
from mlstac.api.utils import download_split


def load_secret(secret: Union[str, pathlib.Path, dict]) -> dict:
    """ Load a secret from a URL or a local file."""
    if isinstance(secret, str):
        if pathlib.Path(secret).exists():
            with open(secret, "r") as f:
                ml_collection = json.load(f)
        else:
            with urllib.request.urlopen(secret) as response:
                binary_data = response.read()
                ml_collection = json.loads(binary_data.decode("utf-8"))
    elif isinstance(secret, dict):
        ml_collection = secret
    else:
        raise ValueError("The secret must be a URL, a local file or a dictionary.")

    return ml_collection


def download(
    secret: Union[str, pathlib.Path, dict],
    path: Union[str, pathlib.Path],
    split: Union[str, None] = None,
    verbose: bool = True,
):
    """ Download a dataset that follows the ML-STAC specification.

    Args:
        secret (Union[str, dict]): An URI or a local path to a JSON 
        file or a dictionary that implements the ML-STAC Collection
        specification.
        path (Union[str, pathlib.Path]): The path where the dataset
        will be saved.
        split (str, optional): The split of the dataset to download.
        If None, the entire dataset will be downloaded. 
        Defaults to None.
    """
    # Check inputs
    if split == "val":
        split = "validation"

    if isinstance(path, str):
        path = pathlib.Path(path)

    ml_collection = load_secret(secret)
    if verbose:
        print("Downloading %s" % ml_collection["id"])

    # Download the dataset
    if split is None:
        _f = ("train", "test", "validation")
        [(path / x).mkdir(parents=True, exist_ok=True) for x in _f]
        for lf in _f:
            download_split(ml_collection, path, lf)
    elif split in ("validation", "train", "test"):
        (path / split).mkdir(parents=True, exist_ok=True)
        download_split(ml_collection, path, split)

    return path


def default_data_dir() -> pathlib.Path:
    """ Get the default data directory."""
    root = pathlib.Path.home() / ".mlstac/datasets/"
    root.mkdir(parents=True, exist_ok=True)

    return root


def load(
    secret: Union[str, pathlib.Path, dict],
    stream: bool = False,
    data_dir: Union[str, pathlib.Path] = None,
    split: Union[str, None] = "train",
    framework: str = "torch",
    device: str = "cpu",
    verbose: bool = True,
):

    if not stream:
        if data_dir is None:
            data_dir = default_data_dir()
        elif isinstance(data_dir, str):
            data_dir = pathlib.Path(data_dir)

        download(secret, data_dir, split, verbose)

        return LocalDataset(path=data_dir / split, framework=framework, device=device)

    else:
        ml_collection = load_secret(secret)

        # create a alway empty temporary file
        tempobj = NamedTemporaryFile(suffix=".safetensors")
        tempfile = pathlib.Path(tempobj.name)

        # obtain the url
        url = ml_collection["ml:%s" % split]["url"]
        if verbose:
            print("Connecting to %s" % ml_collection["id"])

        return StreamDataset(
            tempfile=tempfile, url=url, framework=framework, device=device
        )
