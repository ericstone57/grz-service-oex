#!/bin/bash

export $(grep -v '^#' .envs/.local/.app | xargs -0)
export $(grep -v '^#' .envs/.local/.db | xargs -0)
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

if [[ "$1" == 'api' ]]; then
  export $(grep -v '^#' .envs/.local/.fastapi | xargs -0)
  uvicorn config.asgi:fastapp --port 8052 --host 0.0.0.0 --reload
elif [[ "$1" == 'worker' ]]; then
  celery -A config.celery_app worker -l INFO
elif [[ "$1" == 'beat' ]]; then
  rm -f './celerybeat.pid'
  celery -A config.celery_app beat -l INFO
else
  uvicorn config.asgi:application --port 8051 --reload
fi
