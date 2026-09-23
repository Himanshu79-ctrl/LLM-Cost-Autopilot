from fastapi import FastAPI

from app.api.generate import router as generate_router
from app.api.usage import router as usage_router

app = FastAPI(
    title="LLM Cost Autopilot",
    version="0.1.0",
)


app.include_router(generate_router)
app.include_router(usage_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}