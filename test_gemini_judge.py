import asyncio

from google import genai

from app.core.config import settings


async def main():

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    response = await client.aio.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Rate this answer from 0 to 10: REST API is an API that uses HTTP methods like GET and POST.",
    )

    print(response.text)


asyncio.run(main())