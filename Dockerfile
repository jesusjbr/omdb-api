FROM python:3.12.9

ENV PYTHONUNBUFFERED=1

COPY . /app

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.6.12 /uv /bin/

RUN uv pip install --system --no-cache-dir -r requirements.txt

WORKDIR /app/src

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0",  "--port", "8080"]