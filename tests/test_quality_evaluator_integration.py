import pytest

from app.services.quality_evaluator import (
    QualityEvaluator,
)


@pytest.mark.asyncio
async def test_real_quality_evaluation():

    evaluator = QualityEvaluator()

    result = await evaluator.evaluate(
        prompt=(
            "Explain what a REST API is "
            "and give a simple example."
        ),
        response=(
            "A REST API is an interface that "
            "allows applications to communicate "
            "over HTTP using resources and methods "
            "such as GET, POST, PUT, and DELETE. "
            "For example, GET /users can return "
            "a list of users."
        ),
    )

    print("\nQuality Result:")
    print(result)

    assert 0 <= result.score <= 10

    assert 0 <= result.relevance <= 10
    assert 0 <= result.correctness <= 10
    assert 0 <= result.completeness <= 10
    assert 0 <= result.instruction_following <= 10
    assert 0 <= result.clarity <= 10

    assert isinstance(
        result.passed,
        bool,
    )

    assert result.reason