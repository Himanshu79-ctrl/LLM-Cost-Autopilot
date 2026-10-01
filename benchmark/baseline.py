import asyncio
import json
import time
from pathlib import Path

from app.providers.manager import ProviderManager
from app.services.cost_engine import CostEngine
from benchmark.prompts import get_test_prompts


BASELINE_MODEL = "openai/gpt-oss-20b"
BASELINE_PROVIDER = "groq"

RESULTS_DIR = Path("benchmark_results")
RESULTS_FILE = RESULTS_DIR / "baseline.jsonl"


async def run_baseline():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    prompts = get_test_prompts()
    provider_manager = ProviderManager()
    provider = provider_manager.get_provider(BASELINE_PROVIDER)

    print("=" * 70)
    print("RouteMind Baseline Benchmark")
    print("=" * 70)
    print(f"Model:   {BASELINE_MODEL}")
    print(f"Prompts: {len(prompts)}")
    print(f"Output:  {RESULTS_FILE}")
    print("=" * 70)

    with RESULTS_FILE.open("w", encoding="utf-8") as file:
        for index, item in enumerate(prompts, start=1):
            prompt_id = item["id"]
            prompt = item["prompt"]
            category = item["category"]

            print(
                f"[{index}/{len(prompts)}] "
                f"Prompt {prompt_id} ({category})...",
                end=" ",
                flush=True,
            )

            started_at = time.perf_counter()

            try:
                response = await provider.generate(
                    prompt=prompt,
                    model=BASELINE_MODEL,
                )

                elapsed_ms = (
                    time.perf_counter() - started_at
                ) * 1000

                cost_breakdown = CostEngine.calculate(
                    model_name=response.model,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                )

                result = {
                    "prompt_id": prompt_id,
                    "category": category,
                    "prompt": prompt,
                    "response": response.output,
                    "model": response.model,
                    "provider": BASELINE_PROVIDER,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "latency_ms": response.latency_ms,
                    "wall_clock_latency_ms": elapsed_ms,
                    "cost": cost_breakdown.total_cost,
                    "status": "success",
                    "error": None,
                }

                print(
                    f"OK | "
                    f"{response.input_tokens} in / "
                    f"{response.output_tokens} out | "
                    f"{response.latency_ms:.0f} ms | "
                    f"${cost_breakdown.total_cost:.8f}"
                )

            except Exception as exc:
                elapsed_ms = (
                    time.perf_counter() - started_at
                ) * 1000

                result = {
                    "prompt_id": prompt_id,
                    "category": category,
                    "prompt": prompt,
                    "response": None,
                    "model": BASELINE_MODEL,
                    "provider": BASELINE_PROVIDER,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "latency_ms": elapsed_ms,
                    "wall_clock_latency_ms": elapsed_ms,
                    "cost": 0.0,
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                }

                print(
                    f"ERROR | "
                    f"{type(exc).__name__}: {exc}"
                )

            file.write(
                json.dumps(
                    result,
                    ensure_ascii=False,
                )
                + "\n"
            )
            file.flush()

    print()
    print("=" * 70)
    print("Baseline benchmark completed.")
    print(f"Results saved to: {RESULTS_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_baseline())