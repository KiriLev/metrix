import time
from bisect import bisect_left
from collections import defaultdict


class Metrix:
    def __init__(self, ttl: float = 300):
        """
        Inits Metrix.
        Args:
             ttl (float): time-to-live in seconds for events
        """
        self.ttl = ttl
        self._metrics_data = defaultdict(list)

    def increment(self, metric_name: str) -> None:
        """
        Increments counter for a specified `metric_name`.
        Args:
            metric_name (str): Name of metric to increment.
        """
        event_time = time.time()
        self._validate_ttl(metric_name)
        self._metrics_data[metric_name].append(event_time)

    def sum(self, metric_name: str, start: float) -> int:
        """
        Returns counter value for a specified `metric_name` and specified
        time range (from `start` to current time).
        Args:
            metric_name (str): Name of metric to retrieve number of occurrences.
            start (float): timestamp representing starting point of a query to return
        Raises:
            ValueError: Wrong metric name
        Returns:
            sum: number
        """
        if metric_name not in self._metrics_data:
            raise ValueError(
                f"Wrong metric name, available are: {list(self._metrics_data.keys())}"
            )

        self._validate_ttl(metric_name)
        metric_ts = self._metrics_data[metric_name]

        if len(metric_ts) == 0:
            return 0

        if start < metric_ts[0]:
            return len(metric_ts)

        if start > metric_ts[-1]:
            return 0

        # finding first greatest or equal element by binsearch in O(logn)
        return len(metric_ts) - bisect_left(metric_ts, start)

    def _validate_ttl(self, metric_name: str):
        """
        Removes expired events.
        Args:
            metric_name (str): Name of metric to retrieve number of occurrences.
        """
        metric_ts = self._metrics_data[metric_name]
        expired_before = time.time() - self.ttl

        i = 0

        # linear search from the beginning, should be faster in most cases than binary on whole array
        while i < len(metric_ts) and metric_ts[i] < expired_before:
            i += 1

        if i > 0:
            self._metrics_data[metric_name] = self._metrics_data[metric_name][i:]
