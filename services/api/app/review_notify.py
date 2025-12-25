import logging
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("rticu-api")

router = APIRouter(prefix="/review", tags=["review"])


class ReviewNotifyRequest(BaseModel):
    dept: str
    period: str


@router.post("/notify")
def review_notify(req: ReviewNotifyRequest):
    # لاحقًا: هنا تضع منطق DB/Queue. الآن نجعله بسيط ومستقر للتشغيل.
    logger.info("review_notify received", extra={"dept": req.dept, "period": req.period})
    return {"ok": True, "dept": req.dept, "period": req.period}
