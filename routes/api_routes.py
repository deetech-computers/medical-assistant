from functools import wraps

from flask import Blueprint, current_app, session

from routes.auth_routes import current_user
from services.activity_service import activity_summary, list_recent_activities, record_activity
from services.admin_analytics_service import build_admin_api_payload
from services.auth_service import authenticate_user, create_user, list_users
from services.diagnosis_service import list_recent_diagnoses, list_user_diagnoses, save_diagnosis
from services.prediction_service import create_prediction
from services.symptom_service import format_symptom_name, get_symptom_options
from utils.api_response import error_response, success_response
from validators.api_validators import get_json_payload, require_fields, validate_symptom_payload


api_routes = Blueprint("api_routes", __name__, url_prefix="/api/v1")


def serialize_row(row):
    return dict(row) if row else None


def serialize_user(user):
    user_data = serialize_row(user)

    if not user_data:
        return None

    return {
        "id": user_data.get("id"),
        "name": user_data.get("name"),
        "email": user_data.get("email"),
        "role": user_data.get("role"),
        "created_at": user_data.get("created_at"),
        "diagnosis_count": user_data.get("diagnosis_count"),
    }


def serialize_diagnosis(diagnosis):
    return {
        "id": diagnosis.get("id"),
        "user_id": diagnosis.get("user_id"),
        "user_name": diagnosis.get("name"),
        "user_email": diagnosis.get("email"),
        "disease": diagnosis.get("disease"),
        "confidence": diagnosis.get("confidence"),
        "insights": diagnosis.get("insights"),
        "symptoms": diagnosis.get("symptom_labels", []),
        "created_at": diagnosis.get("created_at"),
    }


def serialize_activity(activity):
    activity_data = dict(activity)
    return {
        "id": activity_data.get("id"),
        "user_id": activity_data.get("user_id"),
        "user_name": activity_data.get("name"),
        "user_email": activity_data.get("email"),
        "event_type": activity_data.get("event_type"),
        "details": activity_data.get("details"),
        "path": activity_data.get("path"),
        "created_at": activity_data.get("created_at"),
    }


def api_login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user():
            return error_response("Authentication is required.", 401, "authentication_required")
        return view(*args, **kwargs)

    return wrapped_view


def api_admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = current_user()

        if not user:
            return error_response("Authentication is required.", 401, "authentication_required")

        if user["role"] != "admin":
            return error_response("Admin access is required.", 403, "admin_required")

        return view(*args, **kwargs)

    return wrapped_view


@api_routes.route("/health")
def health():
    return success_response(
        {
            "status": "ok",
            "service": "medical-diagnosis-assistant",
            "version": "v1",
            "environment": current_app.config.get("ENV_NAME", "development"),
        }
    )


@api_routes.route("/symptoms")
def symptoms():
    return success_response({"symptoms": get_symptom_options()})


@api_routes.route("/predictions", methods=["POST"])
def create_prediction_record():
    payload, payload_error = get_json_payload()

    if payload_error:
        return error_response(payload_error, 400, "invalid_json")

    selected_symptoms, symptom_error = validate_symptom_payload(payload)

    if symptom_error:
        return error_response(symptom_error, 400, "invalid_symptoms")

    result = create_prediction(selected_symptoms)

    if result.get("error"):
        return error_response(result["error"], 400, "prediction_validation_failed")

    diagnosis_id = save_diagnosis(result, session.get("user_id"))
    record_activity("api_diagnosis", f"Diagnosis record {diagnosis_id}: {result['disease']}")

    return success_response(
        {
            "id": diagnosis_id,
            "disease": result["disease"],
            "confidence": result["confidence"],
            "insights": result["insights"],
            "selected_symptoms": [
                {
                    "key": symptom,
                    "label": format_symptom_name(symptom),
                }
                for symptom in result["selected_symptoms"]
            ],
        },
        "Prediction completed.",
        201,
    )


@api_routes.route("/auth/register", methods=["POST"])
def api_register():
    payload, payload_error = get_json_payload()

    if payload_error:
        return error_response(payload_error, 400, "invalid_json")

    missing_error = require_fields(payload, ["name", "email", "password"])

    if missing_error:
        return error_response(missing_error, 400, "missing_fields")

    result = create_user(payload["name"], payload["email"], payload["password"])

    if result.get("error"):
        return error_response(result["error"], 400, "registration_failed")

    session.clear()
    session["user_id"] = result["user"]["id"]
    record_activity("api_register", "New user account")

    return success_response({"user": serialize_user(result["user"])}, "Account created.", 201)


@api_routes.route("/auth/login", methods=["POST"])
def api_login():
    payload, payload_error = get_json_payload()

    if payload_error:
        return error_response(payload_error, 400, "invalid_json")

    missing_error = require_fields(payload, ["email", "password"])

    if missing_error:
        return error_response(missing_error, 400, "missing_fields")

    user = authenticate_user(payload["email"], payload["password"])

    if not user:
        return error_response("Invalid email or password.", 401, "invalid_credentials")

    session.clear()
    session["user_id"] = user["id"]
    record_activity("api_login", "User signed in")

    return success_response({"user": serialize_user(user)}, "Login successful.")


@api_routes.route("/auth/logout", methods=["POST"])
def api_logout():
    record_activity("api_logout", "User signed out")
    session.clear()
    return success_response(message="Logout successful.")


@api_routes.route("/me")
def me():
    user = current_user()

    if not user:
        return success_response({"authenticated": False, "user": None})

    return success_response({"authenticated": True, "user": serialize_user(user)})


@api_routes.route("/history")
@api_login_required
def api_history():
    diagnoses = [
        serialize_diagnosis(diagnosis)
        for diagnosis in list_user_diagnoses(session["user_id"])
    ]
    return success_response({"diagnoses": diagnoses})


@api_routes.route("/admin/summary")
@api_admin_required
def api_admin_summary():
    return success_response({"summary": activity_summary()})


@api_routes.route("/admin/analytics")
@api_admin_required
def api_admin_analytics():
    return success_response({"analytics": build_admin_api_payload()})


@api_routes.route("/admin/users")
@api_admin_required
def api_admin_users():
    users = [serialize_user(user) for user in list_users()]
    return success_response({"users": users})


@api_routes.route("/admin/diagnoses")
@api_admin_required
def api_admin_diagnoses():
    diagnoses = [
        serialize_diagnosis(diagnosis)
        for diagnosis in list_recent_diagnoses()
    ]
    return success_response({"diagnoses": diagnoses})


@api_routes.route("/admin/activities")
@api_admin_required
def api_admin_activities():
    activities = [
        serialize_activity(activity)
        for activity in list_recent_activities()
    ]
    return success_response({"activities": activities})
