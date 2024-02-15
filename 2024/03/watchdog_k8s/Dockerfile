FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . ./

CMD ["./scripts/start-production.sh"]
