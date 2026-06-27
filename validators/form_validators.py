import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_registration_form(name, email, password):
    clean_name = name.strip()
    clean_email = email.strip().lower()

    if not clean_name or not clean_email or not password:
        return None, "All fields are required."

    if len(clean_name) < 2:
        return None, "Enter a valid full name."

    if not EMAIL_PATTERN.match(clean_email):
        return None, "Enter a valid email address."

    if len(password) < 8:
        return None, "Password must be at least 8 characters."

    return {
        "name": clean_name,
        "email": clean_email,
        "password": password,
    }, None


def validate_login_form(email, password):
    clean_email = email.strip().lower()

    if not clean_email or not password:
        return None, "Email and password are required."

    if not EMAIL_PATTERN.match(clean_email):
        return None, "Enter a valid email address."

    return {
        "email": clean_email,
        "password": password,
    }, None
