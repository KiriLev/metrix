# metrix

A tiny library for tracking and retrieving number of events occured during specified window of time.
Not thread-safe

## Usage

```python
import time
from metrix import Metrix

client = Metrix(ttl=300)

for i in range(1000):
    client.increment(metric_name="some_metric_name")

some_timestamp = time.time()-5

client.sum(metric_name="some_metric_name", start=some_timestamp)

```