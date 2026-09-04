import sqlite3
def init_db():
    connection = sqlite3.connect("conversations.db")
    conn = connection.cursor()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS messages(
    PID INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL)
    """)
    connection.commit()
    connection.close()

def save_messages(role,content):
    connection = sqlite3.connect("conversations.db")
    conn = connection.cursor()
    conn.execute(
                "INSERT INTO messages(role,content) VALUES (?,?)",(role,content))
    connection.commit()
    connection.close()

def load_messages():
    connection = sqlite3.connect("conversations.db")
    conn = connection.cursor()
    conn.execute("SELECT role,content from messages ORDER BY PID")
    messages = conn.fetchall()
    connection.close()
    return messages

def delete_messages():
    connection = sqlite3.connect("conversations.db")
    conn = connection.cursor()
    conn.execute("DELETE FROM MESSAGES")
    connection.commit()
    connection.close()

