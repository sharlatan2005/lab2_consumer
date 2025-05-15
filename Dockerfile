FROM python:3.12-slim AS base

FROM base AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY ./requirements.txt ./requirements.txt
RUN apt-get update && \
    apt-get install -y libpq-dev gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runner

# Устанавливаем runtime-зависимости
RUN apt-get update && \
    apt-get install -y libpq5 && \ 
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]