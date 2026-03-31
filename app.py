from flask import Flask, render_template, jsonify
from database import get_logs, get_alerts, init_db
import sqlite3
from collections import Counter
import threading
from traffic_generator import start_ssh_bruteforce, start_ddos_spike
import time
import socket

app = Flask(__name__)

init_db()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/simulate_ssh", methods=["POST"])
def simulate_ssh():
    success = start_ssh_bruteforce()
    return jsonify({"success": success, "message": "SSH Brute Force Started (5s)"})

@app.route("/api/simulate_ddos", methods=["POST"])
def simulate_ddos():
    success = start_ddos_spike()
    return jsonify({"success": success, "message": "DDoS Spike Started (5s)"})

@app.route("/api/reset", methods=["POST"])
def reset():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()
    c.execute("DELETE FROM logs")
    c.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()
    return jsonify({"success": True})

def get_siem_metrics():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM logs WHERE timestamp >= datetime('now', '-10 seconds', 'localtime')")
    recent_packets = c.fetchone()[0]
    packets_per_sec = max(1, recent_packets // 10) if recent_packets > 0 else 0

    c.execute("SELECT COUNT(*) FROM alerts")
    active_alerts = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT ip) FROM logs") 
    tracked_ips = c.fetchone()[0]
    target_ports = [22, 80, 443, 3389, 53, 8080]
    placeholders = ','.join('?' * len(target_ports))
    c.execute(f"SELECT port, COUNT(*) FROM logs WHERE timestamp >= datetime('now', '-60 seconds', 'localtime') AND port IN ({placeholders}) GROUP BY port", target_ports)
    port_data = dict(c.fetchall())
    port_distribution = [port_data.get(p, 0) for p in target_ports]
    
    conn.close()

    return {
        "packets_per_sec": packets_per_sec,
        "active_alerts": active_alerts,
        "tracked_ips": tracked_ips,
        "port_distribution": port_distribution
    }

@app.route("/data")
def data():
    return jsonify({
        "logs": get_logs()[:50], 
        "alerts": get_alerts(),
        "metrics": get_siem_metrics()
    })

@app.route("/logs_page")
def logs_page():
    return render_template("logs.html")

@app.route("/alerts_page")
def alerts_page():
    return render_template("alerts.html")



if __name__ == "__main__":
    app.run(debug=True)