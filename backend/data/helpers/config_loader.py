import json
from typing import Any, Dict


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        print(f"Loading config: {path}")
        return json.load(f)