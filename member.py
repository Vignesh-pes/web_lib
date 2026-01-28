from flask import Blueprint, render_template, redirect, url_for
from auth import require_role
from database import get_db_connection

member_bp = Blueprint("member", __name__, url_prefix="/member")


@member_bp.route("/dashboard")
@require_role("member")
def dashboard(decoded):
    return render_template(
        "member/dashboard.html",
        user=decoded["user"],
        role=decoded["role"],
    )


@member_bp.route("/books")
@require_role("member")
def view_books(decoded):
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books WHERE available = 1").fetchall()
    conn.close()

    return render_template(
        "member/books.html",
        books=books,
        user=decoded["user"],
    )
