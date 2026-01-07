from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS CONFIG (هذا هو الحل الجذري)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقاً يمكن تقييده
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Dummy in-memory DB (مثال) =====
patients_db = [
    {
        "id": 33,
        "name": "Ahmed Ali",
        "age": 45,
        "diagnosis": "ARDS"
    },
    {
        "id": 34,
        "name": "Ahmed Ali",
        "age": 45,
        "diagnosis": "ARDS"
    }
]

@app.get("/")
def root():
    return {"status": "RT-ICU API running"}

@app.get("/patients")
def get_patients():
    return {
        "items": patients_db,
        "total": len(patients_db),
        "page": 1,
        "page_size": 10,
        "pages": 1
    }
