import os
import pathlib
import requests
import logging
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from .sha import calculate_sha1_hash_base64
from dataclasses import dataclass
from typing import Dict, Any
from typing_extensions import Optional
from ..Request import _Request

logger = logging.getLogger(__name__)


@dataclass
class ParamsArgs:
    sha1hash: str
    file_name: str


@dataclass
class FileDownloadResponse:
    sha1_hash: Optional[str]
    file_size: int
    presigned_endpoint_response: Any


DOWNLOAD_CHUNK_SIZE = 1024 * 1024  # 1MB


class FileDownloader:
    def __init__(self, request: _Request):
        self.request = request

    def download_file(
        self,
        file_path: str,
        presigned_endpoint_url: str,
        params: Dict[str, Any],
        request_method: str = "GET",
    ):
        res = self.request._make_request(
            request_method, presigned_endpoint_url, params=params
        )
        if not res:
            raise Exception(
                f"No response for {presigned_endpoint_url} with params {params}"
            )
        download_url = res["url"]

        r = requests.get(download_url, stream=True)
        if not r.ok:
            logger.error(f"Failed to download from {download_url}. Error: {r.text}")
            raise Exception(f"Failed to download from {download_url}")
        r.raise_for_status()

        directory = os.path.dirname(file_path)
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_size = 0

        if r.headers.get("content-length") is not None:
            file_size = int(r.headers.get("content-length", 0))
            with tqdm(
                total=file_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as t:
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                        t.update(len(chunk))
                        f.write(chunk)
        else:
            # Show a spinner if no content-length header is provided
            with tqdm(
                total=None,  # Set total to None for an infinite spinner
                desc="Downloading",  # Description for the spinner
                bar_format="{desc}: {spinner} ",  # Custom format for spinner
                spinner="aesthetic",  # Spinner style (can be changed as per preference)
            ) as t:
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                        file_size += len(chunk)
                        f.write(chunk)
                        t.update()  # This will just keep the spinner spinning

        sha1_hash = None
        if "sha1Checksum" in res:
            with open(file_path, "rb") as f:
                sha1_hash, _ = calculate_sha1_hash_base64(f)
            if sha1_hash != res["sha1Checksum"]:
                raise Exception(
                    f"Checksum mismatch for {file_path} and {download_url}\nExpected: {res['sha1Checksum']}, Actual: {sha1_hash}"
                )
        else:
            logger.warn(f"Checksum not found for {file_path} and {download_url}")

        return FileDownloadResponse(
            sha1_hash=sha1_hash,
            file_size=file_size,
            presigned_endpoint_response=res,
        )
