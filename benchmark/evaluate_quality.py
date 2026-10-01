import asyncio
import json
from pathlib import Path

from app.services.quality_evaluator import QualityEvaluator


RESULTS_DIR = Path("benchmark_results")

BASELINE_FILE = RESULTS_DIR / "baseline.jsonl"
ROUTEMIND_FILE = RESULTS_DIR / "routemind.jsonl"

BASELINE_OUTPUT = RESULTS_DIR / "baseline_quality.jsonl"
ROUTEMIND_OUTPUT = RESULTS_DIR / "routemind_quality.jsonl"


async def evaluate_file(input_file: Path, output_file: Path):
    evaluator = QualityEvaluator()

    with (
        input_file.open("r", encoding="utf-8") as source,
        output_file.open("w", encoding="utf-8") as target,
    ):
        for line in source:
            record = json.loads(line)

            if record["status"] != "success" or not record.get("response"):
                record["quality_status"] = "skipped"
                record["quality_error"] = record.get("error")

                target.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )
                continue

            try:
                quality = await evaluator.evaluate(
                    prompt=record["prompt"],
                    response=record["response"],
                )

                record["quality_score"] = quality.score
                record["quality_passed"] = quality.passed

                record["quality_relevance"] = quality.relevance
                record["quality_correctness"] = quality.correctness
                record["quality_completeness"] = quality.completeness
                record["quality_instruction_following"] = (
                    quality.instruction_following
                )
                record["quality_clarity"] = quality.clarity

                record["quality_reason"] = quality.reason

                record["quality_status"] = "success"
                record["quality_error"] = None

                print(
                    f"{input_file.name} | "
                    f"Prompt {record['prompt_id']} | "
                    f"Quality: {quality.score:.2f}"
                )

            except Exception as exc:
                record["quality_status"] = "error"
                record["quality_error"] = (
                    f"{type(exc).__name__}: {exc}"
                )

                print(
                    f"{input_file.name} | "
                    f"Prompt {record['prompt_id']} | "
                    f"ERROR: {type(exc).__name__}: {exc}"
                )

            target.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )
            target.flush()


async def main():
    await evaluate_file(
        BASELINE_FILE,
        BASELINE_OUTPUT,
    )

    await evaluate_file(
        ROUTEMIND_FILE,
        ROUTEMIND_OUTPUT,
    )

    print()
    print("=" * 70)
    print("Quality evaluation completed.")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())