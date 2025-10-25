import sqlite3

def get_top_leaderboard(limit=10):
    """Lấy danh sách top người chơi theo high_score (giảm dần)"""
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT username, high_score FROM users ORDER BY high_score DESC, id ASC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
