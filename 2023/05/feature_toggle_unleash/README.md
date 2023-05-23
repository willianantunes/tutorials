# Feature Toggle Unleash

To understand it, please read the article [Understand Feature Flags by Practice with Unleash](https://www.willianantunes.com/blog/2023/05/understand-feature-flags-by-practice-with-unleash/).

## Project details

Execute the command:

    docker-compose up

When everything is up, you can access Unleash with the address http://localhost:4242/ and credential:

```
admin
unleash4all
```

You can access the [**Python/Django application**](./app-python-django) at three addresses:

- Home: http://localhost:8000/
- APIs: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/

Use the credential `admin:admin` for the last address.

You can access the [**JavaScript/Next.js application**](./app-javascript-nextjs) from the address:

- http://localhost:3000/

You can access the [**C#/ASP.NET Core with Razor Pages**](./app-csharp-aspnet) from the address:

- http://localhost:5238/

## Importing the configuration on Unleash

Access the project's link:

- http://localhost:4242/projects/default

Then click on `Import` icon. It's above the `Event log` tab. Now select the file the JSON file from the iac folder:

- [2023-04-29T21_20_20.516Z-export.json](./iac/2023-04-29T21_20_20.516Z-export.json)

Follow the wizard and finish the importing process. If you access `http://localhost:4242/features` you should see the following image:

![](./docs/2023-04-25-17-03-00-Screenshot.png)

## Backup the configuration data from the database

Let's say your Unleash instance is fully configured, then you can access the PostgreSQL container with `docker-compose exec db bash` and execute the following command:

```
cd /tmp && pg_dump --clean -U unleash -w -h localhost development > unleash-db.dump.sql
```

Copy the dump from the container to your local machine using the docker cp command. Run this command outside the container:

```
docker cp <container_name>:/tmp/unleash-db.dump.sql ./
```

Now you are able to use `psql` to restore the backup.

## Restore the configuration data into the database

Execute the command:

    docker-compose up

Copy the dump file to the container:

    docker cp ./iac/unleash-db.dump.sql b18d047f7b4b:/tmp

Access its container:

    docker-compose exec db bash

Given you have the dump file, then you can issue:

    psql -U unleash -w -h localhost development < /tmp/unleash-db.dump.sql
