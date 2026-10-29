FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV UV_PYTHON_DOWNLOADS=0
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python -c 'from app.database import Base, engine; from app.orders.models import Order; from app.payments.models import Payment; Base.metadata.create_all(bind=engine)' && uvicorn main:app --host 0.0.0.0 --port 8000"]