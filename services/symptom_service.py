from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "symptoms_disease_dataset.csv"

SYMPTOM_CATEGORIES = {
    "abdominal_pain": ["digestive", "pain"],
    "chest_pain": ["respiratory", "pain"],
    "cough": ["respiratory"],
    "diarrhea": ["digestive"],
    "dizziness": ["neurological"],
    "excessive_thirst": ["general"],
    "fatigue": ["general"],
    "fever": ["general"],
    "frequent_urination": ["general"],
    "headache": ["neurological", "pain"],
    "itching": ["skin"],
    "joint_pain": ["pain"],
    "nausea": ["digestive"],
    "night_sweats": ["general"],
    "rash": ["skin"],
    "runny_nose": ["respiratory"],
    "shortness_of_breath": ["respiratory"],
    "sore_throat": ["respiratory"],
    "vomiting": ["digestive"],
    "weight_loss": ["general"],
}


def get_symptom_keys():
    dataset = pd.read_csv(DATA_PATH, nrows=1)
    return [column for column in dataset.columns if column != "disease"]


def format_symptom_name(symptom_key):
    return symptom_key.replace("_", " ").title()


def get_symptom_options():
    return [
        {
            "key": symptom,
            "label": format_symptom_name(symptom),
            "categories": " ".join(SYMPTOM_CATEGORIES.get(symptom, ["general"])),
        }
        for symptom in get_symptom_keys()
    ]


def validate_symptoms(selected_symptoms):
    valid_symptoms = set(get_symptom_keys())
    return [symptom for symptom in selected_symptoms if symptom in valid_symptoms]
