# Local Development

## API
cd services/api
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
set DATABASE_URL=postgresql://...
uvicorn app.main:app --reload

## Worker
cd services/worker
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set DATABASE_URL=postgresql://...
python -m worker.main

## Web
cd apps/web
npm i
set NEXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
