#!/usr/bin/env bash
# run.sh: Analiza un archivo y guarda registro en SQLite
if [ -z "$1" ]; then
  echo "Uso: ./run.sh <archivo>"
  exit 1
fi
python -m extractor.extractor "$1"
