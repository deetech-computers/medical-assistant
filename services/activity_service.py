from flask import request, session

from repositories import activity_repository


def record_activity(event_type, details=None, user_id=None, path=None):
    active_user_id = user_id if user_id is not None else session.get("user_id")
    active_path = path if path is not None else request.path
    activity_repository.create(active_user_id, event_type, details, active_path)


def list_recent_activities(limit=40):
    return activity_repository.list_recent(limit)


def activity_summary():
    return activity_repository.summary()
