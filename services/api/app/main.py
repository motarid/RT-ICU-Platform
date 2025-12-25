from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ... imports routers ...

app = FastAPI(title="RTICU API", version="1.0.0")

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"service": "rticu-api", "status": "running", "docs": "/docs", "health": "/health"}
