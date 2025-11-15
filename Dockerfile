FROM python:3.10-slim

# dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "extractor.extractor", "samples/sample.txt"]
