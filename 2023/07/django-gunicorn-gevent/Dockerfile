FROM python:3.11-slim

# Git is required for pre-commit
RUN apt update
RUN apt install -y git

# Creates application directory
WORKDIR /app

# Creates an appuser and change the ownership of the application's folder
RUN useradd appuser && chown appuser ./

# Installs poetry and pip
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

# Copy dependency definition to cache
COPY --chown=appuser poetry.lock pyproject.toml ./

# Installs projects dependencies as a separate layer
RUN poetry install --no-root

# Copies and chowns for the userapp on a single layer
COPY --chown=appuser . ./

CMD [ "./scripts/start-development.sh" ]
