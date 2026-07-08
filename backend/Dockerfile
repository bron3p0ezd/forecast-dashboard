FROM python:3.13-alpine

WORKDIR /backend

COPY requirements.txt requirements.txt

RUN apk add --no-cache curl

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /backend/src

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info", "--access-log"]
