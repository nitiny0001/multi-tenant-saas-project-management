from fastapi import FastAPI

app = FastAPI(
    title="SaaS Project Management API",
    description="Multi-tenant project management platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to SaaS Project Management API"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }