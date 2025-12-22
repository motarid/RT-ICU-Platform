# RTICU Platform (Clean Skeleton)

This is a clean, deployment-ready monorepo skeleton with:
- Frontend: Next.js (apps/web)
- Backend API: FastAPI (services/api)
- Worker: background processor (services/worker)
- Postgres: via DATABASE_URL

## Free Deploy
- Frontend: Vercel (Root Directory: apps/web)
- API: Render Web Service (Root Directory: services/api)
- Worker: Render Background Worker (Root Directory: services/worker)
- DB: Neon (DATABASE_URL)

## Python version (important)
Pins Python 3.11 via runtime.txt in API + Worker to avoid pydantic-core build issues on 3.13.

## Local dev
See docs/LOCAL_DEV.md
