import sqlite3

DB_NAME = "app.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # ❌ Plaintext password storage (intentional for now)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()


def create_user(username: str, password: str, role: str = "user") -> bool:
    """
    Returns True if created, False if username exists or insert fails.
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        try:
            conn.close()
        except Exception:
            pass


def find_user_insecure(username: str, password: str):
    """
    ❌ Intentionally vulnerable to SQL Injection via string concatenation.
    Returns a user row or None.
    """
    conn = get_db()
    cur = conn.cursor()

    # VULNERABILITY: user input is directly concatenated into SQL
    query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
    cur.execute(query)

    row = cur.fetchone()
    conn.close()
    return row
