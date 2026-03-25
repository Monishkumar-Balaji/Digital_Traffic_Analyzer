import sqlite3
# print(sqlite3.sqlite_version)

def init_db():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        port INTEGER,
        protocol TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_log(ip, port, protocol):
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (ip, port, protocol) VALUES (?, ?, ?)", (ip, port, protocol))
    conn.commit()
    conn.close()


def insert_alert(message):
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    c.execute("INSERT INTO alerts (message) VALUES (?)", (message,))
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