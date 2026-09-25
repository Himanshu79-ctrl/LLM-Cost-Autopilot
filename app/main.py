from fastapi import FastAPI

from app.api.generate import router as generate_router
from app.api.usage import router as usage_router
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="LLM Cost Autopilot",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(generate_router)
app.include_router(usage_router)



@app.get("/health")
async def health_check():
    return {"status": "ok"}