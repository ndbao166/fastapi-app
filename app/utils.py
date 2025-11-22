import json
from typing import Any


def load_example_json(file_path: str) -> dict[str, Any]:
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def get_password_hash(password: str) -> str:
    return password + "hashed"
