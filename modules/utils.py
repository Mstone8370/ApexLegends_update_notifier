import json
import os

from modules import models


def save_dict_as_json(dict, path):
    """
    dict를 json 파일로 저장.
    """
    with open(path, mode="wt", encoding="utf-8") as file:
        json.dump(dict, file, ensure_ascii=False, indent=2, default=models.json_default)


def load_json_as_dict(path):
    """
    path의 json 파일을 읽어서 dict로 반환.
    """
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            return json.load(file)
    except:  # noqa: E722
        return {}


def create_directory(path):
    os.makedirs(path, exist_ok=True)


def replace_file(old_path, new_path):
    """
    old_path의 파일을 new_path로 이름 변경 또는 덮어쓰기.
    """
    if os.path.exists(old_path):
        os.replace(old_path, new_path)
