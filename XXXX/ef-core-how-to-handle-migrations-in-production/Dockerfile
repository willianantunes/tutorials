ARG MAIN_PROJECT_SRC=./src
ARG TEST_PROJECT_SRC=./tests

FROM mcr.microsoft.com/dotnet/sdk:5.0

WORKDIR /app

ARG MAIN_PROJECT_SRC
ARG TEST_PROJECT_SRC

# https://github.com/dotnet/dotnet-docker/issues/520
ENV PATH="${PATH}:/root/.dotnet/tools"

# Tools used during development
RUN dotnet tool install --global dotnet-ef --verbosity d
RUN dotnet tool install --global dotnet-format --verbosity d

# Restores (downloads) all NuGet packages from all projects of the solution on a separate layer
COPY ${MAIN_PROJECT_SRC}/*.csproj ${MAIN_PROJECT_SRC}/
COPY ${TEST_PROJECT_SRC}/*.csproj ${TEST_PROJECT_SRC}/

RUN dotnet restore ${MAIN_PROJECT_SRC}
RUN dotnet restore ${TEST_PROJECT_SRC}

COPY . ./
