# metrix

A tiny library for tracking and retrieving number of events occurred during specified interval of time.
Not thread-safe

## Usage

```python
from metrix import Metrix

client = Metrix(ttl=300)

for i in range(1000):
    client.increment(metric_name="some_metric_name")

client.sum(metric_name="some_metric_name", interval=10)
```

## Contributing

To install all the required dependencies via [poetry](https://python-poetry.org/):

```sh
$ make install
```

To run formatting and tests use command below:

```sh
$ make fmt && make test
```
