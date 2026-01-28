from flask import Blueprint, render_template, request, redirect, url_for
from auth import require_role
from database import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@require_role("admin")
def dashboard(decoded):
    return render_template(
        "admin/dashboard.html",
        user=decoded["user"],
        role=decoded["role"],
    )


@admin_bp.route("/books")
@require_role("admin")
def view_books(decoded):
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template(
        "admin/books.html",
        books=books,
        user=decoded["user"],
    )


@admin_bp.route("/books/add", methods=["POST"])
@require_role("admin")
def add_book(decoded):
    title = request.form["title"]
    author = request.form["author"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin.view_books"))
