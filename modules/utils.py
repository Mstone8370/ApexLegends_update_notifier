import json
import os

from modules import models

from google.cloud import storage
from google.api_core import exceptions

def save_dict_as_json(dict, path):
    """
    dict를 json 파일로 저장.
    """
    with open(path, mode="wt", encoding="utf-8") as file:
        json.dump(dict, file, ensure_ascii=False, indent=2, default=models.json_default)


def save_dict_as_json_to_GCS(dict, bucket_name:str, blob_name:str):
    """
    dict를 json 파일로 구글 클라우드 스토리지에 저장.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        json_data = json.dumps(dict, ensure_ascii=False, indent=2, default=models.json_default)
        blob.upload_from_string(json_data, content_type="application/json")
    except Exception as e:
        raise e


def load_json_as_dict(path):
    """
    path의 json 파일을 읽어서 dict로 반환.
    """
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            return json.load(file)
    except:  # noqa: E722
        return {}


def load_json_as_dict_from_GCS(bucket_name:str, blob_name:str):
    """
    구글 클라우드 스토리지에서 json 파일을 읽어서 dict로 반환.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        file_contents = blob.download_as_string()
        return json.loads(file_contents.decode('utf-8'))
    except exceptions.NotFound as e:
        return {}
    except Exception as e:
        raise e


def create_directory(path):
    os.makedirs(path, exist_ok=True)


def replace_file(old_path, new_path):
    """
    old_path의 파일을 new_path로 이름 변경 또는 덮어쓰기.
    """
    if os.path.exists(old_path):
        os.replace(old_path, new_path)
