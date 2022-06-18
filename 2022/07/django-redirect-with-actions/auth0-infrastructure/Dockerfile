FROM nikolaik/python-nodejs:python3.10-nodejs14-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY package.json package-lock.json ./

RUN npm ci

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --dev --ignore-pipfile

COPY . ./

CMD ["./scripts/orchestrate.sh"]
