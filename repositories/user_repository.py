from sqlalchemy import func, select

from database.models import Diagnosis, User
from database.session import database_session


def find_by_email(email):
    with database_session() as session:
        user = session.scalar(select(User).where(User.email == email))
        return user.to_dict(include_password=True) if user else None


def find_by_id(user_id):
    with database_session() as session:
        user = session.get(User, user_id)
        return user.to_dict() if user else None


def email_exists(email):
    with database_session() as session:
        return session.scalar(select(User.id).where(User.email == email)) is not None


def create(name, email, password_hash):
    with database_session() as session:
        user = User(name=name, email=email, password_hash=password_hash)
        session.add(user)
        session.flush()
        return user.id


def list_all_with_diagnosis_count():
    with database_session() as session:
        rows = session.execute(
            select(
                User.id,
                User.name,
                User.email,
                User.role,
                User.created_at,
                func.count(Diagnosis.id).label("diagnosis_count"),
            )
            .outerjoin(Diagnosis, Diagnosis.user_id == User.id)
            .group_by(User.id, User.name, User.email, User.role, User.created_at)
            .order_by(User.created_at.desc())
        ).all()

        return [
            {
                "id": row.id,
                "name": row.name,
                "email": row.email,
                "role": row.role,
                "created_at": str(row.created_at),
                "diagnosis_count": row.diagnosis_count,
            }
            for row in rows
        ]


def role_counts():
    with database_session() as session:
        rows = session.execute(
            select(User.role, func.count(User.id).label("total"))
            .group_by(User.role)
            .order_by(func.count(User.id).desc())
        ).all()

        return [{"label": row.role, "value": row.total} for row in rows]
