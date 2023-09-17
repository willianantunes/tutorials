FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --dev --ignore-pipfile

RUN rm Pipfile Pipfile.lock

CMD [ "./scripts/start-development.sh" ]
