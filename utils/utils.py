from validate_email import validate_email
import bcrypt


def validate_signup_data(data):
    errors = []
    error_message = " is required"
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if data[field] is None or data[field] == "":
            errors.append(field + error_message)
    if (validate_email(data["email"])):
        return errors
    else:
        errors.append("Email format is incorrect")
    return errors


def validate_login_data(data):
    errors = []
    error_message = " is required"
    required_fields = ["email", "password"]
    for field in required_fields:
        if data[field] is None or data[field] == "":
            errors.append(field + error_message)
    if (validate_email(data["email"])):
        return errors
    else:
        errors.append("Email format is incorrect")
    return errors


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def make_new_user_dict(username, email, hashed_password):
    return {
        "username": username,
        "email": email,
        "password": hashed_password,
        "todos": []
    }
