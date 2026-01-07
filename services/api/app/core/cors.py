import os

def get_allowed_origins():
    # يمكنك وضعها في Render ENV: CORS_ORIGINS=http://localhost:5173,https://xxx.onrender.com
    raw = os.getenv("CORS_ORIGINS", "*").strip()
    if raw == "*" or raw == "":
        return ["*"]
    return [x.strip() for x in raw.split(",") if x.strip()]
