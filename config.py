import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def build_database_uri(database_path):
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return database_url

    return f"sqlite:///{Path(database_path).resolve().as_posix()}"


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "medscope-local-development-key")
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "data" / "medscope.db"))
    SQLALCHEMY_DATABASE_URI = build_database_uri(DATABASE_PATH)
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = Path(os.getenv("LOG_FILE", BASE_DIR / "logs" / "app.log"))
    ENV_NAME = os.getenv("FLASK_CONFIG", "development").lower()
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "1048576"))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv("SESSION_LIFETIME_SECONDS", "7200"))
    )
    TESTING = False
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DATABASE_PATH = Path(os.getenv("TEST_DATABASE_PATH", BASE_DIR / "data" / "test_medscope.db"))
    SQLALCHEMY_DATABASE_URI = build_database_uri(DATABASE_PATH)


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_SECURE = True

    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY:
            raise RuntimeError("SECRET_KEY must be set in production.")


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    config_name = os.getenv("FLASK_CONFIG", "development").lower()
    config_class = CONFIG_MAP.get(config_name, DevelopmentConfig)

    if hasattr(config_class, "validate"):
        config_class.validate()

    return config_class
