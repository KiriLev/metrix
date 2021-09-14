import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass
class Bucket:
    value: int = 0
    last_updated_at: Optional[int] = None

    def increment(self, timestamp: int):
        self.value += 1
        self.last_updated_at = timestamp

    def reset(self):
        self.value = 0
        self.last_updated_at = None


class Metrix:
    def __init__(self, ttl: int = 300):
        """
        Inits Metrix.
        Args:
             ttl (float): time-to-live in seconds for events
        """
        self.ttl = ttl
        self._metrics_data = defaultdict(lambda: [Bucket() for _ in range(self.ttl)])
        self._start_time = None

    def increment(self, metric_name: str) -> None:
        """
        Increments counter for a specified `metric_name`.
        Args:
            metric_name (str): Name of metric to increment.
        """
        event_time = int(time.time())
        if self._start_time is None:
            self._start_time = event_time

        bucket_ind = (event_time - self._start_time) % self.ttl
        bucket = self._metrics_data[metric_name][bucket_ind]

        # in case of already used and outdated bucket we need to reset its value before we increment
        if (
            bucket.last_updated_at is not None
            and bucket.last_updated_at < event_time - self.ttl
        ):
            bucket.reset()

        bucket.increment(event_time)

    def sum(self, metric_name: str, interval: int) -> int:
        """
        Returns counter value for a specified `metric_name` and specified
        time range.
        Args:
            metric_name (str): Name of metric to retrieve number of occurrences.
            interval (int): Number of seconds representing range of a query
        Raises:
            ValueError: Wrong metric name
        Returns:
            sum (int): number
        """
        event_time = int(time.time())

        if metric_name not in self._metrics_data:
            raise ValueError(
                f"Wrong metric name, available are: {list(self._metrics_data.keys())}"
            )

        sum_ = 0
        for bucket in self._metrics_data[metric_name]:
            if bucket.last_updated_at is not None:
                if (
                    bucket.last_updated_at < event_time - self.ttl
                ):  # reset outdated buckets
                    bucket.reset()
                elif bucket.last_updated_at > event_time - interval:
                    sum_ += bucket.value
        return sum_
