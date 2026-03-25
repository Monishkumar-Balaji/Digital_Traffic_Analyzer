from database import insert_alert
import sqlite3

THRESHOLD = 20  # requests

def detect_suspicious(ip):
    conn = sqlite3.connect("network.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM logs WHERE ip=?", (ip,))
    count = c.fetchone()[0]

    # Check if alert already exists
    c.execute("SELECT * FROM alerts WHERE message LIKE ?", (f"%{ip}%",))
    existing = c.fetchone()

    conn.close()

    if count > THRESHOLD and not existing:
        insert_alert(f"Suspicious activity detected from IP: {ip} ({count} requests)")