"""HTTP API layer (FastAPI).

Exposes the gateway over HTTP: synchronous scanning, streaming, file ingestion,
health and metrics. The API is a thin adapter -- it validates input, delegates to
the core services resolved from the DI :class:`Container`, and serializes
results. No detection or business logic lives here.

``create_app`` is imported lazily so the rest of the package (and its tests) do
not require FastAPI to be installed.
"""

from __future__ import annotations

__all__ = ["create_app"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

    from redactai.gateway.config.settings import Settings
    from redactai.gateway.core.container import Container

def create_app(
    settings: Settings | None = None,
    container: Container | None = None,
) -> FastAPI:
    """Lazily import and build the FastAPI application.

    Importing here (rather than at module load) keeps ``fastapi`` an optional
    dependency for users who only need the CLI/library.
    """
    from redactai.gateway.api.app import create_app as _create_app

    return _create_app(settings, container)
