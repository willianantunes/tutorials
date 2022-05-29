FROM python:3.10-slim

WORKDIR /app

RUN useradd appuser && chown appuser ./

RUN pip install --upgrade pip && pip install poetry

COPY --chown=appuser poetry.lock pyproject.toml ./

RUN poetry export -f requirements.txt -o requirements.txt && \
    pip uninstall --yes poetry && \
    pip install --require-hashes -r requirements.txt

COPY --chown=appuser . ./

USER appuser
