import hashlib
import json
import os

import requests


def checksum(file_path):
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            md5_hash.update(data)

    return md5_hash.hexdigest()


def filesize(file_path):
    file_size = os.path.getsize(file_path)
    return file_size


def download_url(url, target, headers):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(target, "wb") as file:
            for chunk in response.iter_content(
                    chunk_size=8192):
                if chunk:
                    file.write(chunk)
        response.close()
    else:
        server_err = json.loads(response.content.decode('utf-8'))
        reason = server_err.get('reason', '')
        e = ValueError(f"Failed to download the file. Status code: {response.status_code}, reason: {reason}")
        response.close()
        raise e
