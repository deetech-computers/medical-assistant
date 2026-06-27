from functools import wraps

from flask import Blueprint, redirect, render_template, request, session, url_for

from services.activity_service import record_activity
from services.auth_service import authenticate_user, create_user, get_user_by_id


auth_routes = Blueprint("auth_routes", __name__)


def current_user():
    user_id = session.get("user_id")
    return get_user_by_id(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user():
            return redirect(url_for("auth_routes.login"))
        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = current_user()
        if not user:
            return redirect(url_for("auth_routes.login"))
        if user["role"] != "admin":
            return redirect(url_for("main_routes.index"))
        return view(*args, **kwargs)

    return wrapped_view


@auth_routes.app_context_processor
def inject_current_user():
    return {"current_user": current_user()}


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        result = create_user(
            request.form.get("name", ""),
            request.form.get("email", ""),
            request.form.get("password", ""),
        )

        if result.get("error"):
            error = result["error"]
        else:
            session["user_id"] = result["user"]["id"]
            record_activity("register", "New user account")
            return redirect(url_for("main_routes.index"))

    return render_template("register.html", error=error)


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = authenticate_user(
            request.form.get("email", ""),
            request.form.get("password", ""),
        )

        if not user:
            error = "Invalid email or password."
        else:
            session["user_id"] = user["id"]
            record_activity("login", "User signed in")
            return redirect(url_for("main_routes.index"))

    return render_template("login.html", error=error)


@auth_routes.route("/logout")
def logout():
    record_activity("logout", "User signed out")
    session.clear()
    return redirect(url_for("main_routes.index"))
