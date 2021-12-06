FROM registry.cn-shanghai.aliyuncs.com/kuri/kuri-docker-python:latest

LABEL maintainer="Eric Lee <ericstone.dev@gmail.com>"

WORKDIR /app/

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/app
