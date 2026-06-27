from flask import Blueprint, render_template

from routes.auth_routes import admin_required
from services.activity_service import activity_summary, list_recent_activities
from services.auth_service import list_users
from services.diagnosis_service import list_recent_diagnoses


admin_routes = Blueprint("admin_routes", __name__, url_prefix="/admin")


@admin_routes.route("/")
@admin_required
def dashboard():
    return render_template(
        "admin_dashboard.html",
        summary=activity_summary(),
        activities=list_recent_activities(),
        diagnoses=list_recent_diagnoses(),
    )


@admin_routes.route("/users")
@admin_required
def users():
    return render_template("admin_users.html", users=list_users())
