"use client";
import * as React from "react";
import { api } from "../../lib/api";

export default function Ops() {
  const [health, setHealth] = React.useState<any>(null);
  const [err, setErr] = React.useState<string|null>(null);
  return (
    <main className="container">
      <div className="card" style={{display:"grid", gap:10}}>
        <b>فحص الاتصال بالـAPI</b>
        <div className="small">تأكد من NEXT_PUBLIC_API_BASE على Vercel.</div>
        <button className="btn btnPrimary" onClick={async ()=>{
          setErr(null);
          try{ setHealth(await api<any>("/health")); }
          catch(e:any){ setHealth(null); setErr(e?.message||"error");}
        }}>Check /health</button>
        {err && <div style={{padding:12,borderRadius:14,border:"1px solid #fecaca",background:"#fef2f2",color:"#991b1b"}}>{err}</div>}
        {health && <pre style={{margin:0,whiteSpace:"pre-wrap"}}>{JSON.stringify(health,null,2)}</pre>}
      </div>
    </main>
  );
}
