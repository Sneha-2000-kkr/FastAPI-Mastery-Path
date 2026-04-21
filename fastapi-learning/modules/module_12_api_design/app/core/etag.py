import hashlib
import json
from typing import Any


def strong_etag(payload: Any) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return '"' + hashlib.sha256(body).hexdigest()[:32] + '"'
