FROM python:3.12.4-slim

WORKDIR /app

COPY pyproject.toml .

RUN python -m pip install --upgrade pip && \
    pip install ".[dev]"

COPY . .

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]