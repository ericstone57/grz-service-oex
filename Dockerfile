FROM registry.cn-shanghai.aliyuncs.com/kuri/kuri-docker-uvicorn-gunicorn:latest

LABEL maintainer="Eric Lee <ericstone.dev@gmail.com>"

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./docker/production/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ENV PYTHONPATH=/app

ENTRYPOINT ["/entrypoint"]
