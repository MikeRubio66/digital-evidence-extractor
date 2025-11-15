import sys, os, json, sqlite3
from pdfminer.high_level import extract_text
from PIL import Image
try:
    import magic
except:
    magic = None
from .utils import compute_hash

DB="evidence.db"

def explain_type(path):
    if magic:
        try:
            return magic.from_file(path, mime=True)
        except:
            return "unknown/unknown"
    return "unknown/unknown"

def extract_text_preview(path):
    if path.lower().endswith('.pdf'):
        try:
            return extract_text(path)[:3000]
        except Exception as e:
            return ""
    return ""

def create_thumbnail(path, outpath):
    try:
        img = Image.open(path)
        img.thumbnail((300,300))
        img.save(outpath)
        return outpath
    except:
        return None

def analyze_file(path):
    rec = {}
    rec['path']=os.path.abspath(path)
    rec['mimetype']=explain_type(path)
    rec['sha256']=compute_hash(path)
    rec['snippet']=extract_text_preview(path)
    return rec

def save_record(record):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT, mimetype TEXT, sha256 TEXT, snippet TEXT
    )""")
    cur.execute("INSERT INTO evidence (path,mimetype,sha256,snippet) VALUES (?,?,?,?)",
                (record['path'], record['mimetype'], record['sha256'], record['snippet']))
    conn.commit()
    conn.close()

def main():
    if len(sys.argv)<2:
        print('Usage: run.sh <file>')
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print('File not found:', path); sys.exit(1)
    rec = analyze_file(path)
    save_record(rec)
    print(json.dumps(rec, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
