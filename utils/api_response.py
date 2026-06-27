from flask import jsonify


def success_response(data=None, message=None, status=200, meta=None):
    payload = {
        "success": True,
        "data": data or {},
    }

    if message:
        payload["message"] = message

    if meta:
        payload["meta"] = meta

    return jsonify(payload), status


def error_response(message, status=400, code=None, details=None):
    payload = {
        "success": False,
        "error": {
            "message": message,
            "code": code or "request_error",
        },
    }

    if details:
        payload["error"]["details"] = details

    return jsonify(payload), status
