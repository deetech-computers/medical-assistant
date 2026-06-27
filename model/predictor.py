from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(__file__).resolve().parent / "diagnosis_model.pkl"


class DiseasePredictor:
    def __init__(self, model_path=MODEL_PATH):
        if not Path(model_path).exists():
            raise FileNotFoundError(
                "Model file was not found. Run python model/train_model.py first."
            )
        payload = joblib.load(model_path)
        self.model = payload["model"]
        self.symptoms = payload["symptoms"]

    def predict(self, selected_symptoms):
        row = {symptom: 0 for symptom in self.symptoms}
        for symptom in selected_symptoms:
            if symptom in row:
                row[symptom] = 1

        input_frame = pd.DataFrame([row], columns=self.symptoms)
        disease = self.model.predict(input_frame)[0]
        confidence = self._confidence(input_frame)
        return {"disease": disease, "confidence": confidence}

    def _confidence(self, input_frame):
        if not hasattr(self.model, "predict_proba"):
            return None

        probability = self.model.predict_proba(input_frame).max()
        return round(float(probability) * 100)
