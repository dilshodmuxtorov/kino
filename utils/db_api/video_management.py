import sqlite3



def add_video_db(file_id, caption):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO videos (video_id, caption) VALUES (?, ?)
        ''', (file_id, caption))

    conn.commit()
    conn.close()

def get_video(movie_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT video_id, caption FROM videos WHERE id = ? ;
        ''', (movie_code))

    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result