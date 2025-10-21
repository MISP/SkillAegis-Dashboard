FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends jq \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip setuptools \
    && /app/venv/bin/pip install -r backend/requirements.txt

ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:${PATH}"

WORKDIR /app/backend
RUN cp config.py.sample config.py

WORKDIR /app
EXPOSE 4001

CMD ["./start.sh"]
