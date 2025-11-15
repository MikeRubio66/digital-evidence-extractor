# Digital Evidence Extractor

Herramienta forense en Python para extraer metadatos, texto, thumbnails y hashes (SHA256) de archivos digitales. Registra evidencia en SQLite y exporta JSON para reportes periciales.

## Características
- Extracción de texto parcial de PDFs.
- Cálculo de hash SHA256.
- Registro en base SQLite `evidence.db`.
- Generación de miniaturas para imágenes.
- CLI simple para analizar archivos individuales.

## Requisitos
- Python 3.10+
- Tesseract instalado en el sistema si quieres OCR (opcional).

## Instalación
```bash
python -m venv venv
source venv/bin/activate   # linux/mac
venv\Scripts\activate      # windows
pip install -r requirements.txt

# Ejecutable
chmod +x run.sh
./run.sh samples/sample.txt

# O directamente con python
python -m extractor.extractor samples/sample.txt
