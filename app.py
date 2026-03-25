from flask import Flask, render_template
from database import get_logs, get_alerts, init_db
import sqlite3
from collections import Counter
from flask import jsonify


app = Flask(__name__)

# Initialize DB automatically
init_db()

@app.route("/data")
def data():
    return jsonify({
        "logs": get_logs(),
        "alerts": get_alerts(),
        "ip_stats": get_ip_stats()
    })

@app.route("/")
def dashboard():
    logs = get_logs()
    alerts = get_alerts()
    ip_stats = get_ip_stats()

    return render_template("dashboard.html", logs=logs, alerts=alerts, ip_stats=ip_stats)


def get_ip_stats():
    conn = sqlite3.connect("network.db")
    c = conn.cursor()

    c.execute("SELECT ip FROM logs")
    data = c.fetchall()
    conn.close()

    ips = [row[0] for row in data]
    count = Counter(ips)

    return dict(count)



if __name__ == "__main__":
    app.run(debug=True)

    