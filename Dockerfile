FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
RUN cp config.py.sample config.py

EXPOSE 4001

CMD ["./start.sh"]
