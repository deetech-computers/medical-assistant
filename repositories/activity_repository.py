from sqlalchemy import func, select

from database.models import Activity, Diagnosis, User
from database.session import database_session


def create(user_id, event_type, details, path):
    with database_session() as session:
        session.add(
            Activity(
                user_id=user_id,
                event_type=event_type,
                details=details,
                path=path,
            )
        )


def list_recent(limit=40):
    with database_session() as session:
        rows = session.execute(
            select(Activity, User.name, User.email)
            .outerjoin(User, User.id == Activity.user_id)
            .order_by(Activity.created_at.desc())
            .limit(limit)
        ).all()

        records = []

        for activity, name, email in rows:
            record = activity.to_dict()
            record["name"] = name
            record["email"] = email
            records.append(record)

        return records


def summary():
    with database_session() as session:
        return {
            "user_count": session.scalar(select(func.count(User.id))),
            "diagnosis_count": session.scalar(select(func.count(Diagnosis.id))),
            "activity_count": session.scalar(select(func.count(Activity.id))),
            "guest_diagnosis_count": session.scalar(
                select(func.count(Diagnosis.id)).where(Diagnosis.user_id.is_(None))
            ),
        }
