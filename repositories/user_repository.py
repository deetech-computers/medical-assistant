from services.database_service import get_connection


def find_by_email(email):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        ).fetchone()


def find_by_id(user_id):
    with get_connection() as connection:
        return connection.execute(
            "SELECT id, name, email, role, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()


def email_exists(email):
    with get_connection() as connection:
        return connection.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,),
        ).fetchone()


def create(name, email, password_hash):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash),
        )

        return cursor.lastrowid


def list_all_with_diagnosis_count():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT users.id, users.name, users.email, users.role, users.created_at,
                   COUNT(diagnoses.id) AS diagnosis_count
            FROM users
            LEFT JOIN diagnoses ON diagnoses.user_id = users.id
            GROUP BY users.id
            ORDER BY users.created_at DESC
            """
        ).fetchall()
