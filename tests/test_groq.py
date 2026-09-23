import asyncio

from app.providers.groq_provider import GroqProvider


async def main():

    provider = GroqProvider()

    response = await provider.generate(
        "Explain what an API is in simple terms."
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