FROM python:3.10-slim

WORKDIR /home/appuser

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --upgrade pip pipenv

RUN pipenv install --system --deploy --dev --ignore-pipfile && \
    pip uninstall --yes pipenv

COPY . ./

RUN rm Pipfile Pipfile.lock

RUN useradd --user-group --system --uid 1000 appuser \
    && chown -R appuser /home/appuser

USER appuser

CMD [ "./scripts/start.sh" ]
