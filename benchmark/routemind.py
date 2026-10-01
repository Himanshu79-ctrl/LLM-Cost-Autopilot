import asyncio
import json
import os
import time
from pathlib import Path

import httpx

from benchmark.prompts import get_test_prompts


BASE_URL = os.getenv("ROUTEMIND_BASE_URL", "http://127.0.0.1:8000")
EMAIL = os.getenv("ROUTEMIND_EMAIL")
PASSWORD = os.getenv("ROUTEMIND_PASSWORD")

RESULTS_DIR = Path("benchmark_results")
RESULTS_FILE = RESULTS_DIR / "routemind.jsonl"


async def login(client: httpx.AsyncClient) -> str:
    if not EMAIL or not PASSWORD:
        raise RuntimeError(
            "ROUTEMIND_EMAIL and ROUTEMIND_PASSWORD environment "
            "variables must be configured."
        )

    response = await client.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD,
        },
    )

    response.raise_for_status()

    data = response.json()

    return data["access_token"]


async def run_routemind():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    prompts = get_test_prompts()

    async with httpx.AsyncClient(timeout=120.0) as client:

        print("=" * 70)
        print("RouteMind Benchmark")
        print("=" * 70)
        print(f"API:     {BASE_URL}")
        print(f"Prompts: {len(prompts)}")
        print(f"Output:  {RESULTS_FILE}")
        print("=" * 70)

        print("\nLogging in...")

        token = await login(client)

        print("Login successful.\n")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        with RESULTS_FILE.open("w", encoding="utf-8") as file:

            for index, item in enumerate(prompts, start=1):

                prompt_id = item["id"]
                category = item["category"]
                prompt = item["prompt"]

                print(
                    f"[{index}/{len(prompts)}] "
                    f"Prompt {prompt_id} ({category})...",
                    end=" ",
                    flush=True,
                )

                started_at = time.perf_counter()

                try:

                    response = await client.post(
                        f"{BASE_URL}/api/generate",
                        headers=headers,
                        json={
                            "prompt": prompt,
                        },
                    )

                    elapsed_ms = (
                        time.perf_counter() - started_at
                    ) * 1000

                    response.raise_for_status()

                    data = response.json()

                    result = {
                        "prompt_id": prompt_id,
                        "category": category,

                        # Important:
                        # Save the exact prompt and generated response
                        # for later quality evaluation.
                        "prompt": prompt,
                        "response": data["output"],

                        "model": data["model"],
                        "provider": data["provider"],

                        "complexity": data["complexity"],
                        "complexity_score": data["complexity_score"],

                        "input_tokens": data["input_tokens"],
                        "output_tokens": data["output_tokens"],

                        "latency_ms": data["latency_ms"],
                        "wall_clock_latency_ms": elapsed_ms,

                        "cost": data["cost"],

                        "quality_score": data.get("quality_score"),
                        "quality_passed": data.get("quality_passed"),
                        "quality_reason": data.get("quality_reason"),

                        "status": "success",
                        "error": None,
                    }

                    print(
                        f"OK | "
                        f"{data['model']} | "
                        f"{data['complexity']} | "
                        f"{data['input_tokens']} in / "
                        f"{data['output_tokens']} out | "
                        f"{data['latency_ms']:.0f} ms | "
                        f"${data['cost']:.8f}"
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

                        "model": None,
                        "provider": None,

                        "complexity": None,
                        "complexity_score": None,

                        "input_tokens": 0,
                        "output_tokens": 0,

                        "latency_ms": elapsed_ms,
                        "wall_clock_latency_ms": elapsed_ms,

                        "cost": 0.0,

                        "quality_score": None,
                        "quality_passed": None,
                        "quality_reason": None,

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
    print("RouteMind benchmark completed.")
    print(f"Results saved to: {RESULTS_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_routemind())