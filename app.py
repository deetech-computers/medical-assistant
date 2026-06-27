from flask import Flask, Response, request, send_from_directory, url_for

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
    def finalize_response(response):
        set_response_headers(response)

        if response.status_code < 400 and not request.path.startswith("/api/"):
            endpoint = app.view_functions.get(request.endpoint) if request.endpoint else None
            if endpoint and request.endpoint != "static" and request.method == "GET":
                record_activity("page_view", request.endpoint)
        return response

    @app.route("/service-worker.js")
    def service_worker():
        response = send_from_directory(app.static_folder, "js/service-worker.js")
        response.headers["Service-Worker-Allowed"] = "/"
        return response

    @app.route("/robots.txt")
    def robots():
        return Response(
            "User-agent: *\nAllow: /\nSitemap: "
            f"{url_for('sitemap', _external=True)}\n",
            mimetype="text/plain",
        )

    @app.route("/sitemap.xml")
    def sitemap():
        routes = [
            url_for("main_routes.index", _external=True),
            url_for("main_routes.diagnosis", _external=True),
            url_for("main_routes.results", _external=True),
            url_for("main_routes.about", _external=True),
            url_for("auth_routes.login", _external=True),
            url_for("auth_routes.register", _external=True),
        ]
        body = "\n".join(
            [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                *[f"<url><loc>{route}</loc></url>" for route in routes],
                "</urlset>",
            ]
        )
        return Response(body, mimetype="application/xml")

    return app


def set_response_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")

    if request.endpoint == "static":
        response.headers["Cache-Control"] = "public, max-age=604800"
    elif request.path == "/service-worker.js":
        response.headers["Cache-Control"] = "no-cache"


application = create_app()
app = application


if __name__ == "__main__":
    application.run(debug=application.config["DEBUG"])
