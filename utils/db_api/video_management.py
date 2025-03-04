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
        SELECT video_id, caption FROM videos WHERE id=? ;
        ''', (movie_code,))

    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def delete_video(movie_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM videos WHERE id=?; 
    """, (movie_code,))

    result= cursor.fetchall()
    if result == []:
        return False
    else:
        cursor.execute("""
        DELETE FROM videos WHERE id=?; 
        """, (movie_code,))

        conn.commit()
        conn.close()
        return True
    
def get_channels():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT channel_id FROM channels;
    """)    

    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def add_channel(channel_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO channels (channel_id) VALUES (?)
    """, (channel_id,))

    conn.commit()
    conn.close()

def is_channel_in_database(channel_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM channels WHERE channel_id = ?', (channel_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
