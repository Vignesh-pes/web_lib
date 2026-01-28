from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    abort,
)
import jwt
import datetime
import bcrypt
from functools import wraps
from database import get_db_connection
from flask import current_app

auth_bp = Blueprint("auth", __name__)


def create_jwt(username, role):
    payload = {
        "user": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt(token):
    try:
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError:
        return None


def require_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("access_token")
            if not token:
                return redirect(url_for("auth.login"))

            decoded = decode_jwt(token)
            if not decoded or decoded["role"] != role:
                abort(403)

            return fn(decoded, *args, **kwargs)

        return wrapper

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,),
        ).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user["password"]):
            token = create_jwt(user["username"], user["role"])
            resp = make_response(
                redirect(
                    url_for(
                        "admin.dashboard"
                        if user["role"] == "admin"
                        else "member.dashboard"
                    )
                )
            )
            resp.set_cookie(
                "access_token",
                token,
                httponly=True,
                samesite="Lax",
            )
            return resp

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    resp.delete_cookie("access_token")
    return resp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.hashpw(
            request.form["password"].encode(),
            bcrypt.gensalt(),
        )
        role = request.form["role"]

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role),
            )
            conn.commit()
        except Exception:
            return render_template("register.html", error="User exists")
        finally:
            conn.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")
