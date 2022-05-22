# Remco

It's used to generate the Rundeck configuration files from templates. It supports different key/value sources such as vault, etcd, and dynamodb. All configuration backends are combined into a unified keyspace. This allows storing parts of the configuration space in different backends. The default configuration uses environment variables.

Extending the configuration involves building a derived image with additional template files.

- `config.toml`: Where the config backends and resource includes are configured.
- `remco/resources.d`: Directory that includes the resources files declaring the templates.
- `remco/templates`: Directory where the templates are stored.

## References

- [Extending Docker Configuration](https://docs.rundeck.com/docs/administration/configuration/docker/extending-configuration.html#configuration-layout)
