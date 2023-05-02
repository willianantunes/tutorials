# App C# ASP.NET

This project demonstrates how to use feature toggles with Unleash.

## Configuration

- [ENV file used by Docker](./.env.development)
- [Application settings](./src/appsettings.json)

## Feature toggles

Look at the file [FeatureManagement.cs](./src/FeatureManagement.cs) and then try to find usages by the properties.

### Explore de API

Try to consult the API with [HTTPie](https://httpie.io/). 

How to list all posts. Change the toggle `SHOW_TAGS` to change the API behavior.

    http GET :5238/posts

How to create a profile. Change the toggle `ADD_POST` to disable the API or not.

```
http POST :5238/posts/5 \
title="Agrabah" \
content="Jafar and Iago" \
'tags:=["V1", "V2"]'
```
