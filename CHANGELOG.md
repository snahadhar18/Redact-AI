# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Unified Architecture**: Merged the standalone engine and gateway into a single, cohesive `redactai` namespace (`redactai.engine` and `redactai.gateway`).
- **Comprehensive Documentation**: Complete overhaul of the project's documentation, including architecture diagrams, API schemas, and performance benchmarks.
- **AI/ML Detection Layer**: Presidio and spaCy integration for NLP-based Named Entity Recognition of PII.
- **Compliance Engine**: Rule-based categorization of detected elements into GDPR, HIPAA, PCI-DSS, and SOC2 profiles.
- **Risk Scoring**: Document-level risk assessment based on Shannon entropy, density of PII, and critical matches.

### Changed
- Rebranded project from `pii-scrub-stream` / `rag_guardian` to **RedactAI**.
- CLI commands are now scoped to `redactai-engine` and `redactai-gateway`.
- `RegexDetector` base class updated to expose confidence weighting out-of-the-box.

### Fixed
- Fixed an intermittent failure in the `redactai-gateway stream` testing harness by resolving a signal handling clash on Windows.
- Rectified GitHub Actions CI workflow to point to the new `src/redactai` and `tests/` directories.

## [0.1.0] - 2026-06-25

### Added
- Initial release of the core engine.
- Implemented streaming file and stdin processors.
- 10 built-in detectors: Email, Phone, IPv4/IPv6, Credit Card, SSN, JWT, AWS Keys, OpenAI Keys, and Generic API Keys.
- Concurrent file scrubbing powered by `ThreadPoolExecutor`.
- Initial gateway featuring FastAPI `/scan` and `/stream` endpoints.
