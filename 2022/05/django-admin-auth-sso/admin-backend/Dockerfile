FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --upgrade pip pipenv

RUN pipenv install --system --deploy --dev --ignore-pipfile

COPY . ./

CMD ["./scripts/start-development.sh"]
