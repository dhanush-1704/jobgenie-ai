from fastapi import FastAPI

app = FastAPI(
    title="Career Copilot API",
    description="Backend API for Career Copilot",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Career Copilot API is running 🚀"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }