"""
extractor.extractor

Uso:
    python -m extractor.extractor <ruta-al-archivo>

Funcional:
- detecta MIME (si python-magic disponible)
- calcula hash SHA256
- si es PDF extrae texto parcial
- si es imagen genera thumbnail
- guarda registro en SQLite (evidence.db)
- imprime JSON con el registro
"""

import sys
import os
import json
import sqlite3
import traceback
from pathlib import Path
from PIL import Image

# optional dependency
try:
    import magic
except Exception:
    magic = None

from .utils import compute_hash

DB = "evidence.db"

def get_mime(path: str) -> str:
    if magic:
        try:
            return magic.from_file(path, mime=True)
        except Exception:
            return "unknown/unknown"
    # fallback by extension
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return "application/pdf"
    if ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    return "application/octet-stream"

def extract_text_pdf(path: str) -> str:
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(path)
        return text[:3000]  # snippet
    except Exception:
        return ""

def create_thumbnail(path: str, out_dir: str = "samples") -> str | None:
    try:
        img = Image.open(path)
        img.thumbnail((300, 300))
        out_path = os.path.join(out_dir, f"thumb_{os.path.basename(path)}")
        img.save(out_path)
        return out_path
    except Exception:
        return None

def save_record(record: dict) -> None:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            mimetype TEXT,
            sha256 TEXT,
            snippet TEXT
        )
    """)
    cur.execute("INSERT INTO evidence (path, mimetype, sha256, snippet) VALUES (?,?,?,?)",
                (record.get("path"), record.get("mimetype"), record.get("sha256"), record.get("snippet")))
    conn.commit()
    conn.close()

def analyze(path: str) -> dict:
    rec = {}
    abs_path = os.path.abspath(path)
    rec["path"] = abs_path
    rec["mimetype"] = get_mime(path)
    rec["sha256"] = compute_hash(path)
    rec["snippet"] = ""

    # if PDF extract text
    if rec["mimetype"] == "application/pdf" or path.lower().endswith(".pdf"):
        rec["snippet"] = extract_text_pdf(path)

    # if image create thumbnail
    if rec["mimetype"].startswith("image") or Path(path).suffix.lower() in [".jpg", ".jpeg", ".png"]:
        thumb = create_thumbnail(path)
        if thumb:
            rec["thumbnail"] = os.path.abspath(thumb)

    return rec

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m extractor.extractor <archivo>")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Archivo no encontrado: {path}")
        sys.exit(1)
    try:
        record = analyze(path)
        save_record(record)
        print(json.dumps(record, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Error durante el análisis:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

