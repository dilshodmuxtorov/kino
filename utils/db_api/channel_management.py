import sqlite3

def get_channels_from_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM channels')
    channels = cursor.fetchall()
    conn.close()
    return [channel[0] for channel in channels]

def delete_channel_from_database(channel_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM channels WHERE channel_id = ?', (channel_id,))
    conn.commit()
    conn.close()

def clear_videos_and_channels():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM videos')
    
        cursor.execute('DELETE FROM channels')
        
        conn.commit()
    finally:
        conn.close()