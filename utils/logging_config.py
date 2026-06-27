import logging
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    app.logger.setLevel(log_level)

    log_file = app.config["LOG_FILE"]
    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    if not any(isinstance(handler, RotatingFileHandler) for handler in app.logger.handlers):
        app.logger.addHandler(file_handler)

    app.logger.info("Application logging configured")
