"""redactai: stream text/log files and redact sensitive information."""

import warnings

from redactai.engine.detectors.base import Detector, Match, RegexDetector

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    from redactai.engine.scrubber.engine import RedactionEngine

__all__ = ["Detector", "Match", "RegexDetector", "RedactionEngine", "__version__"]
__version__ = "0.1.0"
