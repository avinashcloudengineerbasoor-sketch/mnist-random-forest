# =========================
# Stage 1: build dependencies
# =========================
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


# =========================
# Stage 2: runtime image
# =========================
FROM python:3.10-slim

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH

# copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# copy app code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]