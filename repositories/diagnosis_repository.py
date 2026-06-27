from sqlalchemy import select

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
