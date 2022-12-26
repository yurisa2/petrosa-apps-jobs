# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt
RUN pip install newrelic


ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_MONITOR_MODE=true
# ENV NEW_RELIC_LOG_LEVEL=debug
ENV NEW_RELIC_LOG=/tmp/newrelic.log


# COPY requirements.txt requirements.txt
