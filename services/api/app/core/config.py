from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RT-ICU API"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite:///./rticu.db"  # للتطوير المحلي
    # في Render/Neon ستضع DATABASE_URL في Environment Variables

    # CORS
    CORS_ALLOW_ORIGINS: str = "*"  # ابدأ بـ * ثم قيّدها لاحقًا

settings = Settings()
