from scapy.all import sniff, IP, TCP, UDP
from database import insert_log
from detector import detect_suspicious

def process_packet(packet):
    print("Packet received")   # 👈 MUST see this

    if IP in packet:
        ip = packet[IP].src
        print("IP:", ip)

        protocol = "OTHER"
        port = 0

        if TCP in packet:
            protocol = "TCP"
            port = packet[TCP].dport
        elif UDP in packet:
            protocol = "UDP"
            port = packet[UDP].dport

        insert_log(ip, port, protocol)
        detect_suspicious(ip)

def start_sniffing():
    sniff(iface="Wi-Fi", prn=process_packet, store=False)

if __name__ == "__main__":
    print("Starting packet capture...")
    start_sniffing()