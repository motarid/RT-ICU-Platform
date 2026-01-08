from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RTICU API",
    version="1.0.0"
)

# CORS (حل جذري لمشكلة الفرونت)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقًا نحدد الدومين
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "RTICU API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/patients")
def get_patients():
    return {
        "items": [
            {
                "id": 1,
                "name": "Ahmed Ali",
                "age": 45,
                "diagnosis": "ARDS"
            }
        ],
        "total": 1
    }
