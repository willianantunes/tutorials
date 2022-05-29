# Rundeck recipe repository

This is a repository with just one sample recipe that deals with SonarCloud project creation. Of course, you can add many more using the pleasant Django management command solution.

## Project details

Learn more in [this blog post](https://www.google.com/search?q=COMMING+SOON&tbm=isch&ved=2ahUKEwjuhejH4IT4AhVCOLkGHQrjCs4Q2-cCegQIABAA&oq=COMMING+SOON&gs_lcp=CgNpbWcQAzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoECCMQJzoGCAAQHhAHOgYIABAeEAhQigRYlxBg6BFoAHAAeACAAaoBiAHrDJIBBDAuMTOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=72yTYq7SIMLw5OUPisar8Aw&bih=661&biw=1386).

```shell
docker build -t rundeck-recipe-repository .
kind load docker-image rundeck-recipe-repository:latest
```
