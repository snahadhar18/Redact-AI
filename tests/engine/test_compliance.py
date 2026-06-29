from redactai.engine.compliance.engine import ComplianceAnalyzer
from redactai.engine.detectors.base import Match


def test_compliance_analyzer_critical() -> None:
    analyzer = ComplianceAnalyzer()
    match = Match(start=0, end=10, value="secret", label="AWS_KEY", severity="CRITICAL")
    report = analyzer.analyze([match])
    
    assert report.total_findings == 1
    assert "SOC2" in report.regulations_triggered
    assert report.critical_findings == 1
    assert report.high_findings == 0
    assert len(report.findings) == 1
    
    finding = report.findings[0]
    assert finding.match == match
    assert "Rotate credential immediately" in finding.remediation
    
    # Test serialization
    data = report.to_dict()
    assert data["total_findings"] == 1
    assert data["critical_findings"] == 1
    assert data["findings"][0]["severity"] == "CRITICAL"


def test_compliance_analyzer_high() -> None:
    analyzer = ComplianceAnalyzer()
    match = Match(start=0, end=10, value="ssn", label="SSN", severity="HIGH")
    report = analyzer.analyze([match])
    
    assert report.total_findings == 1
    assert "HIPAA" in report.regulations_triggered
    assert report.high_findings == 1
    
    finding = report.findings[0]
    assert "Rotate credential immediately" in finding.remediation


def test_compliance_analyzer_pci() -> None:
    analyzer = ComplianceAnalyzer()
    match = Match(start=0, end=16, value="4111222233334444", label="CREDIT_CARD", severity="HIGH")
    report = analyzer.analyze([match])
    
    assert "PCI DSS" in report.regulations_triggered
    assert "vaulted or tokenized" in report.findings[0].remediation
