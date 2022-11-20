FROM python:3.10-slim

WORKDIR /app

RUN useradd appuser && chown appuser ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY --chown=appuser poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY --chown=appuser . ./

USER appuser
