import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "medscope-local-development-key")
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "data" / "medscope.db"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = Path(os.getenv("LOG_FILE", BASE_DIR / "logs" / "app.log"))
    TESTING = False
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DATABASE_PATH = Path(os.getenv("TEST_DATABASE_PATH", BASE_DIR / "data" / "test_medscope.db"))


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv("SECRET_KEY")

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
