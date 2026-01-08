from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# إذا عندك راوترات في مشروعك (اختياري)
# from app.api.router import api_router

app = FastAPI(title="RTICU API")

# ✅ CORS (مهم جداً)
allowed_origins = [
    "http://localhost:5173",     # Vite local
    "http://127.0.0.1:5173",
    # ضع رابط Vercel/Production هنا لاحقاً مثل:
    # "https://your-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# إذا عندك راوترات فعّلها:
# app.include_router(api_router)

# ملاحظة: إذا لديك code يستورد:
# from app.db.session import engine
# الآن سيعمل لأننا أنشأنا session.py + __init__.py
