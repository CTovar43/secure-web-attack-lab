import sqlite3
import bcrypt

DB_NAME = "app.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    # Notes table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# ------ PASSWORD SECURITY ------

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(
        plain_password.encode(),
        bcrypt.gensalt()
    ).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )

# ------ USER MANAGEMENT ------

def create_user(username: str, password: str, role: str = "user") -> bool:
    try:
        conn = get_db()
        cur = conn.cursor()
        hashed = hash_password(password)
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()



def ensure_admin_seed():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    exists = cur.fetchone()
    if not exists:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hash_password("adminpass"), "admin")
        )
        conn.commit()
    conn.close()


def find_user_secure(username: str, password: str):
    """
    Secure login with parameterized queries + bcrypt
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password, role FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if row and verify_password(password, row["password"]):
        return {
            "id": row["id"],
            "username": row["username"],
            "role": row["role"]
        }
    return None

# ------ NOTES ------

def create_note(user_id: int, content: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (user_id, content) VALUES (?, ?)",
        (user_id, content)
    )
    conn.commit()
    conn.close()


def get_notes_for_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, content, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_users_and_note_counts():
    """
    Used by /admin page.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.role, COUNT(n.id) AS note_count
        FROM users u
        LEFT JOIN notes n ON n.user_id = u.id
        GROUP BY u.id, u.username, u.role
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_id_by_username(username: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None
