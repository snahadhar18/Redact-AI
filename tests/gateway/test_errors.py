from fastapi import FastAPI
from fastapi.testclient import TestClient

from redactai.gateway.api.errors import register_error_handlers
from redactai.gateway.core.exceptions import ConfigurationError, IngestionError, RagGuardianError

app = FastAPI()
register_error_handlers(app)

@app.get("/error/config")
def err_config():
    raise ConfigurationError("bad config")

@app.get("/error/ingest")
def err_ingest():
    raise IngestionError("bad file format")

@app.get("/error/generic_rag")
def err_generic():
    raise RagGuardianError("generic error")

@app.get("/error/unexpected")
def err_unexpected():
    raise ValueError("unexpected crash")

client = TestClient(app, raise_server_exceptions=False)

def test_configuration_error_handling() -> None:
    response = client.get("/error/config")
    assert response.status_code == 500
    assert response.json() == {
        "error": "ConfigurationError",
        "detail": "bad config",
        "type": "redactai.gateway_error",
    }

def test_ingestion_error_handling() -> None:
    response = client.get("/error/ingest")
    assert response.status_code == 422
    assert response.json()["error"] == "IngestionError"

def test_generic_rag_error_handling() -> None:
    response = client.get("/error/generic_rag")
    assert response.status_code == 400
    assert response.json()["error"] == "RagGuardianError"

def test_unexpected_error_handling() -> None:
    response = client.get("/error/unexpected")
    assert response.status_code == 500
    assert response.json()["error"] == "InternalServerError"
    assert response.json()["type"] == "internal_error"
