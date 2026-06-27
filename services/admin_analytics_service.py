import csv
import io
import json
from collections import Counter
from datetime import datetime, timedelta

from repositories import activity_repository, diagnosis_repository, user_repository
from services.diagnosis_service import format_diagnosis_rows
from services.symptom_service import format_symptom_name, get_symptom_keys


def build_admin_dashboard(args):
    filters = normalize_filters(args)
    page = parse_page(args.get("page"))
    per_page = parse_page_size(args.get("per_page"))
    paginated = diagnosis_repository.list_filtered(filters, page, per_page)
    diagnoses = format_diagnosis_rows(paginated["records"])
    chart_data = build_chart_data()

    return {
        "filters": filters,
        "diagnoses": diagnoses,
        "pagination": {
            "page": paginated["page"],
            "per_page": paginated["per_page"],
            "pages": paginated["pages"],
            "total": paginated["total"],
            "has_previous": paginated["page"] > 1,
            "has_next": paginated["page"] < paginated["pages"],
            "previous_page": max(1, paginated["page"] - 1),
            "next_page": min(paginated["pages"], paginated["page"] + 1),
        },
        "chart_data": chart_data,
        "chart_data_json": json.dumps(chart_data),
        "disease_options": [item["label"] for item in chart_data["diseases"]],
        "symptom_analytics": build_symptom_analytics(diagnoses),
        "reports": build_report_cards(chart_data),
    }


def build_admin_api_payload():
    chart_data = build_chart_data()
    return {
        "charts": chart_data,
        "reports": build_report_cards(chart_data),
    }


def build_diagnosis_csv(args):
    filters = normalize_filters(args)
    records = format_diagnosis_rows(diagnosis_repository.list_for_export(filters))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "date",
        "user",
        "email",
        "disease",
        "confidence",
        "symptoms",
        "record_type",
    ])

    for record in records:
        writer.writerow([
            record.get("created_at"),
            record.get("name") or "Guest",
            record.get("email") or "",
            record.get("disease"),
            record.get("confidence") or 0,
            "; ".join(record.get("symptom_labels", [])),
            "Saved" if record.get("user_id") else "Guest",
        ])

    return output.getvalue()


def normalize_filters(args):
    return {
        "search": (args.get("search") or "").strip(),
        "disease": (args.get("disease") or "").strip(),
        "account_mode": (args.get("account_mode") or "").strip(),
        "start_date": (args.get("start_date") or "").strip(),
        "end_date": (args.get("end_date") or "").strip(),
    }


def parse_page(value):
    try:
        return max(int(value or 1), 1)
    except ValueError:
        return 1


def parse_page_size(value):
    try:
        return max(min(int(value or 10), 25), 5)
    except ValueError:
        return 10


def build_chart_data():
    records = format_diagnosis_rows(diagnosis_repository.list_for_export({}, limit=1000))
    daily = count_by_date(records, 14)
    weekly = count_by_week(records, 8)
    monthly = count_by_month(records, 6)
    diseases = diagnosis_repository.disease_counts()
    activity = activity_repository.event_counts()
    users = user_repository.role_counts()

    return {
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
        "diseases": diseases,
        "activities": activity,
        "users": users,
    }


def count_by_date(records, limit):
    counter = Counter()

    for record in records:
        created_at = parse_created_at(record.get("created_at"))
        if created_at:
            counter[created_at.date().isoformat()] += 1

    return fill_recent_days(counter, limit)


def count_by_week(records, limit):
    counter = Counter()

    for record in records:
        created_at = parse_created_at(record.get("created_at"))
        if created_at:
            iso_year, iso_week, _ = created_at.isocalendar()
            counter[f"{iso_year}-W{iso_week:02d}"] += 1

    return latest_counter_items(counter, limit)


def count_by_month(records, limit):
    counter = Counter()

    for record in records:
        created_at = parse_created_at(record.get("created_at"))
        if created_at:
            counter[created_at.strftime("%Y-%m")] += 1

    return latest_counter_items(counter, limit)


def fill_recent_days(counter, limit):
    today = datetime.today().date()
    labels = [
        (today - timedelta(days=offset)).isoformat()
        for offset in range(limit - 1, -1, -1)
    ]
    return [{"label": label, "value": counter.get(label, 0)} for label in labels]


def latest_counter_items(counter, limit):
    labels = sorted(counter.keys())[-limit:]
    return [{"label": label, "value": counter.get(label, 0)} for label in labels]


def parse_created_at(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def build_symptom_analytics(diagnoses):
    counts = {symptom: 0 for symptom in get_symptom_keys()}

    for diagnosis in diagnoses:
        for symptom in diagnosis.get("selected_symptoms", []):
            if symptom in counts:
                counts[symptom] += 1

    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [
        {
            "key": symptom,
            "label": format_symptom_name(symptom),
            "value": total,
            "width": min(total * 10, 100),
        }
        for symptom, total in ranked[:8]
        if total > 0
    ]


def build_report_cards(chart_data):
    daily_total = sum(item["value"] for item in chart_data["daily"])
    weekly_total = sum(item["value"] for item in chart_data["weekly"])
    monthly_total = sum(item["value"] for item in chart_data["monthly"])
    top_disease = chart_data["diseases"][0]["label"] if chart_data["diseases"] else "No records"

    return [
        {
            "label": "Daily report",
            "value": daily_total,
            "detail": "Diagnoses in the recent daily window",
        },
        {
            "label": "Weekly report",
            "value": weekly_total,
            "detail": "Diagnoses across recent weeks",
        },
        {
            "label": "Monthly report",
            "value": monthly_total,
            "detail": "Diagnoses across recent months",
        },
        {
            "label": "Most common condition",
            "value": top_disease,
            "detail": "Highest recorded disease in the dataset",
        },
    ]
