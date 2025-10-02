# redics

Publish redis values as prometheus metrics.

## supported metrics

* [x] length of lists

## configuration

The redics configuration is provided as a single toml file, explained below. When
running redics expects to find an environment variable `REDICS_CONFIG` which is
a path to toml file like below.

A redis url is required, which can be provider either in the config file *or* as
an environment variable `REDICS_REDIS_URL`. The environment variable takes precedence.

```toml
# mandatory, unless an environment value for REDICS_REDIS_URL is set
redis_url = "redis://127.0.0.1:6379"

# redis lists which will have their length published as a gauge metric
[list_lengths]
name = "foobar"  # the name to expose the lists under
# redis list keys, each will have its length published with it as a label
keys = ["abc", "xyz"]
```

### example configuration

This would publish the list lengths of `abc` and `xyz` on a metric named `foobar`.

```toml
redis_url = "redis://redis:6379"

[list_lengths]
name = "foobar"
keys = ["abc", "xyz"]
```

When hitting `/metrics` this configuration would result in something like

```text
# HELP foobar Length of redis lists.
# TYPE foobar gauge
foobar{list="abc"} 0 1759435076954
foobar{list="xyz"} 0 1759435076954
```
