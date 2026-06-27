# Frequently Asked Questions (FAQ)

## General Information
1. **What is RedactAI?**
   RedactAI is an enterprise-grade toolkit that detects and redacts sensitive PII and secrets from text, logs, and files before they reach AI models or databases.
2. **Is RedactAI open source?**
   Yes, RedactAI is distributed under the MIT license.
3. **What is the difference between the engine and the gateway?**
   The engine (`redactai-engine`) is a local library/CLI for file processing. The gateway (`redactai-gateway`) is a web server and streaming infrastructure layer that wraps the engine.
4. **Does RedactAI phone home or send data externally?**
   No. RedactAI operates 100% locally or within your own VPC. It never sends data to third parties.

## Installation & Setup
5. **What versions of Python are supported?**
   Python 3.10, 3.11, and 3.12.
6. **How do I install just the CLI?**
   Run `pip install -e .` from the source root.
7. **How do I install the API and ML detectors?**
   Run `pip install -e ".[api,ai]"`.
8. **Is there a Docker image?**
   Yes, you can build it via `docker build -t redactai .` or use the provided `docker-compose.yml`.

## Features & Detection
9. **What types of PII does it detect?**
   Emails, Phones, IPv4/IPv6, US SSNs, and Credit Cards.
10. **What types of secrets does it detect?**
    JWTs, AWS Keys, OpenAI Keys, and generic high-entropy API tokens.
11. **Can I add my own detector?**
    Yes. Subclass `Detector` and register it in the `global_registry`.
12. **Does it support other languages for NLP?**
    Yes, by loading different spaCy models, but the default built-in ML detectors are optimized for English.
13. **What is the Shannon Entropy detector?**
    It detects highly randomized strings (like base64 tokens) that don't match specific regex patterns but mathematically look like cryptographic secrets.
14. **How does the Credit Card detector avoid false positives?**
    It applies the Luhn algorithm checksum to any 13-19 digit number before flagging it.
15. **Does it support PDF or Word documents?**
    Not directly. You must extract the text first (e.g., using `PyPDF2` or `Tika`) and pass the raw text to RedactAI.

## Usage & API
16. **How do I redact a single file?**
    `redactai-engine scrub input.txt output.txt`
17. **Can I process multiple files at once?**
    Yes, use `redactai-engine batch /logs/*.log -o /safe_logs/`
18. **Can I stream logs into it?**
    Yes: `tail -f app.log | redactai-gateway stream`
19. **How do I start the API?**
    `redactai-gateway serve --port 8000`
20. **Is there an SDK for Python?**
    Yes, you can import `RedactionEngine` and use it programmatically.
21. **How do I mask instead of replacing with tags?**
    Use the `--mask` flag in the CLI, or set `redact=True` and configure a mask redactor in the API.

## Performance
22. **Will processing a 100GB log file crash my server?**
    No. RedactAI streams the file line-by-line and uses bounded memory (`O(1)` space).
23. **Is it multithreaded?**
    Yes. The batch CLI and API use `ThreadPoolExecutor` to process records concurrently.
24. **How fast is it?**
    On modern hardware, it processes roughly 1GB of text per 10-15 seconds depending on the number of active detectors.
25. **Can I run it on Kubernetes?**
    Yes. The API is completely stateless and scales horizontally behind a Load Balancer.

## Troubleshooting
26. **I get a ModuleNotFoundError when running python -m.**
    Ensure you ran `pip install -e .` or have `src/` in your `PYTHONPATH`.
27. **Why is the spaCy ML detector crashing?**
    You need to download the model first: `python -m spacy download en_core_web_sm`.
28. **The stream command throws an OS Error on Windows.**
    The `sys.stdin` pipeline on Windows PowerShell ISE can break signal handlers. Use standard Command Prompt or Git Bash.
29. **My custom detector isn't showing up.**
    Make sure you registered it via `global_registry.register("name", MyClass)`.
30. **How do I see debug logs?**
    Set the environment variable `RG_OBSERVABILITY__LOG_LEVEL=DEBUG`.
