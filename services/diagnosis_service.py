import json

from repositories import diagnosis_repository
from services.symptom_service import format_symptom_name


def save_diagnosis(result, user_id=None):
    symptoms = json.dumps(result["selected_symptoms"])
    return diagnosis_repository.create(
        user_id,
        result["disease"],
        result["confidence"],
        symptoms,
    )


def list_user_diagnoses(user_id):
    rows = diagnosis_repository.list_by_user(user_id)
    return [_format_diagnosis(row) for row in rows]


def list_recent_diagnoses(limit=40):
    rows = diagnosis_repository.list_recent(limit)
    return [_format_diagnosis(row) for row in rows]


def _format_diagnosis(row):
    diagnosis = dict(row)
    symptoms = json.loads(diagnosis["symptoms"])
    diagnosis["symptom_labels"] = [format_symptom_name(symptom) for symptom in symptoms]
    return diagnosis
