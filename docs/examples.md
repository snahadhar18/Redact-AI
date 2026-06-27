# Examples

This document provides concrete, copy-pasteable examples for integrating and using RedactAI in various environments.

## 1. CLI Examples

### Scrubbing a local database dump
```bash
redactai-engine scrub pg_dump.sql safe_dump.sql -d email -d phone -d ssn
```

### Batch processing an S3 sync folder
```bash
# Assuming logs were downloaded from S3 to ./s3_logs/
redactai-engine batch ./s3_logs/*.json -o ./clean_logs/ --workers 16 --mask
```

### Real-time streaming
Pipe a Kubernetes log tail into RedactAI before writing it to a local file:
```bash
kubectl logs -f deployment/backend | redactai-gateway stream > clean_backend.log
```

---

## 2. Python SDK Examples

### Basic String Redaction
```python
from redactai.engine import RedactionEngine
from redactai.engine.detectors import default_detectors

engine = RedactionEngine(default_detectors())

text = "Hello, contact me at bob@gmail.com or 555-0199."
safe_text, count = engine.scrub_text(text)

print(f"Redacted {count} items:")
print(safe_text)
# Output: Hello, contact me at [EMAIL_REDACTED] or [PHONE_REDACTED].
```

### Extracting Structured Detection Data
```python
from redactai.engine import RedactionEngine
from redactai.engine.detectors import default_detectors

engine = RedactionEngine(default_detectors())

matches = engine.find_matches("User signed up with IP 192.168.1.1")
for m in matches:
    print(f"Found {m.label} at [{m.start}:{m.end}] with {m.confidence*100}% confidence.")
# Output: Found IPV4 at [23:34] with 95.0% confidence.
```

---

## 3. FastAPI REST Examples

### Starting the Server
```bash
export RG_PROCESSING__WORKERS=10
redactai-gateway serve --host 0.0.0.0 --port 8000
```

### Sending a Scan Request (cURL)
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "text": "My AWS key is AKIAIOSFODNN7EXAMPLE",
    "redact": true
  }'
```

---

## 4. Docker Examples

### Docker Compose
Create a `docker-compose.yml` to run the gateway:

```yaml
version: '3.8'
services:
  gateway:
    image: redactai:latest
    ports:
      - "8000:8000"
    environment:
      - RG_API__PORT=8000
      - RG_PROCESSING__WORKERS=8
    command: redactai-gateway serve --host 0.0.0.0 --port 8000
```
Run it:
```bash
docker-compose up -d
```
