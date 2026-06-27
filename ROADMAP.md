# RedactAI Roadmap

RedactAI is actively maintained and continually expanding. This roadmap outlines our short-term goals, long-term vision, and areas where community contributions are highly welcomed.

## Q3 2026: Horizontal Scalability & Ecosystem Integration
- **Kafka & RabbitMQ Ingestion:** Finalize the `BrokerConsumer` integration to natively ingest streams directly from message brokers without a bespoke script.
- **Redis Cluster Support:** Enable robust distributed locking for parallel ingestion across multiple pod replicas in Kubernetes.
- **Pre-trained ML Classifiers:** Fine-tune small language models (SLMs) specifically for PII detection to replace heuristics for edge-case languages and regions.

## Q4 2026: Performance & Native Acceleration
- **Rust Core Extension:** Port the `RedactionEngine` and overlap resolution algorithms to Rust using PyO3 to bypass the Python GIL and drastically increase throughput for extreme workloads (100GB+).
- **GPU Acceleration for NLP:** Shift the spaCy and Presidio ML layers to leverage CUDA/MPS for faster Named Entity Recognition.
- **Web UI & Dashboard:** Develop a React-based administration dashboard that consumes the FastAPI gateway to provide real-time metrics, audit logs, and risk reports visually.

## 2027+: Enterprise Compliance & Cloud Native
- **Helm Charts:** Official Kubernetes Helm charts for deploying the RedactAI Gateway as a distributed service mesh.
- **Zero-Trust KMS Integrations:** Native integration with AWS KMS, HashiCorp Vault, and Azure Key Vault for decrypting streams before redaction.
- **Multi-Tenant Authorization:** Role-Based Access Control (RBAC) and OAuth2 support on the Gateway API.
- **Compliance Policy Enforcer:** Let administrators write policies (e.g., `Reject if HIPAA > 0.8`) and attach them to specific API keys.

---

### How to Influence the Roadmap
We build what the community needs. If you require a feature not listed here:
1. Open a **Feature Request** on GitHub.
2. Join the discussion in our GitHub Discussions board.
3. If you're tackling a roadmap item, leave a comment on the corresponding issue to claim it!
