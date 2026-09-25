import json
from dataclasses import dataclass

from app.providers.manager import ProviderManager


@dataclass(frozen=True)
class QualityResult:
    score: float
    passed: bool

    relevance: float
    correctness: float
    completeness: float
    instruction_following: float
    clarity: float

    reason: str


class QualityEvaluator:

    JUDGE_MODEL = "openai/gpt-oss-20b"
    PASS_THRESHOLD = 7.0

    def __init__(self):
        self.provider_manager = ProviderManager()

    async def evaluate(
        self,
        prompt: str,
        response: str,
    ) -> QualityResult:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        if not response or not response.strip():
            raise ValueError(
                "Response cannot be empty."
            )

        judge_provider = self.provider_manager.get_provider(
            "groq"
        )

        judge_prompt = self._build_judge_prompt(
            prompt=prompt,
            response=response,
        )

        judge_response = await judge_provider.generate(
            prompt=judge_prompt,
            model=self.JUDGE_MODEL,
        )

        return self._parse_result(
            judge_response.output
        )

    @staticmethod
    def _build_judge_prompt(
        prompt: str,
        response: str,
    ) -> str:

        return f"""
You are an objective LLM response quality evaluator.

Evaluate the generated response against the user's original prompt.

Evaluate these five dimensions:

1. relevance
   Does the response directly address the user's request?

2. correctness
   Is the response technically and factually reasonable?

3. completeness
   Does it cover the important parts required by the prompt?

4. instruction_following
   Does it follow explicit instructions and constraints?

5. clarity
   Is the response clear, understandable, and well structured?

Give each dimension a score from 0 to 10.

Then calculate an overall score from 0 to 10.

A response passes if the overall score is 7.0 or higher.

Return ONLY valid JSON.
Do not use markdown.
Do not include additional text.

Required JSON format:

{{
  "score": 0.0,
  "passed": true,
  "relevance": 0.0,
  "correctness": 0.0,
  "completeness": 0.0,
  "instruction_following": 0.0,
  "clarity": 0.0,
  "reason": "Brief explanation of the evaluation."
}}

USER PROMPT:
{prompt}

GENERATED RESPONSE:
{response}
""".strip()

    @staticmethod
    def _parse_result(
        raw_output: str,
    ) -> QualityResult:

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "LLM judge returned invalid JSON."
            ) from exc

        required_fields = {
            "score",
            "passed",
            "relevance",
            "correctness",
            "completeness",
            "instruction_following",
            "clarity",
            "reason",
        }

        missing_fields = (
            required_fields - data.keys()
        )

        if missing_fields:
            raise RuntimeError(
                "LLM judge response is missing fields: "
                + ", ".join(sorted(missing_fields))
            )

        score = float(data["score"])

        if not 0 <= score <= 10:
            raise RuntimeError(
                "LLM judge returned an invalid score."
            )

        passed = score >= QualityEvaluator.PASS_THRESHOLD

        return QualityResult(
            score=score,
            passed=passed,
            relevance=float(data["relevance"]),
            correctness=float(data["correctness"]),
            completeness=float(data["completeness"]),
            instruction_following=float(
                data["instruction_following"]
            ),
            clarity=float(data["clarity"]),
            reason=str(data["reason"]),
        )