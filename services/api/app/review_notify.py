from fastapi import APIRouter
from pydantic import BaseModel

# إذا كان لديك DB لاحقًا، سنفعلها داخل الدالة فقط حتى لا ينهار التشغيل عند import
# from app.db import conn

router = APIRouter(prefix="/review", tags=["review"])

class ReviewNotifyRequest(BaseModel):
    dept: str
    period: str

@router.post("/notify")
def review_notify(req: ReviewNotifyRequest):
    # مثال: من دون DB الآن (لتشغيل الخدمة بشكل مضمون)
    return {"ok": True, "dept": req.dept, "period": req.period}
