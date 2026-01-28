from flask import Blueprint, render_template, request, redirect, url_for
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)
import bcrypt
from database import get_db_connection

auth_bp = Blueprint("auth", __name__)


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user["password"]):
            token = create_access_token(
                identity=user["username"],
                additional_claims={"role": user["role"]},
            )
            resp = redirect(
                url_for(
                    "admin.dashboard" if user["role"] == "admin" else "member.dashboard"
                )
            )
            set_access_cookies(resp, token)
            return resp

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()
        role = request.form["role"]

        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_db_connection()
        try:
            conn.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                (username, hashed_pw, role),
            )
            conn.commit()
        except Exception:
            conn.close()
            return render_template(
                "register.html",
                error="User already exists",
            )

        conn.close()
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    resp = redirect(url_for("auth.login"))
    unset_jwt_cookies(resp)
    return resp
