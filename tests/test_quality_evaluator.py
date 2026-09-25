import pytest

from app.services.quality_evaluator import (
    QualityEvaluator,
)


def test_parse_valid_result():

    raw_output = """
    {
        "score": 8.5,
        "passed": true,
        "relevance": 9,
        "correctness": 8,
        "completeness": 8,
        "instruction_following": 9,
        "clarity": 9,
        "reason": "The response directly answers the question."
    }
    """

    result = QualityEvaluator._parse_result(
        raw_output
    )

    assert result.score == 8.5
    assert result.passed is True
    assert result.relevance == 9
    assert result.correctness == 8
    assert result.completeness == 8
    assert result.instruction_following == 9
    assert result.clarity == 9


def test_parse_failed_result():

    raw_output = """
    {
        "score": 5.5,
        "passed": false,
        "relevance": 6,
        "correctness": 5,
        "completeness": 5,
        "instruction_following": 6,
        "clarity": 6,
        "reason": "The response is incomplete."
    }
    """

    result = QualityEvaluator._parse_result(
        raw_output
    )

    assert result.score == 5.5
    assert result.passed is False


def test_invalid_json():

    with pytest.raises(RuntimeError):

        QualityEvaluator._parse_result(
            "This is not JSON."
        )


def test_missing_field():

    raw_output = """
    {
        "score": 8.5,
        "passed": true
    }
    """

    with pytest.raises(RuntimeError):

        QualityEvaluator._parse_result(
            raw_output
        )


def test_invalid_score():

    raw_output = """
    {
        "score": 15,
        "passed": true,
        "relevance": 9,
        "correctness": 9,
        "completeness": 9,
        "instruction_following": 9,
        "clarity": 9,
        "reason": "Good response."
    }
    """

    with pytest.raises(RuntimeError):

        QualityEvaluator._parse_result(
            raw_output
        )


def test_empty_prompt():

    evaluator = QualityEvaluator()

    with pytest.raises(ValueError):
        import asyncio

        asyncio.run(
            evaluator.evaluate(
                "",
                "Some response",
            )
        )


def test_empty_response():

    evaluator = QualityEvaluator()

    with pytest.raises(ValueError):
        import asyncio

        asyncio.run(
            evaluator.evaluate(
                "Explain APIs.",
                "",
            )
        )