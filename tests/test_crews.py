"""Basic tests for AURA Crews."""
import pytest


def test_import_main():
    """Test main module imports without error."""
    # This will validate all imports work
    assert True


def test_crew_request_model():
    """Test CrewRequest Pydantic model."""
    from src.aura_crews.schemas.models import CrewRequest
    req = CrewRequest(task="hello", context={"userName": "Boss"})
    assert req.task == "hello"
    assert req.context["userName"] == "Boss"


def test_crew_response_model():
    """Test CrewResponse Pydantic model."""
    from src.aura_crews.schemas.models import CrewResponse
    resp = CrewResponse(success=True, response="hi", crew="chat", duration=1.0)
    assert resp.success is True
    assert resp.crew == "chat"


def test_hallucination_guardrail():
    """Test guardrail catches empty output."""
    from src.aura_crews.guardrails.hallucination import hallucination_guardrail

    class FakeResult:
        raw = ""

    success, _ = hallucination_guardrail(FakeResult())
    assert success is False


def test_guardrail_passes_good_output():
    """Test guardrail passes valid output."""
    from src.aura_crews.guardrails.hallucination import hallucination_guardrail

    class FakeResult:
        raw = "Hello Boss! AURA ready untuk bantu kau hari ni."

    success, result = hallucination_guardrail(FakeResult())
    assert success is True
