# Basis-Image mit Python
FROM python:3.9

# Arbeitsverzeichnis setzen
WORKDIR /app

# Notwendige Abhängigkeiten installieren
RUN pip install --no-cache-dir farm-haystack astra-haystack fastapi uvicorn torch transformers

# Kopiere den Code
COPY . /app

# Standard-Port setzen
ENV PORT=8000

# FastAPI starten
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
