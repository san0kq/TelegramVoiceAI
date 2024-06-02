FROM python:3.12-alpine as requirements_stage

ENV PYTHONUNBUFFERED=1

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-alpine

COPY --from=requirements_stage /tmp/requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r ./requirements.txt && \
    pip install --no-cache /wheels/* \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /code
