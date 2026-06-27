from sqlalchemy import func, or_, select

from database.models import Diagnosis, User, serialize_datetime
from database.session import database_session


def create(user_id, disease, confidence, symptoms):
    with database_session() as session:
        diagnosis = Diagnosis(
            user_id=user_id,
            disease=disease,
            confidence=confidence,
            symptoms=symptoms,
        )
        session.add(diagnosis)
        session.flush()
        return diagnosis.id


def list_by_user(user_id):
    with database_session() as session:
        diagnoses = session.scalars(
            select(Diagnosis)
            .where(Diagnosis.user_id == user_id)
            .order_by(Diagnosis.created_at.desc())
        ).all()

        return [diagnosis.to_dict() for diagnosis in diagnoses]


def list_recent(limit=40):
    with database_session() as session:
        rows = session.execute(
            select(Diagnosis, User.name, User.email)
            .outerjoin(User, User.id == Diagnosis.user_id)
            .order_by(Diagnosis.created_at.desc())
            .limit(limit)
        ).all()

        records = []

        for diagnosis, name, email in rows:
            record = diagnosis.to_dict()
            record["name"] = name
            record["email"] = email
            record["created_at"] = serialize_datetime(diagnosis.created_at)
            records.append(record)

        return records


def list_filtered(filters=None, page=1, per_page=10):
    filters = filters or {}
    page = max(int(page or 1), 1)
    per_page = max(min(int(per_page or 10), 50), 1)
    offset = (page - 1) * per_page

    with database_session() as session:
        base_query = (
            select(Diagnosis, User.name, User.email)
            .outerjoin(User, User.id == Diagnosis.user_id)
            .where(*_filter_conditions(filters))
        )

        rows = session.execute(
            base_query
            .order_by(Diagnosis.created_at.desc())
            .offset(offset)
            .limit(per_page)
        ).all()

        total = session.scalar(
            select(func.count(Diagnosis.id))
            .outerjoin(User, User.id == Diagnosis.user_id)
            .where(*_filter_conditions(filters))
        )

        records = []

        for diagnosis, name, email in rows:
            record = diagnosis.to_dict()
            record["name"] = name
            record["email"] = email
            record["created_at"] = serialize_datetime(diagnosis.created_at)
            records.append(record)

        return {
            "records": records,
            "total": total or 0,
            "page": page,
            "per_page": per_page,
            "pages": max(1, ((total or 0) + per_page - 1) // per_page),
        }


def list_for_export(filters=None, limit=1000):
    filters = filters or {}

    with database_session() as session:
        rows = session.execute(
            select(Diagnosis, User.name, User.email)
            .outerjoin(User, User.id == Diagnosis.user_id)
            .where(*_filter_conditions(filters))
            .order_by(Diagnosis.created_at.desc())
            .limit(limit)
        ).all()

        records = []

        for diagnosis, name, email in rows:
            record = diagnosis.to_dict()
            record["name"] = name
            record["email"] = email
            record["created_at"] = serialize_datetime(diagnosis.created_at)
            records.append(record)

        return records


def disease_counts(limit=8):
    with database_session() as session:
        rows = session.execute(
            select(Diagnosis.disease, func.count(Diagnosis.id).label("total"))
            .group_by(Diagnosis.disease)
            .order_by(func.count(Diagnosis.id).desc())
            .limit(limit)
        ).all()

        return [{"label": row.disease, "value": row.total} for row in rows]


def daily_counts(limit=14):
    created_day = func.date(Diagnosis.created_at)

    with database_session() as session:
        rows = session.execute(
            select(created_day.label("day"), func.count(Diagnosis.id).label("total"))
            .group_by(created_day)
            .order_by(created_day.desc())
            .limit(limit)
        ).all()

        return [
            {"label": str(row.day), "value": row.total}
            for row in reversed(rows)
        ]


def weekly_counts(limit=8):
    week_label = func.strftime("%Y-W%W", Diagnosis.created_at)

    with database_session() as session:
        rows = session.execute(
            select(week_label.label("week"), func.count(Diagnosis.id).label("total"))
            .group_by(week_label)
            .order_by(week_label.desc())
            .limit(limit)
        ).all()

        return [
            {"label": str(row.week), "value": row.total}
            for row in reversed(rows)
        ]


def monthly_counts(limit=6):
    month_label = func.strftime("%Y-%m", Diagnosis.created_at)

    with database_session() as session:
        rows = session.execute(
            select(month_label.label("month"), func.count(Diagnosis.id).label("total"))
            .group_by(month_label)
            .order_by(month_label.desc())
            .limit(limit)
        ).all()

        return [
            {"label": str(row.month), "value": row.total}
            for row in reversed(rows)
        ]


def _filter_conditions(filters):
    conditions = []
    search = (filters.get("search") or "").strip()
    disease = (filters.get("disease") or "").strip()
    account_mode = (filters.get("account_mode") or "").strip()
    start_date = (filters.get("start_date") or "").strip()
    end_date = (filters.get("end_date") or "").strip()

    if search:
        pattern = f"%{search}%"
        conditions.append(
            or_(
                Diagnosis.disease.ilike(pattern),
                Diagnosis.symptoms.ilike(pattern),
                User.name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    if disease:
        conditions.append(Diagnosis.disease == disease)

    if account_mode == "guest":
        conditions.append(Diagnosis.user_id.is_(None))
    elif account_mode == "saved":
        conditions.append(Diagnosis.user_id.is_not(None))

    if start_date:
        conditions.append(func.date(Diagnosis.created_at) >= start_date)

    if end_date:
        conditions.append(func.date(Diagnosis.created_at) <= end_date)

    return conditions
