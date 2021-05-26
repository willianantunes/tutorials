ARG MAIN_PROJECT_NAME=CSharpWebAPIHowToEndpointIT
ARG MAIN_PROJECT_SRC=./CSharpWebAPIHowToEndpointIT

ARG TEST_PROJECT_NAME=Tests
ARG TEST_PROJECT_SRC=./tests

FROM mcr.microsoft.com/dotnet/sdk:5.0

WORKDIR /app

ARG MAIN_PROJECT_NAME
ARG MAIN_PROJECT_SRC

ARG TEST_PROJECT_NAME
ARG TEST_PROJECT_SRC

# Restores (downloads) all NuGet packages from all projects of the solution on a separate layer
COPY ${MAIN_PROJECT_SRC}/*.csproj ${MAIN_PROJECT_SRC}/
COPY ${TEST_PROJECT_SRC}/*.csproj ${TEST_PROJECT_SRC}/

RUN dotnet restore ${MAIN_PROJECT_SRC}/${MAIN_PROJECT_NAME}.csproj
RUN dotnet restore ${TEST_PROJECT_SRC}/${TEST_PROJECT_NAME}.csproj

COPY . ./
