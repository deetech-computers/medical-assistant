from flask import Flask, request

from config import get_config
from errors.handlers import register_error_handlers
from routes.api_routes import api_routes
from routes.admin_routes import admin_routes
from routes.auth_routes import auth_routes
from routes.main_routes import main_routes
from services.activity_service import record_activity
from services.database_service import init_database
from utils.logging_config import configure_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    configure_logging(app)

    with app.app_context():
        init_database()

    app.register_blueprint(auth_routes)
    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(api_routes)
    register_error_handlers(app)
    app.logger.info("Application started")

    @app.after_request
    def track_page_activity(response):
        if response.status_code < 400 and not request.path.startswith("/api/"):
            endpoint = app.view_functions.get(request.endpoint) if request.endpoint else None
            if endpoint and request.endpoint != "static" and request.method == "GET":
                record_activity("page_view", request.endpoint)
        return response

    return app


application = create_app()
app = application


if __name__ == "__main__":
    application.run(debug=application.config["DEBUG"])
