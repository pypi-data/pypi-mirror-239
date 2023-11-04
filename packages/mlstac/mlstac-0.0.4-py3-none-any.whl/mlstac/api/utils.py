import asyncio
import gzip
import pathlib
import urllib

import aiohttp
import tqdm
from tqdm.asyncio import tqdm_asyncio

BASE_ALPH = tuple("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)


def urljoin(*args: str) -> str:
    """Safely join URLs.

    Returns:
        str: The joined URL.
    """
    return "/".join(map(lambda x: str(x).rstrip("/"), args))


def base61_decode(string: str) -> int:
    """ Decode a base61 string.

    Args:
        string (str): The string to decode.

    Returns:
        str: The decoded string.
    """
    num = 0
    for char in string:
        num = num * BASE_LEN + BASE_DICT[char]
    return num


def base61_encode(num: int) -> str:
    """ Encode a number in base61.

    Args:
        num (int): The number to encode.

    Returns:
        str: The encoded string.
    """

    if not num:
        return BASE_ALPH[0]

    encoding = ""
    while num:
        num, rem = divmod(num, BASE_LEN)
        encoding = BASE_ALPH[rem] + encoding
    return encoding


def get_file_size(filename: str) -> float:
    """ This function returns the size of a file in MB
    
    Args:
        filename (str): The path to the file

    Returns:
        float: The size of the file in MB
    """
    mbhr = pathlib.Path(filename).stat().st_size / (1024 ** 2)
    return round(mbhr, 4)


async def download_file(url: str) -> bytes:
    """ Download a file from a URL.

    Args:
        url (str): The URL to download from.
    
    Returns:
        bytes: The content of the file.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            return content


async def write_to_file(content: bytes, filename: pathlib.Path) -> None:
    """ Download a file from a URL.

    Args:
        content (bytes): The content to write.
        filename (pathlib.Path): The filename to save to.
    """
    with open(filename, "wb") as outfile:
        outfile.write(content)


async def extract_file(in_filename: pathlib.Path, out_filename: pathlib.Path) -> int:
    """ Extract a file from a gzip archive.

    Args:
        in_filename (pathlib.Path): The zipped filename.
        out_filename (pathlib.Path): The unzipped filename.
    
    Returns:
        int: The number of bytes extracted.
    """
    sum_bytes = 0
    with gzip.open(in_filename, "rb") as infile:
        with open(out_filename, "wb") as outfile:
            for line in infile:
                outfile.write(line)
                sum_bytes += len(line)

    # Remove the .zip file
    in_filename.unlink()

    return sum_bytes


async def download_and_extract_task(url: str, out_filename: pathlib.Path) -> None:
    """ Create a task to download and extract a file.

    Args:
        url (str): The URL to download from.
        out_filename (pathlib.Path): The filename to save to.
    """

    content = await download_file(url)

    # get the name
    gzip_name = out_filename.parent / pathlib.Path(url).name
    await write_to_file(content, gzip_name)
    await extract_file(gzip_name, out_filename)


async def _download_and_extract(
    url: str, nfiles: int, out_dir: pathlib.Path, bar_msg: str
) -> None:
    """ Create a list of tasks to download and extract a file.

    Args:
        url (str): The URL to download from.
        nfiles (int): The number of files to download.
        out_dir (pathlib.Path): The directory to save the files to.
    """

    # Get the file names
    tasks = []
    for index in range(nfiles):
        file_snippet = base61_encode(index).zfill(7)
        filename = out_dir / ("%s.safetensors" % file_snippet)

        # merge the url and the filename
        url_filename = urljoin(url, "%s.safetensors.gz" % file_snippet)

        # download the file
        tasks.append(download_and_extract_task(url_filename, filename))

    _ = await tqdm_asyncio.gather(*tasks, desc=bar_msg)


def download_and_extract(
    url: str, n_items: int, out_dir: pathlib.Path, bar_msg: str = "Downloading Files"
) -> None:
    """ Download and extract a file."""
    asyncio.run(_download_and_extract(url, n_items, out_dir, bar_msg))


def download_split(
    ml_collection: dict, path: pathlib.Path, split: str = "train", force: bool = False
) -> None:
    """ Download a set of files. """
    catalog = ml_collection["ml:%s" % split].copy()

    if not force:
        counter = 0
        for _ in (path / split).glob("*.safetensors"):
            counter += 1

        # If the number of files is equal to the number of items
        if counter == catalog["n_items"]:
            return None

    # Add the output directory and the bar message parameters
    catalog.update({"out_dir": path / split, "bar_msg": "%s dataset" % split})

    # Download the files
    download_and_extract(**catalog)

    return None


def simple_download_extract(url_file: str, filename: pathlib.Path) -> None:
    """ Download a file from a URL.

    Args:
        url (str): The URL to download from.
        filename (pathlib.Path): The filename to save to.
    """
    filename2 = filename.parent / ("%s.gz" % filename.stem)

    # if the file exists remove it
    if filename.exists():
        filename.unlink()

    if filename2.exists():
        filename2.unlink()

    # batch download the file
    with urllib.request.urlopen(url_file) as r:
        for chunk in iter(lambda: r.read(4096), b""):
            with open(filename2, "ab") as f:
                f.write(chunk)

    # Extract the file
    with gzip.open(filename2, "rb") as infile:
        with open(filename, "wb") as outfile:
            for line in infile:
                outfile.write(line)

    return None
