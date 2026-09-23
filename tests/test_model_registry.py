import pytest

from app.router.model_registry import (
    get_model,
    get_models_by_tier,
    list_models,
)


def test_get_model():
    model = get_model("gemini-3.6-flash")

    assert model.name == "gemini-3.6-flash"
    assert model.provider == "gemini"
    assert model.tier == "powerful"


def test_get_groq_model():
    model = get_model("openai/gpt-oss-20b")

    assert model.name == "openai/gpt-oss-20b"
    assert model.provider == "groq"
    assert model.tier == "medium"


def test_list_models():
    models = list_models()

    assert len(models) == 3

    model_names = {
        model.name
        for model in models
    }

    assert "gemini-3.1-flash-lite" in model_names
    assert "openai/gpt-oss-20b" in model_names
    assert "gemini-3.6-flash" in model_names


def test_get_models_by_tier():

    powerful_models = get_models_by_tier("powerful")

    assert len(powerful_models) == 1
    assert powerful_models[0].name == "gemini-3.6-flash"


def test_medium_models():

    medium_models = get_models_by_tier("medium")

    assert len(medium_models) == 1
    assert medium_models[0].name == "openai/gpt-oss-20b"


def test_unknown_model():

    with pytest.raises(ValueError):
        get_model("does-not-exist")


def test_get_cheap_model():
    model = get_model(
        "gemini-3.1-flash-lite"
    )

    assert model.name == "gemini-3.1-flash-lite"
    assert model.provider == "gemini"
    assert model.tier == "cheap"


def test_cheap_models():
    cheap_models = get_models_by_tier("cheap")

    assert len(cheap_models) == 1

    assert (
        cheap_models[0].name
        == "gemini-3.1-flash-lite"
    )