import time
import threading
import random
from database import insert_log
from detector import detect_suspicious

def _simulate_ssh_bruteforce():
    end_time = time.time() + 5
    malicious_ip = "203.0.113.44"
    while time.time() < end_time:
        insert_log(ip=malicious_ip, port=22, protocol="TCP", size=random.randint(64, 128))
        detect_suspicious(malicious_ip, 22)
        time.sleep(0.06)

def _simulate_ddos_spike():
    end_time = time.time() + 5
    target_ports = [80, 443]
    while time.time() < end_time:
        spoofed_ip = f"150.150.150.{random.randint(1, 5)}"
        port = random.choice(target_ports)
        insert_log(ip=spoofed_ip, port=port, protocol="TCP", size=random.randint(500, 1500))
        detect_suspicious(spoofed_ip, port)
        time.sleep(0.03)

def start_ssh_bruteforce():
    threading.Thread(target=_simulate_ssh_bruteforce, daemon=True).start()
    return True

def start_ddos_spike():
    threading.Thread(target=_simulate_ddos_spike, daemon=True).start()
    return True
