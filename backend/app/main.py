from fastapi import FastAPI
from app.api.routes import logs

app = FastAPI(
    title="DevOps AI Copilot",
    description="AI-powered incident investigation platform",
    version="0.1.0",
)

app.include_router(logs.router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "devops-ai-copilot"
    }