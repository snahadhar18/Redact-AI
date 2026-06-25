"""Tests for the ``rag-guardian`` Click CLI.

A fixture detector is registered into the process-wide registry so the CLI's
container can resolve it via ``-d fake_email``; the CLI never ships detection
logic of its own.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from pathlib import Path

import pytest
from click.testing import CliRunner

from rag_guardian.cli.main import cli
from rag_guardian.core.detector import DetectionSpan, Detector
from rag_guardian.core.registry import global_registry


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


def test_stream_command(runner: CliRunner) -> None:
    result = runner.invoke(cli, ["stream", "-d", "fake_email"], input="contact a@b.com\nplain\n")
    assert result.exit_code == 0, result.output
    lines = result.output.splitlines()
    assert "contact [EMAIL]" in lines
