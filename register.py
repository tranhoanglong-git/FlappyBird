import sqlite3
import bcrypt

def register_user(username, password):
    """Đăng kí: tạo tài khoản mới với username duy nhất, password được băm bằng bcrypt"""
    if not username or not password:
        return False, 'Missing username or password'
    try:
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    except Exception:
        return False, 'Password encryption error'
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username, password_hash) VALUES (?, ?)", (username, pw_hash))
        conn.commit()
        return True, 'Registration successful'
    except sqlite3.IntegrityError:
        return False, 'Name already exists'
    finally:
        conn.close()
