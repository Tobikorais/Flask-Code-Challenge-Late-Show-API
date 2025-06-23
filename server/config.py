import os

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "postgresql://username@localhost:5432/late_show_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expires in 1 hour
    
    # Application Configuration
    DEBUG = os.environ.get("FLASK_DEBUG", False)
    TESTING = os.environ.get("FLASK_TESTING", False)

    # Rate Limiting Configuration
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_IN_MEMORY_FALLBACK_ENABLED = True 