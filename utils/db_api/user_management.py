import sqlite3



def add_user(user_id, username, fullname):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, fullname, is_active) VALUES (?, ?, ?, 1)
        ''', (user_id, username, fullname))

    conn.commit()
    conn.close()

def get_all_user():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM users;
        ''')
    result = cursor.fetchall()

    conn.commit()
    conn.close()
    return result