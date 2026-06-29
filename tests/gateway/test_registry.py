import pytest

from redactai.gateway.core.detector import DetectorProtocol, NullDetector
from redactai.gateway.core.registry import DetectorRegistry


def test_registry_register_and_create() -> None:
    reg = DetectorRegistry()
    
    def my_factory() -> DetectorProtocol:
        return NullDetector()
        
    reg.register("null_test", my_factory)
    assert "null_test" in reg
    assert "null_test" in reg.names()
    
    detector = reg.create("null_test")
    assert isinstance(detector, NullDetector)


def test_registry_replace() -> None:
    reg = DetectorRegistry()
    reg.register("null_test", lambda: NullDetector())
    
    # Should replace without error
    reg.register("null_test", lambda: NullDetector(), replace=True)


def test_registry_unregister() -> None:
    reg = DetectorRegistry()
    reg.register("null", lambda: NullDetector())
    reg.unregister("null")
    assert "null" not in reg


def test_registry_create_many_and_all() -> None:
    reg = DetectorRegistry()
    reg.register("one", lambda: NullDetector())
    reg.register("two", lambda: NullDetector())
    
    detectors = reg.create_many(["one", "two"])
    assert len(detectors) == 2
    
    all_detectors = reg.create_all()
    assert len(all_detectors) == 2


def test_registry_duplicate_register() -> None:
    from redactai.gateway.core.exceptions import DetectorError
    reg = DetectorRegistry()
    reg.register("null", lambda: NullDetector())
    with pytest.raises(DetectorError, match="already registered"):
        reg.register("null", lambda: NullDetector())


def test_registry_unknown_create() -> None:
    from redactai.gateway.core.exceptions import DetectorError
    reg = DetectorRegistry()
    with pytest.raises(DetectorError, match="unknown detector"):
        reg.create("nonexistent")


def test_registry_invalid_factory() -> None:
    from redactai.gateway.core.exceptions import DetectorError
    reg = DetectorRegistry()
    reg.register("bad", lambda: "not a detector") # type: ignore
    with pytest.raises(DetectorError, match="returned an object without a detect"):
        reg.create("bad")


def test_registry_load_entry_points(monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.metadata
    
    class MockEntryPoint:
        def __init__(self, name: str, factory):
            self.name = name
            self._factory = factory
        def load(self):
            if self._factory is None:
                raise Exception("Broken plugin")
            return self._factory
            
    def mock_eps(group: str):
        return [
            MockEntryPoint("ep1", lambda: NullDetector()),
            MockEntryPoint("ep_broken", None)
        ]
        
    monkeypatch.setattr(importlib.metadata, "entry_points", mock_eps)
    
    reg = DetectorRegistry()
    loaded = reg.load_entry_points()
    assert loaded == 1
    assert "ep1" in reg
    assert "ep_broken" not in reg
