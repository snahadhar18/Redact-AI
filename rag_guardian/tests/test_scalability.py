"""Tests for the scalability layer (in-memory reference broker + worker)."""

from __future__ import annotations

import threading

from rag_guardian.core.models import Record, ScanResult
from rag_guardian.scalability.broker import InMemoryBroker, MessageBroker, ResultSink
from rag_guardian.scalability.worker import DistributedWorker
from rag_guardian.streaming.processor import ProcessingEngine


class CollectingSink:
    def __init__(self) -> None:
        self.results: list[ScanResult] = []

    def emit(self, result: ScanResult) -> None:
        self.results.append(result)

    def close(self) -> None:
        pass


def test_inmemory_broker_satisfies_protocol() -> None:
    assert isinstance(InMemoryBroker(), MessageBroker)
    assert isinstance(CollectingSink(), ResultSink)


def test_distributed_worker_processes_until_close(scan_service) -> None:
    broker = InMemoryBroker()
    sink = CollectingSink()
    engine = ProcessingEngine(scan_service, workers=2, redact=True)
    worker = DistributedWorker(broker, engine, sink)

    for i in range(5):
        broker.publish(Record(id=str(i), content="a@b.com"))

    thread = threading.Thread(target=worker.run)
    thread.start()
    # Give the worker time to drain, then close to end consumption.
    import time

    time.sleep(0.3)
    broker.close()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert len(sink.results) == 5
    assert all(r.hit_count == 1 for r in sink.results)
