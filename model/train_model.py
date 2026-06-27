from pathlib import Path

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "symptoms_disease_dataset.csv"
MODEL_PATH = BASE_DIR / "model" / "diagnosis_model.pkl"


def train_model():
    dataset = pd.read_csv(DATA_PATH)
    features = dataset.drop(columns=["disease"])
    target = dataset["disease"]

    classifier = DecisionTreeClassifier(max_depth=6, random_state=42)
    classifier.fit(features, target)

    payload = {
        "model": classifier,
        "symptoms": list(features.columns),
        "diseases": sorted(target.unique()),
    }
    joblib.dump(payload, MODEL_PATH)
    return MODEL_PATH


if __name__ == "__main__":
    saved_path = train_model()
    print(f"Model saved to {saved_path}")
