# Rundeck recipe repository

This is a repository with just one sample recipe that deals with SonarCloud project creation. Of course, you can add many more using the pleasant Django management command solution.

## Project details

Learn more in the blog post where I explain about the [Rundeck Recipe Repository](https://www.willianantunes.com/blog/2022/06/rundeck-recipe-repository/).

```shell
docker build -t rundeck-recipe-repository .
kind load docker-image rundeck-recipe-repository:latest
```
