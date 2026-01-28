from flask import Blueprint, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt
from database import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# -------- ADMIN DASHBOARD --------
@admin_bp.route("/dashboard")
@jwt_required()
def dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return "Forbidden", 403

    return render_template("admin/dashboard.html")


# -------- VIEW + ADD BOOKS --------
@admin_bp.route("/books", methods=["GET", "POST"])
@jwt_required()
def books():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return "Forbidden", 403

    conn = get_db_connection()

    # ADD BOOK (POST)
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin.books"))

    # VIEW BOOKS (GET)
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template("admin/books.html", books=books)
