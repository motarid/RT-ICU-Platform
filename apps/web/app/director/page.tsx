"use client";
import * as React from "react";
import { api } from "../../lib/api";

type Digest = { ok: boolean; subject: string; body_txt: string; created_at: number };

export default function Director() {
  const [digest, setDigest] = React.useState<Digest|null>(null);
  const [msg, setMsg] = React.useState<string|null>(null);

  async function refresh() {
    setMsg(null);
    try { setDigest(await api<Digest>("/review/notify/latest?period=weekly&dept=ICU")); }
    catch { setDigest(null); }
  }
  async function generate() {
    setMsg(null);
    try {
      await api<any>("/review/notify/enqueue", { method:"POST", body: JSON.stringify({ period:"weekly", dept:"ICU" }) });
      setMsg("تمت جدولة الملخص. انتظر 30-60 ثانية ثم اضغط Refresh.");
    } catch {
      setMsg("فشل جدولة الملخص. تحقق من API/DB/Worker.");
    }
  }
  React.useEffect(()=>{ refresh(); }, []);

  return (
    <main className="container">
      <div className="card" style={{display:"grid", gap:10}}>
        <b>📨 Review Digest</b>
        <div style={{display:"flex", gap:10, flexWrap:"wrap"}}>
          <button className="btn" onClick={refresh}>Refresh</button>
          <button className="btn btnPrimary" onClick={generate}>Generate</button>
        </div>
        {msg && <div className="small">{msg}</div>}
        {!digest && <div className="small">لا يوجد ملخص بعد.</div>}
        {digest && (
          <>
            <div><b>{digest.subject}</b></div>
            <div className="small">Created: {new Date((digest.created_at||0)*1000).toLocaleString()}</div>
            <pre style={{whiteSpace:"pre-wrap", margin:0}}>{digest.body_txt}</pre>
          </>
        )}
      </div>
    </main>
  );
}
