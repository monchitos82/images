FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV

ENV HOSTS=''

WORKDIR /influxsensor

RUN apt-get update && apt-get install -y \
    build-essential iputils-ping\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r requirements.txt

COPY . .

CMD ["/opt/venv/bin/python", "/influxsensor/influx_sensor.py"]
