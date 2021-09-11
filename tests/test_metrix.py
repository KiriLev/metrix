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
    # GIVEN: start timestamp
    start_time = time.time()

    # WHEN: increment metric 1000 times
    for i in range(1000):
        client.increment(metric_name=metric_name)

    # AND: store timestamp after first increment
    mid_time = time.time()

    # AND: increment metric 1000 times
    for i in range(1000):
        client.increment(metric_name=metric_name)

    # THEN: sum from `start_time` should be equal to 2000
    assert client.sum(metric_name=metric_name, start=start_time) == 2000

    # AND: sum from `mid_time` should be equal to 1000 and not include events occured before
    assert client.sum(metric_name=metric_name, start=mid_time) == 1000


def test_multiple_metrics(client: Metrix):
    start_time = time.time()

    # GIVEN: multiple metrics names
    metric_names = ["a", "b", "c", "d"]

    # WHEN: increment counters for each metric_name
    for name in metric_names:
        client.increment(metric_name=name)

    # THEN: sum value for each metric_name should be 1
    for name in metric_names:
        assert client.sum(metric_name=name, start=start_time) == 1


def test_ttl(metric_name: str):
    # GIVEN: init client with ttl = 0.5s
    start_time = time.time()
    client = Metrix(ttl=0.5)

    # WHEN: increment counter
    client.increment(metric_name=metric_name)

    # THEN: counter sum from start_time == 1
    assert client.sum(metric_name=metric_name, start=start_time) == 1

    # WHEN: sleep 1 sec
    time.sleep(1)
    # THEN: counter sum from start_time == 0
    assert client.sum(metric_name=metric_name, start=start_time) == 0
