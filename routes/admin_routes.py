from flask import Blueprint, Response, render_template, request

from routes.auth_routes import admin_required
from services.activity_service import activity_summary, list_recent_activities
from services.admin_analytics_service import build_admin_dashboard, build_diagnosis_csv
from services.auth_service import list_users


admin_routes = Blueprint("admin_routes", __name__, url_prefix="/admin")


@admin_routes.route("/")
@admin_required
def dashboard():
    dashboard_data = build_admin_dashboard(request.args)

    return render_template(
        "admin_dashboard.html",
        summary=activity_summary(),
        activities=list_recent_activities(),
        **dashboard_data,
    )


@admin_routes.route("/users")
@admin_required
def users():
    return render_template("admin_users.html", users=list_users())


@admin_routes.route("/export/diagnoses")
@admin_required
def export_diagnoses():
    csv_body = build_diagnosis_csv(request.args)
    return Response(
        csv_body,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=diagnosis-report.csv",
        },
    )
