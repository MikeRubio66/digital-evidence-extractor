import hashlib
from typing import Optional

def compute_hash(path: str, algo: str = "sha256") -> str:
    """
    Calcula hash (sha256 por defecto) de un archivo.
    """
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

