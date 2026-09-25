from pydantic import BaseModel, Field

from datetime import datetime
class GenerateRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        description="Prompt to send to the LLM.",
    )


class GenerateResponse(BaseModel):
    output: str

    model: str
    provider: str

    complexity: str
    complexity_score: int

    input_tokens: int
    output_tokens: int

    latency_ms: float
    cost: float

    quality_score: float | None
    quality_passed: bool | None
    quality_reason: str


class UsageSummaryResponse(BaseModel):
    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    total_cost: float
    average_latency_ms: float


class ProviderUsageResponse(BaseModel):
    provider: str
    requests: int
    cost: float
    input_tokens: int
    output_tokens: int


class ModelUsageResponse(BaseModel):
    model: str
    requests: int
    cost: float


class ComplexityUsageResponse(BaseModel):
    complexity: str
    requests: int

class RequestHistoryResponse(BaseModel):
    id: int
    created_at: datetime

    complexity_level: str
    complexity_score: int

    selected_model: str
    selected_provider: str

    input_tokens: int
    output_tokens: int

    latency_ms: float
    cost: float

    error_type: str | None
    error_message: str | None