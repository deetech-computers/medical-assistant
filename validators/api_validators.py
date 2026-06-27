from flask import request


def get_json_payload():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return None, "Request body must be valid JSON."

    return payload, None


def require_fields(payload, fields):
    missing_fields = [
        field
        for field in fields
        if field not in payload or payload.get(field) in (None, "")
    ]

    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}."

    return None


def validate_symptom_payload(payload):
    error = require_fields(payload, ["symptoms"])

    if error:
        return None, error

    symptoms = payload.get("symptoms")

    if not isinstance(symptoms, list):
        return None, "Symptoms must be provided as a list."

    if not all(isinstance(symptom, str) for symptom in symptoms):
        return None, "Each symptom must be a string."

    return symptoms, None
