import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey-change-me")

    # Session cookie hardening
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    SESSION_PERMANENT = False
