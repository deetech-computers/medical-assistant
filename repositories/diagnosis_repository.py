from services.database_service import get_connection


def create(user_id, disease, confidence, symptoms):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO diagnoses (user_id, disease, confidence, symptoms)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, disease, confidence, symptoms),
        )

        return cursor.lastrowid


def list_by_user(user_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT * FROM diagnoses
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()


def list_recent(limit=40):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT diagnoses.*, users.name, users.email
            FROM diagnoses
            LEFT JOIN users ON users.id = diagnoses.user_id
            ORDER BY diagnoses.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
