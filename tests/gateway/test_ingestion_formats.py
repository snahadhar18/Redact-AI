from pathlib import Path

import pytest

from redactai.gateway.config.settings import IngestionSettings
from redactai.gateway.ingestion.csv_source import CSVSource
from redactai.gateway.ingestion.json_source import JSONSource


def test_csv_source_read(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "name,email\nAlice,alice@example.com\nBob,bob@example.com", encoding="utf-8"
    )
    
    source = CSVSource(csv_file, settings=IngestionSettings())
    source.open()
    records = list(source.read_records())
    source.close()
    
    assert len(records) == 2
    assert "Alice" in records[0].content
    assert "bob@example.com" in records[1].content


def test_json_source_read_lines(tmp_path: Path) -> None:
    json_file = tmp_path / "test.jsonl"
    json_file.write_text('{"name": "Alice"}\n{"name": "Bob"}', encoding="utf-8")
    
    source = JSONSource(json_file, settings=IngestionSettings())
    source.open()
    records = list(source.read_records())
    source.close()
    
    assert len(records) == 2
    assert "Alice" in records[0].content
    assert "Bob" in records[1].content


def test_json_source_read_array(tmp_path: Path) -> None:
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"name": "Alice"}, {"name": "Bob"}]', encoding="utf-8")
    
    source = JSONSource(json_file, settings=IngestionSettings())
    source.open()
    records = list(source.read_records())
    source.close()
    
    assert len(records) == 2
    assert "Alice" in records[0].content
    assert "Bob" in records[1].content


def test_json_source_invalid_lines(tmp_path: Path) -> None:
    json_file = tmp_path / "test.jsonl"
    json_file.write_text('{"name": "Alice"}\nbad_json\n', encoding="utf-8")
    source = JSONSource(json_file, settings=IngestionSettings())
    with pytest.raises(Exception) as exc:
        list(source.read_records())
    assert "invalid JSON on line 2" in str(exc.value)


def test_json_source_invalid_array(tmp_path: Path) -> None:
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"name": "Alice"}, bad]', encoding="utf-8")
    source = JSONSource(json_file, settings=IngestionSettings())
    with pytest.raises(Exception) as exc:
        list(source.read_records())
    assert "invalid JSON" in str(exc.value)


def test_json_source_not_array(tmp_path: Path) -> None:
    json_file = tmp_path / "test.json"
    json_file.write_text('{"name": "Alice"}', encoding="utf-8")
    source = JSONSource(json_file, settings=IngestionSettings())
    with pytest.raises(Exception) as exc:
        list(source.read_records())
    assert "expected a top-level JSON array" in str(exc.value)


def test_json_source_content_field(tmp_path: Path) -> None:
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"data": "Alice", "other": "Bob"}]', encoding="utf-8")
    source = JSONSource(json_file, settings=IngestionSettings(), content_field="data")
    records = list(source.read_records())
    assert records[0].content == "Alice"


def test_json_source_string_value(tmp_path: Path) -> None:
    json_file = tmp_path / "test.json"
    json_file.write_text('["Alice", "Bob"]', encoding="utf-8")
    source = JSONSource(json_file, settings=IngestionSettings())
    records = list(source.read_records())
    assert records[0].content == "Alice"


def test_json_source_file_not_found(tmp_path: Path) -> None:
    source = JSONSource(tmp_path / "missing.json", settings=IngestionSettings())
    with pytest.raises(Exception) as exc:
        source.open()
    assert "file not found" in str(exc.value)


def test_csv_source_file_not_found(tmp_path: Path) -> None:
    source = CSVSource(tmp_path / "missing.csv")
    with pytest.raises(Exception) as exc:
        source.open()
    assert "file not found" in str(exc.value)


def test_csv_source_empty_with_header(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("", encoding="utf-8")
    source = CSVSource(csv_file, has_header=True)
    records = list(source.read_records())
    assert len(records) == 0


def test_csv_source_no_header(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Alice,alice@example.com\nBob,bob@example.com", encoding="utf-8")
    source = CSVSource(csv_file, has_header=False)
    records = list(source.read_records())
    assert len(records) == 2
    assert records[0].metadata["fields"]["0"] == "Alice"


def test_csv_source_specific_columns(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,email,age\nAlice,alice@example.com,30", encoding="utf-8")
    source = CSVSource(csv_file, has_header=True, columns=["email", "1", "nonexistent"])
    records = list(source.read_records())
    assert len(records) == 1
    # email is column 1 (alice@example.com). "1" also points to index 1.
    assert records[0].content == "alice@example.com alice@example.com"


def test_csv_source_parse_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,email\nAlice,alice@example.com", encoding="utf-8")
    source = CSVSource(csv_file)
    import csv
    def mock_reader(*args, **kwargs):
        raise csv.Error("fake error")
    monkeypatch.setattr(csv, "reader", mock_reader)
    with pytest.raises(Exception, match="CSV parse error"):
        list(source.read_records())


def test_json_source_ijson_mock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"name": "Alice"}]', encoding="utf-8")
    
    import sys
    from types import ModuleType
    mock_ijson = ModuleType("ijson")
    def mock_items(f, prefix):
        import json
        f.seek(0)
        yield from json.load(f)
    mock_ijson.items = mock_items # type: ignore
    monkeypatch.setitem(sys.modules, "ijson", mock_ijson)
    
    source = JSONSource(json_file, settings=IngestionSettings())
    records = list(source.read_records())
    assert len(records) == 1
    assert "Alice" in records[0].content
