"""Observability: structured logging, metrics, audit logging and health checks.

These cross-cutting utilities are dependency-free (stdlib only) so they can be
imported from any layer -- including the hot processing path -- without pulling
in heavy frameworks. The FastAPI layer adapts them to HTTP, but they are not
coupled to it.
"""

from __future__ import annotations

from rag_guardian.observability.audit import AuditEvent, AuditLogger
from rag_guardian.observability.health import HealthCheck, HealthReport, HealthStatus
from rag_guardian.observability.logging_config import configure_logging, get_logger
from rag_guardian.observability.metrics import MetricsRegistry, Timer, metrics

__all__ = [
    "configure_logging",
    "get_logger",
    "MetricsRegistry",
    "Timer",
    "metrics",
    "AuditEvent",
    "AuditLogger",
    "HealthCheck",
    "HealthReport",
    "HealthStatus",
]
