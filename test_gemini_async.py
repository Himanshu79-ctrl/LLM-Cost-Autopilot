import asyncio

from google import genai

from app.core.config import settings


async def main():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    response = await client.aio.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say hello in one sentence.",
    )

    print(response.text)


asyncio.run(main())