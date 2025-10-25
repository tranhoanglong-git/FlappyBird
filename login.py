import sqlite3
import bcrypt

def init_db():
    """Khởi tạo bảng users nếu chưa có"""
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            high_score REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def login_user(username, password):
    """Đăng nhập: kiểm tra username tồn tại và so khớp mật khẩu (checkpw)"""
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    try:
        return bcrypt.checkpw(password.encode('utf-8'), row[0])
    except Exception:
        return False

def get_user_high_score(username):
    """Lấy điểm cao nhất của 1 người chơi"""
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT high_score FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0

def update_user_high_score(username, new_score):
    """Cập nhật điểm cao nhất (giữ giá trị lớn hơn giữa cũ và mới)"""
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET high_score = MAX(high_score, ?) WHERE username=?", (float(new_score), username))
    conn.commit()
    conn.close()
