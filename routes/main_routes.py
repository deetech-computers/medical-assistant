from flask import Blueprint, redirect, render_template, request, session, url_for

from routes.auth_routes import login_required
from services.activity_service import record_activity
from services.diagnosis_service import list_user_diagnoses, save_diagnosis
from services.prediction_service import create_prediction
from services.symptom_service import (
    format_symptom_name,
    get_symptom_options,
    validate_symptoms,
)


main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/")
def index():
    return render_template("home.html")


@main_routes.route("/diagnosis")
def diagnosis():
    return render_template("index.html", symptoms=get_symptom_options())


@main_routes.route("/predict", methods=["POST"])
def predict():
    selected_symptoms = request.form.getlist("symptoms")
    result = create_prediction(selected_symptoms)

    if result.get("error"):
        return render_template(
            "index.html",
            symptoms=get_symptom_options(),
            error=result["error"],
            selected_symptoms=selected_symptoms,
        )

    diagnosis_id = save_diagnosis(result, session.get("user_id"))
    record_activity(
        "diagnosis",
        f"Diagnosis record {diagnosis_id}: {result['disease']}",
    )

    return render_template(
        "result.html",
        result=result,
        symptom_label=format_symptom_name,
    )


@main_routes.route("/review", methods=["POST"])
def review():
    selected_symptoms = validate_symptoms(request.form.getlist("symptoms"))

    if not selected_symptoms:
        return render_template(
            "index.html",
            symptoms=get_symptom_options(),
            error="Select at least one symptom before reviewing the case.",
            selected_symptoms=[],
        )

    record_activity(
        "review",
        f"Reviewing {len(selected_symptoms)} selected symptoms",
    )

    return render_template(
        "review.html",
        selected_symptoms=selected_symptoms,
        symptom_label=format_symptom_name,
    )


@main_routes.route("/about")
def about():
    return render_template("about.html")


@main_routes.route("/history")
@login_required
def history():
    return render_template(
        "history.html",
        diagnoses=list_user_diagnoses(session["user_id"]),
    )


@main_routes.route("/results")
def results():
    if session.get("user_id"):
        return redirect(url_for("main_routes.history"))
    return render_template("results_overview.html")


@main_routes.route("/reset")
def reset():
    return redirect(url_for("main_routes.diagnosis"))
