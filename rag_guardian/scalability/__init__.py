"""Scalability layer -- interface contracts for distributed deployment.

This package defines the *seams* that let RAG Guardian scale from a single
process to a distributed fleet without rewriting the core. It intentionally
ships interfaces and an in-memory reference implementation only: concrete Redis,
Kafka and RabbitMQ backends are optional add-ons (see ``docs/scalability.md``)
so the base install stays dependency-light.

Two abstractions cover the distributed story:

* :class:`MessageBroker` -- enqueue/consume work items across processes/hosts.
* :class:`ResultSink`    -- publish scan results to a downstream system.
"""

from __future__ import annotations

from rag_guardian.scalability.broker import (
    InMemoryBroker,
    Message,
    MessageBroker,
    ResultSink,
)
from rag_guardian.scalability.worker import DistributedWorker

__all__ = [
    "Message",
    "MessageBroker",
    "ResultSink",
    "InMemoryBroker",
    "DistributedWorker",
]
