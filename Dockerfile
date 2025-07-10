FROM python:3.13-slim

WORKDIR /fastapp

RUN pip install uv

COPY pyproject.toml .
COPY src/fastapp ./fastapp

RUN uv venv && \
    uv pip install --no-cache-dir -r pyproject.toml
EXPOSE 8000
CMD [".venv/bin/uvicorn", "fastapp.main:app", "--host", "0.0.0.0", "--port", "8000"]