from __future__ import annotations
import time, json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from .db import conn

router = APIRouter(prefix="/review/notify", tags=["review-notify"])
Period = Literal["daily","weekly"]

class EnqueueReq(BaseModel):
    period: Period = "weekly"
    dept: Optional[str] = None

def ensure_tables():
    with conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS outbox_events (
          id BIGSERIAL PRIMARY KEY,
          event_type TEXT NOT NULL,
          dept TEXT NOT NULL,
          payload JSONB NOT NULL DEFAULT '{}'::jsonb,
          status TEXT NOT NULL DEFAULT 'pending',
          attempts INT NOT NULL DEFAULT 0,
          max_attempts INT NOT NULL DEFAULT 10,
          available_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
          created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS review_notifications (
          id BIGSERIAL PRIMARY KEY,
          dept TEXT NOT NULL,
          period TEXT NOT NULL,
          created_at BIGINT NOT NULL,
          subject TEXT NOT NULL,
          body_txt TEXT NOT NULL,
          body_html TEXT NOT NULL,
          metrics JSONB NOT NULL DEFAULT '{}'::jsonb
        );
        """)

@router.post("/enqueue")
def enqueue(req: EnqueueReq):
    ensure_tables()
    dept = req.dept or "ICU"
    with conn() as c:
        c.execute(
            """INSERT INTO outbox_events(event_type, dept, payload)
               VALUES(%s,%s,%s::jsonb) RETURNING id""",
            ("review_digest", dept, json.dumps({"dept": dept, "period": req.period})),
        )
        row = c.fetchone()
    return {"ok": True, "event_id": row["id"], "dept": dept, "period": req.period}

@router.get("/latest")
def latest(period: str = "weekly", dept: str = "ICU"):
    ensure_tables()
    with conn() as c:
        c.execute(
            """SELECT dept, period, created_at, subject, body_txt, body_html, metrics
               FROM review_notifications
               WHERE dept=%s AND period=%s
               ORDER BY created_at DESC
               LIMIT 1""",
            (dept, period),
        )
        row = c.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="no_digest")
    return {"ok": True, **row}
