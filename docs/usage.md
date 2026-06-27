# Usage Guide

RedactAI provides two main CLI binaries:
1. `redactai-engine`: Used for direct local file and batch processing.
2. `redactai-gateway`: Used for spinning up infrastructure like APIs and real-time streaming filters.

---

## 1. redactai-engine

### `scrub`
Scrub a single file. This is the canonical command for processing logs locally.

```bash
redactai-engine scrub [OPTIONS] INPUT OUTPUT
```

**Options:**
- `-d, --detector NAME`: Enable a specific detector (e.g., `email`, `credit_card`). Can be passed multiple times. Defaults to all built-in detectors.
- `--mask`: Replace matched secrets with `****` instead of typed placeholders like `[EMAIL_REDACTED]`.
- `--keep-last INTEGER`: When `--mask` is set, keep this many trailing characters visible (e.g., `****1234`).
- `--encoding TEXT`: Text encoding used to read/write. Defaults to `utf-8`.

**Examples:**
```bash
# Scrub using all detectors
redactai-engine scrub source.log safe.log

# Only scrub emails and IP addresses, masking everything except the last 4 characters
redactai-engine scrub passwords.txt safe_passwords.txt -d email -d ipv4 --mask --keep-last 4
```

### `batch`
Scrub many files concurrently into an output directory using a `ThreadPoolExecutor`.

```bash
redactai-engine batch [OPTIONS] INPUT_PATHS... -o OUTPUT_DIR
```

**Options:**
- `-o, --output-dir PATH`: (Required) Directory where scrubbed files are written.
- `--suffix TEXT`: Suffix inserted before the file extension. Defaults to `.scrubbed`.
- `-w, --workers INTEGER`: Maximum worker threads. Defaults to CPU count.
- (Also accepts all `scrub` options like `-d`, `--mask`, `--encoding`).

**Examples:**
```bash
# Process an entire directory of logs using 16 threads
redactai-engine batch /var/logs/nginx/*.log -o /var/logs/safe/ -w 16
```

### `detectors`
List all currently registered and available detectors.

```bash
redactai-engine detectors
```

---

## 2. redactai-gateway

### `serve`
Run the FastAPI REST microservice.

```bash
redactai-gateway serve [OPTIONS]
```

**Options:**
- `--host TEXT`: Host to bind to. Default is `127.0.0.1`.
- `--port INTEGER`: Port to bind to. Default is `8000`.

**Examples:**
```bash
redactai-gateway serve --host 0.0.0.0 --port 8080
```

### `stream`
Filter a live stream from `stdin` to `stdout` in real time. Perfect for piping logs.

```bash
redactai-gateway stream [OPTIONS]
```

**Options:**
- `-d, --detector NAME`: Detectors to enable.
- `--redact / --no-redact`: Whether to output the redacted text or just output structured metadata. Default is `--redact`.
- `-w, --workers INTEGER`: Override worker count for the concurrent stream processor.
- `--buffer-size INTEGER`: Set the max in-flight queue size to enforce backpressure.

**Examples:**
```bash
tail -f application.log | redactai-gateway stream -d aws_key -d openai_key > safe_application.log
```

### `ingest`
Scan a file or CSV/JSON dataset and print a compliance and risk summary instead of redacting the file directly.

```bash
redactai-gateway ingest [OPTIONS] INPUT_PATH
```

**Options:**
- `--source-type TEXT`: The format of the data. Choices are `auto`, `file`, `csv`, `json`.
- `-d, --detector NAME`: Detectors to use.

**Examples:**
```bash
redactai-gateway ingest users_dump.csv --source-type csv
```
