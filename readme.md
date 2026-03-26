# 🛡️ Network Security Monitoring Dashboard

## 📌 Overview

This project is a **Network Security Monitoring Dashboard** that captures real-time network traffic, analyzes it, and detects suspicious activities such as abnormal traffic spikes. The system provides a graphical interface to visualize traffic and alerts, helping users monitor network behavior effectively.

---

## 🎯 Objectives

* Capture real-time network traffic
* Analyze traffic patterns
* Detect suspicious activities
* Display results through a user-friendly dashboard
* Provide alerts for potential threats

---

## ⚙️ Features

* 📡 Packet capture using Scapy
* 📊 Real-time traffic monitoring
* 🚨 Suspicious activity detection
* 📈 Graphical visualization of traffic (Chart.js)
* 🔄 Auto-updating dashboard (AJAX-based)
* 🧭 Sidebar navigation for modular design

---

## 🏗️ System Architecture

```text
Packet Capture (Scapy)
        ↓
Traffic Logging (SQLite)
        ↓
Detection Engine (Python Rules)
        ↓
Flask Backend (API)
        ↓
Web Dashboard (HTML, CSS, JS)
```

---

## 🛠️ Tech Stack

| Component      | Technology Used       |
| -------------- | --------------------- |
| Backend        | Python (Flask)        |
| Packet Capture | Scapy                 |
| Database       | SQLite                |
| Frontend       | HTML, CSS, JavaScript |
| Visualization  | Chart.js              |

---

## 🔐 Security Techniques Used

* Traffic monitoring using packet sniffing
* Threshold-based anomaly detection
* Time-based traffic analysis
* Logging and alert generation

---

## 🚀 How to Run the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```python
from database import init_db
init_db()
```

### 3. Start Packet Capture (Run as Administrator)

```bash
python packet_capture.py
```

### 4. Run Flask Server

```bash
python app.py
```

### 5. Open Dashboard

```
http://127.0.0.1:5000
```

---

## 🧪 How It Works

1. Captures network packets using Scapy
2. Extracts IP, port, and protocol information
3. Stores logs in SQLite database
4. Applies detection rules to identify suspicious activity
5. Displays logs and alerts in dashboard
6. Updates UI automatically every few seconds

---

## 🚨 Detection Logic

* Detects IPs with excessive requests
* Identifies abnormal traffic spikes
* Generates alerts when threshold is exceeded

---

## 📸 Sample Output

* Real-time traffic logs
* Alerts for suspicious IP activity
* Graph showing request distribution

---

## ⚠️ Limitations

* Threshold-based detection may generate false positives
* Works best in controlled environments
* Requires administrator privileges for packet capture

---

## 🔮 Future Enhancements

* Port scan detection
* Machine learning-based anomaly detection
* User authentication system
* WebSocket-based real-time updates
* Multi-page dashboard navigation

---

## 👨‍💻 Authors

* Melvin Isaac I
* Monishkumar Balaji
* Nanda Kumar B

---

## 📄 License

This project is developed for academic purposes.
