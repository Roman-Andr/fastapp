FROM python:3.13-slim
RUN apt update && apt install curl -y
WORKDIR /fastapp

RUN pip install uv

COPY pyproject.toml .
RUN uv venv && \
    uv pip install --no-cache-dir -r pyproject.toml

COPY src/fastapp ./fastapp
EXPOSE 8000
CMD [".venv/bin/uvicorn", "fastapp.main:app", "--host", "0.0.0.0", "--port", "8000"]