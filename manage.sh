#!/bin/bash

export $(grep -v '^#' .envs/.local/.app | xargs -0)
export $(grep -v '^#' .envs/.local/.db | xargs -0)
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

python manage.py "$@"
