from fastapi import FastAPI
@app.get("/")
def root():
    return {"ok": True, "message": "RTICU API is running. Try /health"}
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from fastapi import Request
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("rticu-api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    logger.info("%s %s -> %s (%dms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


from app.health import router as health_router
app.include_router(health_router)

from app.review_notify import router as review_notify_router

app = FastAPI(title="RTICU API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(review_notify_router)
