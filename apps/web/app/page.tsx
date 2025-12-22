import Link from "next/link";

export default function Home() {
  return (
    <main className="container">
      <section className="hero">
        <div style={{display:"grid", gap:10}}>
          <div className="pill">PHI-safe • Audit-ready • Dept-scoped</div>
          <h1 style={{margin:0, fontSize:34, lineHeight:1.2}}>منصة RTICU الذكية للعلاج التنفسي</h1>
          <p style={{margin:0, maxWidth:900, opacity:0.92}}>
            Skeleton نظيف وجاهز للنشر: API + Worker + Digest + واجهة رسمية.
          </p>
          <div style={{display:"flex", gap:10, flexWrap:"wrap"}}>
            <Link className="btn btnPrimary" href="/director">لوحة المدير</Link>
            <Link className="btn" href="/ops">تشغيل/فحص</Link>
          </div>
        </div>
      </section>

      <div className="grid grid3" style={{marginTop:14}}>
        <div className="card"><b>Decision Workspace</b><div className="small">قابل للتوسع</div></div>
        <div className="card"><b>Review Queue</b><div className="small">Outbox + Worker</div></div>
        <div className="card"><b>Director Analytics</b><div className="small">Digest Endpoint</div></div>
      </div>
    </main>
  );
}
