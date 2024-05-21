from flask import Blueprint, render_template, Response, request, redirect, current_app
from routes.auth.service import generate_auth_code, confirm_auth_code

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET"])
def login_page():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login():
    return render_template("auth/login.html")


@auth.route("/register", methods=["GET"])
def register_page():
    return render_template("auth/register.html")


@auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if not username or not email or not password or password != confirm_password:
        error_message = "There was an error with your submission. Please ensure all fields are filled out and passwords match."
        return f'<div class="p-4 bg-red-100 border border-red-300 text-red-800 rounded-md">{error_message}</div>', 400

    user = current_app.db.users.find_one({"email": email})

    if user:
        error_message = "The User Exists"
        return f'<div class="p-4 bg-red-100 border border-red-300 text-red-800 rounded-md">{error_message}</div>', 400

    try:
        unique_code = generate_auth_code(
            username=username, password=password, email=email)
        response = Response()
        response.set_cookie("CACFHS", value=unique_code, max_age=3600, expires=3600, path='/', doauth=None,
                            secure=None, httponly=False)
        response.headers['HX-Redirect'] = "/confirm_account"
        return response
    except:
        error_message = "Email error"
        return f'<div class="p-4 bg-red-100 border border-red-300 text-red-800 rounded-md">{error_message}</div>', 400


@auth.route("/confirm_account", methods=["GET"])
def confirm_account_page():
    cookie = request.cookies.get('CACFHS')
    if (not cookie):
        return redirect("/register")
    return render_template("/auth/confirm_account.html")


@auth.route("/confirm_account", methods=["POST"])
def confirm_account():
    confirm_code = request.form.get("confirm_code")
    cookie = request.cookies.get('CACFHS')
    res = confirm_auth_code(unique_code=cookie, auth_code=confirm_code)

    if (res == True):
        response = Response()
        response.headers['HX-Redirect'] = "/"
        return response

    return res, 400
