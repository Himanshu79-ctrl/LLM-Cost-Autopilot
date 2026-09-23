import pytest

from app.router.complexity_analyzer import (
    ComplexityAnalyzer,
)


@pytest.fixture
def analyzer():
    return ComplexityAnalyzer()


def test_simple_query(analyzer):

    result = analyzer.analyze(
        "Hello"
    )

    assert result.level == "low"
    assert result.score <= 2


def test_technical_query(analyzer):

    result = analyzer.analyze(
        "Explain Django REST API."
    )

    assert result.level == "medium"
    assert result.score >= 3


def test_complex_query(analyzer):

    result = analyzer.analyze(
        """
        Design a distributed scalable payment
        system with database consistency,
        fault tolerance, retries, idempotency,
        architecture and optimization.
        """
    )

    print("\nSCORE:", result.score)
    print("FEATURES:", result.features)
    print("REASONS:", result.reasons)

    assert result.level == "high"
    assert result.score >= 10


def test_empty_prompt(analyzer):

    with pytest.raises(ValueError):
        analyzer.analyze("")