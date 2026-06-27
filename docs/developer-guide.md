# Developer Guide

Welcome to the RedactAI codebase! This guide explains how to extend the platform, write custom detectors, and understand the project's internal coding standards.

## 1. Project Architecture
The codebase is split into two primary namespaces:
- `src/redactai/engine/`: The core detection algorithms, regular expressions, risk scoring, and scrubbing logic. No external I/O or web servers live here.
- `src/redactai/gateway/`: The infrastructure wrapper. Contains FastAPI, Kafka ingestion, stream buffering, and the CLI.

## 2. Coding Standards
We enforce strict standards to ensure the core engine remains memory-safe and highly performant.

- **Formatting:** We use `ruff format`.
- **Linting:** We use `ruff check`.
- **Type Hinting:** 100% type coverage is enforced via `mypy --strict`.
- **Docstrings:** Use Google-style docstrings for any public class or function.

## 3. Creating a New Detector

To add a new PII or secret type, you must create a new detector plugin.

### Step 1: Subclass `Detector` or `RegexDetector`
Most detectors are regex-based. Create a new file in `src/redactai/engine/detectors/`.

```python
import re
from redactai.engine.detectors.base import RegexDetector

class StripeKeyDetector(RegexDetector):
    label = "STRIPE_KEY"
    pattern = re.compile(r"\b(sk_test|rk_test)_[a-zA-Z0-9]{24,99}\b")
    default_confidence = 0.99

    def validate(self, value: str) -> bool:
        # Optional: Add secondary validation logic here
        return True
```

### Step 2: Register the Detector
Open `src/redactai/engine/detectors/__init__.py` and add your detector to the `default_detectors` list or register it in the DI container.

### Step 3: Write Tests
Create a test file in `tests/engine/detectors/test_stripe_key.py`:

```python
from redactai.engine.detectors.stripe import StripeKeyDetector

def test_stripe_detector():
    detector = StripeKeyDetector()
    matches = detector.detect("My key is sk_test_1234567890abcdefghijklmnopqr")
    assert len(matches) == 1
    assert matches[0].value == "sk_test_1234567890abcdefghijklmnopqr"
    assert matches[0].label == "STRIPE_KEY"
```

## 4. Running Benchmarks
When modifying the core engine, always run the benchmarking suite to ensure no performance regressions.
```bash
pytest benchmarks/
```

## 5. Release Workflow & Versioning
We use [Semantic Versioning 2.0.0](https://semver.org/).

**Release Checklist:**
1. Ensure all CI checks pass.
2. Update the `CHANGELOG.md`.
3. Bump the version in `pyproject.toml` and `src/redactai/engine/__init__.py`.
4. Commit: `git commit -m "chore: bump version to vX.Y.Z"`
5. Tag: `git tag vX.Y.Z`
6. Push: `git push --tags`
7. GitHub Actions will automatically publish the wheel to PyPI.
