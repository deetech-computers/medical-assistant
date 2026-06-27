from model.predictor import DiseasePredictor
from services.symptom_service import validate_symptoms


predictor = DiseasePredictor()


def create_prediction(selected_symptoms):
    clean_symptoms = validate_symptoms(selected_symptoms)
    if not clean_symptoms:
        return {
            "error": "Select at least one symptom before checking the result.",
            "selected_symptoms": [],
        }

    prediction = predictor.predict(clean_symptoms)
    return {
        "disease": prediction["disease"],
        "confidence": prediction["confidence"],
        "selected_symptoms": clean_symptoms,
    }
