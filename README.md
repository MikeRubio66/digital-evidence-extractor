# Digital Evidence Extractor
Herramienta Python para extracción forense de archivos: metadatos, texto, hashes y registro en SQLite.

## Características
- Extrae texto de PDFs (pdfminer)
- Extrae thumbnails de imágenes
- Calcula hashes SHA256
- Registra evidencias en SQLite y exporta JSON

## Requisitos
Python 3.10+
pip install -r requirements.txt

## Uso
./run.sh samples/sample.pdf
