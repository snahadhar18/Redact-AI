"""Tests for the ``redactai`` Click CLI.

A fixture detector is registered into the process-wide registry so the CLI's
container can resolve it via ``-d fake_email``; the CLI never ships detection
logic of its own.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from pathlib import Path
from unittest import mock

import pytest
from click.testing import CliRunner

from redactai.gateway.cli.main import cli
from redactai.gateway.core.detector import DetectionSpan, Detector
from redactai.gateway.core.registry import global_registry


class _FakeEmailDetector(Detector):
    name = "fake_email"
    labels = ("EMAIL",)
    _pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

    def detect(self, text: str) -> Sequence[DetectionSpan]:
        return [
            DetectionSpan(m.start(), m.end(), "EMAIL", m.group(), 0.99, "[EMAIL]")
            for m in self._pattern.finditer(text)
        ]


@pytest.fixture(autouse=True)
def _register_detector() -> None:
    global_registry.register("fake_email", _FakeEmailDetector, replace=True)
    yield
    global_registry.unregister("fake_email")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_detectors_lists_registered(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["detectors"])
    assert result.exit_code == 0
    assert "fake_email" in result.output


def test_scan_redacts_file(runner: CliRunner, tmp_path: Path) -> None:
    p = tmp_path / "in.log"
    p.write_text("ping a@b.com\nplain line\n", encoding="utf-8")
    result = runner.invoke(cli, ["scan", str(p), "-d", "fake_email"])
    assert result.exit_code == 0, result.output
    assert "ping [EMAIL]" in result.output
    assert "plain line" in result.output


def test_scan_report_mode(runner: CliRunner, tmp_path: Path) -> None:
    p = tmp_path / "in.log"
    p.write_text("a@b.com\n", encoding="utf-8")
    result = runner.invoke(cli, ["scan", str(p), "-d", "fake_email", "--no-redact"])
    assert result.exit_code == 0, result.output
    row = json.loads(result.output.splitlines()[0])
    assert row["hits"] == 1
    assert row["labels"] == ["EMAIL"]


def test_ingest_summary(runner: CliRunner, tmp_path: Path) -> None:
    p = tmp_path / "data.csv"
    p.write_text("name,email\nAlice,a@b.com\nBob,b@c.com\n", encoding="utf-8")
    result = runner.invoke(cli, ["ingest", str(p), "-d", "fake_email"])
    assert result.exit_code == 0, result.output
    summary = json.loads(result.output)
    assert summary["records"] == 2
    assert summary["spans"] == 2
    assert summary["label_counts"]["EMAIL"] == 2


@mock.patch("redactai.gateway.streaming.stream.StreamProcessor._install_signals")
def test_stream_command(mock_install_signals, monkeypatch: pytest.MonkeyPatch) -> None:
    import io

    from redactai.gateway.cli.main import stream
    monkeypatch.setattr("sys.stdin", io.StringIO("contact a@b.com\nplain\n"))
    out = io.StringIO()
    monkeypatch.setattr("sys.stdout", out)
    
    stream.callback(detectors=("fake_email",), redact=True, workers=None, buffer_size=None)
    
    lines = out.getvalue().splitlines()
    assert "contact [EMAIL]" in lines


@mock.patch("redactai.gateway.streaming.stream.StreamProcessor._install_signals")
def test_stream_command_buffer_size(mock_install_signals, monkeypatch: pytest.MonkeyPatch) -> None:
    import io

    from redactai.gateway.cli.main import stream
    monkeypatch.setattr("sys.stdin", io.StringIO("test\n"))
    out = io.StringIO()
    monkeypatch.setattr("sys.stdout", out)
    stream.callback(detectors=(), redact=True, workers=None, buffer_size=10)
    assert out.getvalue() != ""
    monkeypatch.setattr("sys.stdin", io.StringIO("test\n"))
    out = io.StringIO()
    monkeypatch.setattr("sys.stdout", out)
    stream.callback(detectors=(), redact=True, workers=None, buffer_size=10)
    assert out.getvalue() != ""


def test_serve_command(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    import sys
    from types import ModuleType
    mock_uvicorn = ModuleType("uvicorn")
    mock_uvicorn.run = mock.Mock() # type: ignore
    monkeypatch.setitem(sys.modules, "uvicorn", mock_uvicorn)
    
    result = runner.invoke(cli, ["serve", "--port", "9090"])
    assert result.exit_code == 0
    mock_uvicorn.run.assert_called_once()
    assert mock_uvicorn.run.call_args[1]["port"] == 9090


def test_serve_command_no_uvicorn(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    import sys
    monkeypatch.setitem(sys.modules, "uvicorn", None) # type: ignore
    result = runner.invoke(cli, ["serve"])
    assert result.exit_code != 0
    assert "uvicorn is not installed" in result.output
