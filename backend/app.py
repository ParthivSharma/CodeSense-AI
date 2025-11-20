from fastapi import FastAPI
from backend.routers import analyze

app = FastAPI(title="CodeSense AI Backend")

# Attach routers
app.include_router(analyze.router)

@app.get("/")
def home():
    return {"status": "ok", "message": "CodeSense AI Backend Running"}
