# redics

Publish redis values as prometheus metrics.

## supported metrics

* [x] length of lists

## configuration

A redis url is needed to know how to connect to redis, which can be provided in one of 2 ways:

* `REDICS_REDIS_URL` - a full redis url, ex: `redis://1.2.3.4:4242/4`
* Each component can alternately be provided
    * `REDICS_REDIS_PROTO` - ex: `rediss` (default `redis`)
    * `REDICS_REDIS_HOST` - ex: `1.2.3.4` (default `127.0.0.1`)
    * `REDICS_REDIS_PORT` - ex: `4242` (default `6379`)
    * `REDICS_REDIS_DB` - ex: `4` (default `0`)

The `REDICS_REDIS_URL` takes precedence if both means of defining the url are provided.

The redics configuration is provided as a single toml file. When
running redics expects to find an environment variable `REDICS_CONFIG` which is
a path to toml file like below.

```toml
# redis lists which will have their length published as a gauge metric
[list_lengths]
name = "foobar"  # the name to expose the lists under
# redis list keys, each will have its length published with it as a label
keys = ["abc", "xyz"]
```

### example configuration

This would publish the list lengths of `abc` and `xyz` on a metric named `foobar`.

```toml
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
