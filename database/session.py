from contextlib import contextmanager

from flask import current_app, has_app_context
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_config
from database.models import Base


_engines = {}
_session_factories = {}


def get_database_uri():
    if has_app_context():
        return current_app.config["SQLALCHEMY_DATABASE_URI"]

    return get_config().SQLALCHEMY_DATABASE_URI


def get_engine():
    database_uri = get_database_uri()

    if database_uri not in _engines:
        connect_args = {"check_same_thread": False} if database_uri.startswith("sqlite") else {}
        _engines[database_uri] = create_engine(
            database_uri,
            future=True,
            pool_pre_ping=True,
            connect_args=connect_args,
        )

    return _engines[database_uri]


def get_session_factory():
    database_uri = get_database_uri()

    if database_uri not in _session_factories:
        _session_factories[database_uri] = sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
            future=True,
        )

    return _session_factories[database_uri]


@contextmanager
def database_session():
    session = get_session_factory()()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_schema():
    Base.metadata.create_all(bind=get_engine())
