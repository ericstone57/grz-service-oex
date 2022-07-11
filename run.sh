#!/bin/bash

export $(grep -v '^#' .envs/.local/.app | xargs -0)
export $(grep -v '^#' .envs/.local/.db | xargs -0)
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"


if [[ "$1" == 'prod' || "$2" == 'prod' ]]; then
  export APP_ENV="production"
  echo "On PRODUCTION Environment..."
else
  echo "On DEVELOPMENT Environment..."
fi

if [[ "$1" == 'worker' ]]; then
  celery -A config.celery_app worker -l INFO
elif [[ "$1" == 'beat' ]]; then
  rm -f './celerybeat.pid'
  celery -A config.celery_app beat -l INFO
else
  uvicorn config.asgi:fastapp --host 0.0.0.0 --port 8051 --reload
fi
