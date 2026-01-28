import sqlite3

DB_name = "library.db"


def get_db_conection():
    conn = sqlite3.connect(DB_name)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_conection()
    cursor = conn.cursor()

    # Users table
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL,
                   role TEXT NOT NULL
                   )
                   """
    )
    # Books table
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS books (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   author TEXT NOT NULL,
                   available INTEGER DEFAULT 1
                   )
                   """
    )

    # Borrowed
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS borrowed_books(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   book_id INTEGER,
                   borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   """
    )

    conn.commit()
    conn.close()
