from __future__ import annotations
import time, json
from datetime import datetime, timezone
from .db import conn

POLL_SECONDS = 2

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

def claim_one():
    with conn() as c:
        c.execute("""
        SELECT id, event_type, dept, payload
        FROM outbox_events
        WHERE status='pending'
        ORDER BY created_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED
        """)
        row = c.fetchone()
        if not row:
            return None
        c.execute("UPDATE outbox_events SET status='processing' WHERE id=%s", (row["id"],))
        return row

def mark_done(event_id: int):
    with conn() as c:
        c.execute("UPDATE outbox_events SET status='done' WHERE id=%s", (event_id,))

def write_digest(dept: str, period: str):
    now = datetime.now(timezone.utc)
    subject = f"RTICU Review Digest — {dept} — {period.upper()} — {now.date().isoformat()}"
    metrics = {"in_review": 0, "overdue": 0, "unassigned": 0, "oldest": []}
    ar = [
        "ملخص المراجعات (PHI-safe)",
        f"القسم: {dept}",
        f"الفترة: {period}",
        "",
        f"- قيد المراجعة: {metrics['in_review']}",
        f"- متأخرة (Overdue): {metrics['overdue']}",
        f"- غير مُعيّنة: {metrics['unassigned']}",
        "",
        "ملاحظة: لا يحتوي هذا الملخص أي بيانات تعريفية للمريض (PHI).",
    ]
    en = [
        "Review Digest (PHI-safe)",
        f"Dept: {dept}",
        f"Period: {period}",
        "",
        f"- In review: {metrics['in_review']}",
        f"- Overdue: {metrics['overdue']}",
        f"- Unassigned: {metrics['unassigned']}",
        "",
        "Note: This digest contains no PHI.",
    ]
    body_txt = "\n".join(ar) + "\n\n" + "\n".join(en) + "\n"
    body_html = "<pre>" + body_txt + "</pre>"
    with conn() as c:
        c.execute(
            """INSERT INTO review_notifications(dept, period, created_at, subject, body_txt, body_html, metrics)
                 VALUES(%s,%s,%s,%s,%s,%s,%s::jsonb)""",
            (dept, period, int(time.time()), subject, body_txt, body_html, json.dumps(metrics, ensure_ascii=False))
        )

def main():
    ensure_tables()
    print("[worker] started")
    while True:
        evt = claim_one()
        if not evt:
            time.sleep(POLL_SECONDS)
            continue
        try:
            if evt["event_type"] == "review_digest":
                payload = evt["payload"] or {}
                dept = payload.get("dept") or evt["dept"] or "ICU"
                period = payload.get("period") or "weekly"
                write_digest(dept, period)
            mark_done(evt["id"])
        except Exception as e:
            print("[worker] error:", e)
            mark_done(evt["id"])

if __name__ == "__main__":
    main()
