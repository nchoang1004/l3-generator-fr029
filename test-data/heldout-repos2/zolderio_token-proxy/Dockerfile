FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash token
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies directly (faster than building from pyproject.toml)
RUN mkdir -p /app/data && \
    pip install --no-cache-dir \
    "fastapi>=0.110,<1" \
    "uvicorn[standard]>=0.29,<1" \
    "httpx>=0.27,<1" \
    "spacy>=3.7,<4" \
    "maxminddb>=2.6,<3" && \
    python -m spacy download en_core_web_sm

COPY token_proxy/ ./token_proxy/

USER token
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -sf http://localhost:8080/health || exit 1

CMD ["uvicorn", "token_proxy.main:app", "--host", "0.0.0.0", "--port", "8080"]
