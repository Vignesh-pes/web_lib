from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt
from database import get_db_connection

member_bp = Blueprint("member", __name__, url_prefix="/member")


@member_bp.route("/dashboard")
@jwt_required()
def dashboard():
    claims = get_jwt()
    if claims["role"] != "member":
        return "Forbidden", 403

    return render_template("member/dashboard.html")


@member_bp.route("/books")
@jwt_required()
def books():
    claims = get_jwt()
    if claims["role"] != "member":
        return "Forbidden", 403

    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books WHERE available = 1").fetchall()
    conn.close()

    return render_template("member/books.html", books=books)
