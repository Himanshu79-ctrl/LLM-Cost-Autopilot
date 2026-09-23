import pytest

from app.router.router import LLMRouter


@pytest.fixture
def router():
    return LLMRouter()


def test_low_complexity_query(router):
    decision = router.route("Hello")

    assert decision.complexity == "low"

    assert (
        decision.model.name
        == "gemini-3.1-flash-lite"
    )

    assert decision.model.tier == "cheap"


def test_medium_complexity_query(router):

    decision = router.route(
        "Explain Django REST API."
    )

    assert decision.complexity == "medium"
    assert decision.model.name == "openai/gpt-oss-20b"


def test_high_complexity_query(router):

    decision = router.route(
        """
        Design a distributed scalable payment
        system with database consistency,
        fault tolerance, retries, idempotency,
        architecture and optimization.
        """
    )

    assert decision.complexity == "high"
    assert decision.model.name == "gemini-3.6-flash"


def test_empty_prompt(router):

    with pytest.raises(ValueError):
        router.route("")