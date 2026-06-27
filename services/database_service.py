import sqlite3
from pathlib import Path

from flask import current_app, has_app_context
from werkzeug.security import generate_password_hash


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "medscope.db"


def get_database_path():
    if has_app_context():
        return Path(current_app.config["DATABASE_PATH"])
    return DB_PATH


def get_connection():
    connection = sqlite3.connect(get_database_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                disease TEXT NOT NULL,
                confidence INTEGER,
                symptoms TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT NOT NULL,
                details TEXT,
                path TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
        )

        admin_exists = connection.execute(
            "SELECT id FROM users WHERE role = 'admin' LIMIT 1"
        ).fetchone()

        if not admin_exists:
            connection.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    "System Admin",
                    "admin@medscope.local",
                    generate_password_hash("Admin@12345"),
                    "admin",
                ),
            )
