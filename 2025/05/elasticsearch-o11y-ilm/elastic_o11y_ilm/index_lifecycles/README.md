# Phases transitioning

The JSON files have been captured by executing the following request in the Dev Tools:

```shell
GET .ds-metrics-apm.app.all-default-2025.05.31-000001/_ilm/explain
```

Check them in the following order:

- [hot.json](./hot.json)
- [warm-1-migrate.json](./warm-1-migrate.json)
- [warm-2-complete.json](./warm-2-complete.json)
- [cold-1-migrate.json](./cold-1-migrate.json)
- [cold-2-complete.json](./cold-2-complete.json)
- [delete-1-wait-for-shard-history-leases.json](./delete-1-wait-for-shard-history-leases.json)
- [delete-2-check-ts-end-time-passed.json](./delete-2-check-ts-end-time-passed.json)
- [delete-3-not-found.json](./delete-3-not-found.json)
