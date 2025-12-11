# Backend Dockerfile — production-friendly for FAISS + MiniLM + FastAPI
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required for FAISS
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    wget \
    libblas-dev \
    liblapack-dev \
    libopenblas-dev \
    libffi-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# copy requirements and install (use cache-friendly layer)
COPY Backened/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt


# copy app
COPY Backened/ /app

# create a model cache directory (avoid downloading to root cache)
RUN mkdir -p /app/model_cache && chown -R 1000:1000 /app/model_cache

# optionally pre-download small embedding model to avoid cold-start during runtime
# NOTE: this increases image build time and size but speeds first-run
USER root
RUN python - <<PY
from sentence_transformers import SentenceTransformer
model_name = "sentence-transformers/all-MiniLM-L6-v2"
print("Pre-downloading model:", model_name)
SentenceTransformer(model_name).save('/app/model_cache/miniLM')
PY

# create non-root user and fix permissions
RUN useradd -m -u 1000 appuser \
 && chown -R appuser:appuser /app

USER appuser

ENV TRANSFORMERS_CACHE=/app/model_cache
ENV HF_HOME=/app/model_cache

EXPOSE 8000

# Use Gunicorn with Uvicorn workers for better process management
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

