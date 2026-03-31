from database import insert_alert
import sqlite3

THRESHOLD = 20
import time
import datetime
import socket
import urllib.request
import json
from database import insert_alert
import sqlite3

THRESHOLD = 20
LOGIN_PORTS = {21: "FTP", 22: "SSH", 23: "Telnet", 3389: "RDP", 3306: "MySQL"}
LOGIN_THRESHOLD = 5

last_custom_alert_time = {}

def get_domain(ip):
    
    if ip == "127.0.0.1": return "Localhost"
    if ip == "255.255.255.255": return "Broadcast"
    
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.error:
        try:
            with urllib.request.urlopen(f"http://ip-api.com/json/{ip}", timeout=2) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "success":
                    return data.get("org") or data.get("isp") or "Unknown Domain"
        except Exception:
            pass
    return "Unknown Domain"

def detect_suspicious(ip, port=None):
    global last_custom_alert_time
    conn = sqlite3.connect("network.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM logs WHERE ip=?", (ip,))
    count = c.fetchone()[0]

    c.execute("SELECT * FROM alerts WHERE message LIKE ?", (f"Suspicious activity detected from IP: {ip} %",))
    existing_traffic_alert = c.fetchone()

    if count > THRESHOLD and not existing_traffic_alert:
        domain = get_domain(ip)
        insert_alert(f"Suspicious activity detected from IP: {ip}\nDomain: [{domain}]\n({count} requests)")

    if port and port in LOGIN_PORTS:
        c.execute("SELECT COUNT(*) FROM logs WHERE ip=? AND port=?", (ip, port))
        port_count = c.fetchone()[0]

        c.execute("SELECT * FROM alerts WHERE message LIKE ?", (f"Suspicious {LOGIN_PORTS[port]} login attempts from IP: {ip}\n%",))
        existing_login_alert = c.fetchone()

        if port_count > LOGIN_THRESHOLD and not existing_login_alert:
            domain = get_domain(ip)
            insert_alert(f"Suspicious {LOGIN_PORTS[port]} login attempts from IP: {ip}\nDomain: [{domain}]\n({port_count} attempts)")


    if port == 9999:
        now = time.time()
        
        if ip not in last_custom_alert_time or (now - last_custom_alert_time[ip]) > 3:
            last_custom_alert_time[ip] = now
            domain = get_domain(ip)
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            insert_alert(f" CUSTOM TRAFFIC DETECTED from IP: {ip}\nDomain: [{domain}]\nat {current_time} (Testing Mode)")

    conn.close()