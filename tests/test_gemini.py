import asyncio

from app.providers.gemini_provider import GeminiProvider


async def main():
    provider = GeminiProvider()

    response = await provider.generate(
        "Explain what an API is in two simple sentences."
    )

    print("\n--- RESPONSE ---")
    print(response.output)

    print("\n--- METADATA ---")
    print("Model:", response.model)
    print("Input tokens:", response.input_tokens)
    print("Output tokens:", response.output_tokens)
    print("Latency:", response.latency_ms)
    print("Cost:", response.cost)


if __name__ == "__main__":
    asyncio.run(main())