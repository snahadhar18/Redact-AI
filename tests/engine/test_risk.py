from redactai.engine.detectors.base import Match
from redactai.engine.risk.engine import RiskScorer


def test_risk_scorer_safe() -> None:
    scorer = RiskScorer()
    assessment = scorer.evaluate([])
    
    assert assessment.score == 0.0
    assert assessment.risk_level == "SAFE"
    assert "No sensitive data" in assessment.factors[0]
    
    data = assessment.to_dict()
    assert data["score"] == 0.0
    assert data["risk_level"] == "SAFE"


def test_risk_scorer_critical() -> None:
    scorer = RiskScorer()
    match = Match(
        start=0, end=10, value="secret", label="AWS_KEY", severity="CRITICAL", confidence=1.0
    )
    assessment = scorer.evaluate([match])
    
    # CRITICAL weight is 85.0 * 1.0 confidence = 85.0
    assert assessment.score >= 85.0
    assert assessment.risk_level == "CRITICAL"
    assert "CRITICAL findings" in assessment.factors[0]


def test_risk_scorer_high() -> None:
    scorer = RiskScorer()
    match = Match(start=0, end=10, value="ssn", label="SSN", severity="HIGH", confidence=1.0)
    match2 = Match(start=10, end=20, value="email", label="EMAIL", severity="LOW", confidence=1.0)
    assessment = scorer.evaluate([match, match2])
    
    # HIGH weight is 40.0, LOW is 5.0 -> total 45.0
    assert assessment.score == 45.0
    assert assessment.risk_level == "MEDIUM"  # 30-59 is MEDIUM, wait, HIGH is 60+
    assert any("HIGH severity" in f for f in assessment.factors)


def test_risk_scorer_capped_at_100() -> None:
    scorer = RiskScorer()
    match1 = Match(
        start=0, end=10, value="secret", label="AWS_KEY", severity="CRITICAL", confidence=1.0
    )
    match2 = Match(
        start=10, end=20, value="secret2", label="AWS_KEY", severity="CRITICAL", confidence=1.0
    )
    assessment = scorer.evaluate([match1, match2])
    
    # Should cap at 100.0 instead of 170.0
    assert assessment.score == 100.0
    assert assessment.risk_level == "CRITICAL"
