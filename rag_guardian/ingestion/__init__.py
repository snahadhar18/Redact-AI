"""Ingestion layer: pluggable, memory-efficient record sources.

Every source converts some external representation (a text/log file, a CSV, a
JSON document or stream) into a uniform stream of :class:`Record` objects that
the processing engine can consume. Sources are lazy and chunked so a multi-
gigabyte file never has to be resident in memory.
"""

from __future__ import annotations

from rag_guardian.ingestion.base import BaseIngestionSource
from rag_guardian.ingestion.csv_source import CSVSource
from rag_guardian.ingestion.factory import SourceFactory, SourceType
from rag_guardian.ingestion.file_source import FileSource
from rag_guardian.ingestion.json_source import JSONSource

__all__ = [
    "BaseIngestionSource",
    "FileSource",
    "CSVSource",
    "JSONSource",
    "SourceFactory",
    "SourceType",
]
