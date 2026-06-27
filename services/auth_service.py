from werkzeug.security import check_password_hash, generate_password_hash

from repositories import user_repository
from validators.form_validators import validate_login_form, validate_registration_form


def create_user(name, email, password):
    form_data, error = validate_registration_form(name, email, password)

    if error:
        return {"error": error}

    if user_repository.email_exists(form_data["email"]):
        return {"error": "An account with this email already exists."}

    user_id = user_repository.create(
        form_data["name"],
        form_data["email"],
        generate_password_hash(form_data["password"]),
    )
    return {"user": get_user_by_id(user_id)}


def authenticate_user(email, password):
    form_data, error = validate_login_form(email, password)

    if error:
        return None

    user = get_user_by_email(form_data["email"])

    if not user or not check_password_hash(user["password_hash"], form_data["password"]):
        return None

    return user


def get_user_by_email(email):
    return user_repository.find_by_email(email)


def get_user_by_id(user_id):
    return user_repository.find_by_id(user_id)


def list_users():
    return user_repository.list_all_with_diagnosis_count()
