FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends jq \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend
RUN pip3 install -r requirements.txt
RUN cp config.py.sample config.py

EXPOSE 4001

CMD ["./start.sh"]
