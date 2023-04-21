FROM node:18-alpine AS parcel-build

WORKDIR /built-project
COPY .babelrc package.json package-lock.json ./
RUN npm ci

COPY app_python_django ./app_python_django

RUN npm run build

FROM python:3.9.7-slim AS main

WORKDIR /home/appuser

# This way when I run collectstatic command it will collect all the static files the application needs
COPY --from=parcel-build /built-project/app_python_django/apps/core/static/core/dist/ ./app_python_django/apps/core/static/core/dist/

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir --upgrade pip pipenv

RUN pipenv install --system --deploy --ignore-pipfile && \
    pip uninstall --yes pipenv

COPY . ./

RUN rm Pipfile Pipfile.lock package.json package-lock.json .babelrc

RUN useradd --user-group --system --uid 1000 appuser \
    && chown -R appuser /home/appuser

USER appuser

CMD [ "./scripts/start.sh" ]
