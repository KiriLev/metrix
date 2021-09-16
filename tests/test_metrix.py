import time

import pytest

from metrix import Metrix


@pytest.fixture
def client():
    return Metrix()


@pytest.fixture
def metric_name():
    return "abacaba"


def test_ok(client: Metrix, metric_name: str):
    # WHEN: increment metric 1000 times
    for i in range(1000):
        client.increment(metric_name=metric_name)

    # AND: sleep for 2 s
    time.sleep(2)

    # AND: increment metric 1000 times
    for i in range(1000):
        client.increment(metric_name=metric_name)

    # THEN: sum with interval=5 should be equal to 2000
    assert client.sum(metric_name=metric_name, interval=5) == 2000

    # AND: sum with interval=1 should be equal to 1000 and not include events occurred before
    assert client.sum(metric_name=metric_name, interval=1) == 1000


def test_multiple_metrics(client: Metrix):
    # GIVEN: multiple metrics names
    metric_names = ["a", "b", "c", "d"]

    # WHEN: increment counters for each metric_name
    for name in metric_names:
        client.increment(metric_name=name)

    # THEN: sum value for each metric_name should be 1
    for name in metric_names:
        assert client.sum(metric_name=name, interval=5) == 1


def test_wrong_metric_name(client: Metrix, metric_name: str):
    # WHEN: increment counter with `metric_name`
    client.increment(metric_name)

    # THEN: `sum` for `metric_name` returns 1
    assert client.sum(metric_name, 5) == 1

    # AND: `sum` for not existing metric name returns 0
    assert client.sum(metric_name + "a", 5) == 0


def test_ttl(metric_name: str):
    # GIVEN: init client with ttl = 2s
    client = Metrix(ttl=2)

    # WHEN: increment counter
    client.increment(metric_name=metric_name)

    # THEN: count sum with interval 1s == 1
    assert client.sum(metric_name=metric_name, interval=1) == 1

    # WHEN: sleep 3s
    time.sleep(3)
    # THEN: count sum with interval 1s == 0
    assert client.sum(metric_name=metric_name, interval=1) == 0

    # WHEN: do increment one more time
    client.increment(metric_name=metric_name)

    # THEN: count sum with interval = 1s == 1
    assert client.sum(metric_name=metric_name, interval=1) == 1


def test_interval_greater_than_ttl(metric_name: str):
    # GIVEN: init client with ttl = 2s
    client = Metrix(ttl=2)

    # WHEN: increment counter
    client.increment(metric_name=metric_name)

    # THEN: `sum` for interval == ttl not raises any error and returns 1
    assert client.sum(metric_name, 2) == 1

    # AND: `sum` for interval > ttl not raises any error and returns 1
    assert client.sum(metric_name, 10) == 1


def test_ttl_zero():
    # THEN: init with ttl <= 0s causes error
    with pytest.raises(ValueError):
        Metrix(ttl=0)
        Metrix(ttl=-5)
