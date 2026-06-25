# RAG Guardian

Infrastructure for an enterprise-grade AI security gateway: ingestion, stream
processing, concurrency, an HTTP API, observability and deployment around a
**pluggable detector contract**. RAG Guardian deliberately ships **no detection
logic** — detectors (regex, Presidio, spaCy, secret scanners, ML classifiers)
are external plugins integrated through a single interface.

## Install

```bash
pip install -e ".[api,json]"      # API + streaming JSON ingestion
pip install -e ".[dev]"           # everything + test/lint tooling
```

## The detector contract

Everything is built around this one seam (see `rag_guardian/core/detector.py`):

```python
class Detector:
    def detect(self, text: str) -> Sequence[DetectionSpan]:
        ...
```

Register a detector and the whole stack (CLI, API, streaming, workers) uses it:

```python
from rag_guardian.core.registry import global_registry
global_registry.register("my_detector", MyDetectorFactory)
```

External packages can advertise detectors via the `rag_guardian.detectors`
entry-point group; they are auto-discovered at startup with no code changes.

## CLI

```bash
rag-guardian detectors                       # list registered plugins
rag-guardian scan app.log -d my_detector     # redact a file to stdout
rag-guardian ingest data.csv                 # scan a file, print a summary
tail -f app.log | rag-guardian stream        # real-time redacting filter
rag-guardian serve --port 8000               # run the FastAPI service
```

## API

```bash
uvicorn rag_guardian.api.app:create_app --factory --port 8000
# POST /scan, POST /stream, POST /ingest, GET /health, GET /metrics
# OpenAPI docs at /docs
```

## Configuration

All settings are environment-driven with the `RG_` prefix and `__` nesting
(see `rag_guardian/config/settings.py`):

```bash
export RG_PROCESSING__WORKERS=16
export RG_API__PORT=9000
export RG_OBSERVABILITY__LOG_FORMAT=json
```

## Documentation

- [`architecture.md`](architecture.md) — layered design and data flow.
- [`scalability.md`](scalability.md) — horizontal scaling roadmap (Redis/Kafka/RabbitMQ).
