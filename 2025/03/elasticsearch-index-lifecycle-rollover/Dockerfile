FROM python:3.12-slim

WORKDIR /app

RUN useradd appuser && chown appuser ./

ARG VENV_PATH=./.venv

RUN python -m venv $VENV_PATH && \
    $VENV_PATH/bin/pip install -U pip setuptools && \
    $VENV_PATH/bin/pip install poetry && \
    ln -s $(pwd)/$VENV_PATH/bin/poetry /usr/local/bin/poetry && \
    poetry self add poetry-plugin-export --no-cache

COPY --chown=appuser poetry.lock pyproject.toml ./

RUN poetry export --only main -f requirements.txt -o requirements.txt --with-credentials && \
    rm -rf $VENV_PATH && rm /usr/local/bin/poetry && \
    pip install --require-hashes -r requirements.txt --no-cache-dir

COPY --chown=appuser . ./

USER appuser

CMD [ "./scripts/start-production.sh" ]
