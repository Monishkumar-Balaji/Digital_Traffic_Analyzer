import sqlite3

def init_db():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        port INTEGER,
        protocol TEXT,
        size INTEGER DEFAULT 0,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Attempt to gracefully add the 'size' column if this is an old database
    try:
        c.execute("ALTER TABLE logs ADD COLUMN size INTEGER DEFAULT 0;")
    except sqlite3.OperationalError:
        pass # The column already exists

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


import datetime

def insert_log(ip, port, protocol, size=0):
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logs (ip, port, protocol, size, timestamp) VALUES (?, ?, ?, ?, ?)", (ip, port, protocol, size, local_time))
    conn.commit()
    conn.close()


def insert_alert(message):
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    local_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO alerts (message, timestamp) VALUES (?, ?)", (message, local_time))
    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 20")
    data = c.fetchall()
    conn.close()
    return data


def get_alerts():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    c.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10")
    data = c.fetchall()
    conn.close()
    return data