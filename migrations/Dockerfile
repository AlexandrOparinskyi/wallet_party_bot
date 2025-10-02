FROM python:3.11-slim

WORKDIR /app

RUN pip install alembic environs asyncpg

# Копируем всё необходимое для миграций
COPY migrations/ ./migrations/
COPY alembic.ini .
COPY database/ ./database/
COPY config.py .

CMD ["alembic", "upgrade", "head"]