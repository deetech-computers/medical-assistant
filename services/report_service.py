URGENT_SYMPTOMS = {
    "chest_pain",
    "shortness_of_breath",
    "dizziness",
}

RECOVERY_FOCUSED_SYMPTOMS = {
    "fever",
    "cough",
    "sore_throat",
    "runny_nose",
    "fatigue",
}

DIGESTIVE_SYMPTOMS = {
    "abdominal_pain",
    "diarrhea",
    "nausea",
    "vomiting",
}


def build_report_insights(prediction_result):
    selected_symptoms = prediction_result.get("selected_symptoms", [])
    confidence = int(prediction_result.get("confidence") or 0)
    risk_score = calculate_risk_score(confidence, selected_symptoms)
    severity = describe_severity(risk_score, selected_symptoms)

    return {
        "confidence_level": describe_confidence(confidence),
        "risk_score": risk_score,
        "severity": severity,
        "probability_rows": build_probability_rows(prediction_result.get("disease"), confidence),
        "summary": build_prediction_summary(prediction_result.get("disease"), confidence, selected_symptoms),
        "recommendations": build_recommendations(selected_symptoms),
        "lifestyle_suggestions": build_lifestyle_suggestions(selected_symptoms),
        "hydration_advice": build_hydration_advice(selected_symptoms),
        "recovery_advice": build_recovery_advice(selected_symptoms),
        "emergency_warning": build_emergency_warning(selected_symptoms),
        "disclaimer": (
            "This report is for an educational prototype and does not replace a doctor, clinic, "
            "or emergency care."
        ),
    }


def calculate_risk_score(confidence, selected_symptoms):
    symptom_count = len(selected_symptoms)
    urgent_count = len(set(selected_symptoms) & URGENT_SYMPTOMS)
    digestive_count = len(set(selected_symptoms) & DIGESTIVE_SYMPTOMS)

    score = 20 + min(symptom_count * 7, 35)
    score += min(confidence * 0.18, 18)
    score += urgent_count * 16
    score += 8 if digestive_count >= 2 else 0

    return min(95, round(score))


def describe_confidence(confidence):
    if confidence >= 80:
        return {
            "label": "Strong match",
            "message": "The selected symptoms closely match one condition in the project dataset.",
        }
    if confidence >= 55:
        return {
            "label": "Moderate match",
            "message": "The selected symptoms point toward a possible condition, but review is advised.",
        }
    return {
        "label": "Limited match",
        "message": "The selected symptoms produce a low certainty result in the project dataset.",
    }


def describe_severity(risk_score, selected_symptoms):
    if set(selected_symptoms) & {"chest_pain", "shortness_of_breath"}:
        return {
            "label": "Needs prompt attention",
            "tone": "high",
            "message": "Selected symptoms include warning signs that should be reviewed quickly.",
        }
    if risk_score >= 70:
        return {
            "label": "Elevated",
            "tone": "high",
            "message": "The symptom pattern may need timely clinical review.",
        }
    if risk_score >= 45:
        return {
            "label": "Moderate",
            "tone": "medium",
            "message": "Monitor symptoms and consider a clinical check if they continue.",
        }
    return {
        "label": "Low",
        "tone": "low",
        "message": "Current selections suggest a lower risk pattern in this project report.",
    }


def build_probability_rows(disease, confidence):
    remaining = max(0, 100 - confidence)
    return [
        {"label": disease or "Predicted condition", "value": confidence},
        {"label": "Other dataset patterns", "value": remaining},
    ]


def build_prediction_summary(disease, confidence, selected_symptoms):
    count = len(selected_symptoms)
    symptom_word = "symptom" if count == 1 else "symptoms"
    return (
        f"The model compared {count} selected {symptom_word} with the project dataset "
        f"and returned {disease} with a {confidence}% match."
    )


def build_recommendations(selected_symptoms):
    recommendations = [
        "Review this result with a qualified health professional before taking treatment decisions.",
        "Track changes in symptoms, temperature, pain level, and duration.",
    ]

    if "fever" in selected_symptoms:
        recommendations.append("Monitor fever pattern and seek care if it becomes high or persistent.")

    if set(selected_symptoms) & DIGESTIVE_SYMPTOMS:
        recommendations.append("Avoid heavy meals while digestive symptoms are active.")

    if set(selected_symptoms) & URGENT_SYMPTOMS:
        recommendations.append("Do not delay clinical help if warning symptoms worsen.")

    return recommendations


def build_lifestyle_suggestions(selected_symptoms):
    suggestions = [
        "Rest in a clean, well-ventilated environment.",
        "Avoid strenuous activity until symptoms improve.",
    ]

    if "rash" in selected_symptoms or "itching" in selected_symptoms:
        suggestions.append("Avoid scratching affected skin and keep the area clean.")

    if "cough" in selected_symptoms or "sore_throat" in selected_symptoms:
        suggestions.append("Reduce exposure to smoke, dust, and cold drinks if they worsen symptoms.")

    return suggestions


def build_hydration_advice(selected_symptoms):
    if set(selected_symptoms) & {"vomiting", "diarrhea", "fever", "excessive_thirst"}:
        return "Take small, regular fluids and seek help if dehydration signs appear."
    return "Maintain normal fluid intake unless a clinician has advised otherwise."


def build_recovery_advice(selected_symptoms):
    if set(selected_symptoms) & RECOVERY_FOCUSED_SYMPTOMS:
        return "Allow time for rest, monitor symptom duration, and avoid self-medication."
    return "Observe symptoms over time and arrange a clinical review if they persist or worsen."


def build_emergency_warning(selected_symptoms):
    selected = set(selected_symptoms)

    if {"chest_pain", "shortness_of_breath"} <= selected:
        return "Chest pain with shortness of breath can be serious. Seek urgent medical care."

    if "chest_pain" in selected:
        return "Chest pain should be checked promptly, especially if severe or spreading."

    if "shortness_of_breath" in selected:
        return "Shortness of breath should be reviewed quickly if it is new or worsening."

    if "dizziness" in selected:
        return "Severe dizziness, fainting, or confusion needs urgent medical attention."

    return "Seek urgent care if symptoms become severe, sudden, or difficult to manage."
