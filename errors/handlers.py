from flask import jsonify, render_template, request


def wants_json_response():
    return request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning("Page not found: %s", request.path)
        if wants_json_response():
            return jsonify({"error": "Not found", "status": 404}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("Unexpected server error")
        if wants_json_response():
            return jsonify({"error": "Server error", "status": 500}), 500
        return render_template("errors/500.html"), 500
