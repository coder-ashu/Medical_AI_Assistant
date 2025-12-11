# Backened/Dockerfile — optimized for FAISS + MiniLM + FastAPI
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for building wheels / faiss
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential gcc g++ git wget libblas-dev liblapack-dev libopenblas-dev libffi-dev curl \
 && rm -rf /var/lib/apt/lists/*

# copy requirements and install (cache-friendly)
COPY Backened/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# copy application code
COPY Backened/ /app

# create model cache dir (mounted from host)
RUN mkdir -p /app/model_cache && chown -R 1000:1000 /app/model_cache

# create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV TRANSFORMERS_CACHE=/app/model_cache
ENV HF_HOME=/app/model_cache

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
