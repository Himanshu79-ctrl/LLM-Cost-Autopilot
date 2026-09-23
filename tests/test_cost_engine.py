import pytest

from app.services.cost_engine import CostEngine


def test_cost_calculation():

    result = CostEngine.calculate(
        model_name="gemini-3.6-flash",
        input_tokens=10_000,
        output_tokens=2_000,
    )

    assert result.model == "gemini-3.6-flash"

    assert result.input_tokens == 10_000
    assert result.output_tokens == 2_000

    assert result.input_cost == pytest.approx(0.0075)
    assert result.output_cost == pytest.approx(0.0075)
    assert result.total_cost == pytest.approx(0.015)


def test_zero_tokens():

    result = CostEngine.calculate(
        model_name="gemini-3.6-flash",
        input_tokens=0,
        output_tokens=0,
    )

    assert result.total_cost == 0.0


def test_negative_input_tokens():

    with pytest.raises(ValueError):
        CostEngine.calculate(
            model_name="gemini-3.6-flash",
            input_tokens=-1,
            output_tokens=10,
        )


def test_negative_output_tokens():

    with pytest.raises(ValueError):
        CostEngine.calculate(
            model_name="gemini-3.6-flash",
            input_tokens=10,
            output_tokens=-1,
        )


def test_unknown_model():

    with pytest.raises(ValueError):
        CostEngine.calculate(
            model_name="unknown-model",
            input_tokens=100,
            output_tokens=100,
        )