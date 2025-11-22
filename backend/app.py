from fastapi import FastAPI
from backend.routers import analyze, metrics_router, auth_router

app = FastAPI(title="CodeSense AI Backend")

# Attach routers
app.include_router(analyze.router)
app.include_router(metrics_router.router)
app.include_router(auth_router.router)

@app.get("/")
def home():
    return {"status": "ok", "message": "CodeSense AI Backend Running"}
