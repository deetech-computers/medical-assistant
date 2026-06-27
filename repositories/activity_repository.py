from services.database_service import get_connection


def create(user_id, event_type, details, path):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO activities (user_id, event_type, details, path)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, event_type, details, path),
        )


def list_recent(limit=40):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT activities.*, users.name, users.email
            FROM activities
            LEFT JOIN users ON users.id = activities.user_id
            ORDER BY activities.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()


def summary():
    with get_connection() as connection:
        return {
            "user_count": connection.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            "diagnosis_count": connection.execute(
                "SELECT COUNT(*) FROM diagnoses"
            ).fetchone()[0],
            "activity_count": connection.execute(
                "SELECT COUNT(*) FROM activities"
            ).fetchone()[0],
            "guest_diagnosis_count": connection.execute(
                "SELECT COUNT(*) FROM diagnoses WHERE user_id IS NULL"
            ).fetchone()[0],
        }
