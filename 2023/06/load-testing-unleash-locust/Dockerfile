FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY load_testing_unleash_locust ./load_testing_unleash_locust

EXPOSE 8089 5557

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["locust"]
