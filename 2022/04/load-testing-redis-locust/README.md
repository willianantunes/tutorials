# Estimating an initial Redis setup through Locust

Do you want to know how to estimate an initial Redis setup through Locust? Look at this project 👀!

## Project details

At the root folder of the project, just issue the following command:

    docker-compose up performance-testing

Then access the link `http://localhost:8089/` so you can configure your load test scenario.

If you just want to run the project and see sample reports, run the command:

    docker-compose up performance-testing-with-reports

You'll get the following reports:

```
locust_report_exceptions.csv
locust_report_failures.csv
locust_report_stats.csv
locust_report_stats_history.csv
```
