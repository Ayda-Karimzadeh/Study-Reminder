import sqlite3

DB_NAME = 'study.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            learn_date TEXT,
            review_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_topic(title, learn_date, review_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO topics (title, learn_date, review_date)
        VALUES (?, ?, ?)
        ''',
        (title, learn_date, review_date))
    conn.commit()
    conn.close()

def get_review(today):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM topics WHERE review_date = ?
        ''',
        (today,))
    result = cursor.fetchall()
    conn.close()
    return result