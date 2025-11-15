from extractor.utils import compute_hash
import os

def test_compute_hash_consistent(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hola")
    h1 = compute_hash(str(f))
    h2 = compute_hash(str(f))
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex length
