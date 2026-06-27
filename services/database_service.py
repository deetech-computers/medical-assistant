from sqlalchemy import text
from werkzeug.security import generate_password_hash

from database.models import User
from database.session import create_schema, database_session


def init_database():
    create_schema()
    ensure_indexes()
    seed_default_admin()


def ensure_indexes():
    index_statements = [
        "CREATE INDEX IF NOT EXISTS ix_users_role ON users (role)",
        "CREATE INDEX IF NOT EXISTS ix_users_created_at ON users (created_at)",
        "CREATE INDEX IF NOT EXISTS ix_diagnoses_user_id ON diagnoses (user_id)",
        "CREATE INDEX IF NOT EXISTS ix_diagnoses_disease ON diagnoses (disease)",
        "CREATE INDEX IF NOT EXISTS ix_diagnoses_created_at ON diagnoses (created_at)",
        "CREATE INDEX IF NOT EXISTS ix_activities_user_id ON activities (user_id)",
        "CREATE INDEX IF NOT EXISTS ix_activities_event_type ON activities (event_type)",
        "CREATE INDEX IF NOT EXISTS ix_activities_created_at ON activities (created_at)",
    ]

    with database_session() as session:
        for statement in index_statements:
            session.execute(text(statement))


def seed_default_admin():
    with database_session() as session:
        admin_exists = session.query(User.id).filter(User.role == "admin").first()

        if admin_exists:
            return

        session.add(
            User(
                name="System Admin",
                email="admin@medscope.local",
                password_hash=generate_password_hash("Admin@12345"),
                role="admin",
            )
        )
