from scapy.all import sniff, IP, TCP, UDP
from database import insert_log, init_db
from detector import detect_suspicious

def process_packet(packet):
    print("Packet received") 
    if IP in packet:
        ip = packet[IP].src
        print("IP:", ip)

        protocol = "OTHER"
        port = 0
        size = len(packet)  # Track the packet size in bytes

        if TCP in packet:
            protocol = "TCP"
            port = packet[TCP].dport
        elif UDP in packet:
            protocol = "UDP"
            port = packet[UDP].dport

        # To avoid UI errors when checking 'size' in javascript, wrap this in try-except 
        # just in case the size column doesn't match perfectly. But the init_db fixes 99% of this.
        try:
            insert_log(ip, port, protocol, size)
        except Exception as e:
            print(f"DB Insert Error: {e}")
            
        detect_suspicious(ip, port)

def start_sniffing():
    sniff(iface="Wi-Fi", prn=process_packet, store=False)

if __name__ == "__main__":
    print("Starting packet capture...")
    init_db()
    start_sniffing()