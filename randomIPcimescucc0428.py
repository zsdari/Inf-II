"""
IP 10.7.64.116
"""
from scapy.all import sniff, get_if_list

def packet_callback(packet):
    print(packet.summary())
    if packet.haslayer(HTTPRequest):
        req = packet[HTTPRequest]
        if req.method and reg.method.decode() == "POST":
            if packet.haslayer(Raw):
                post_data = packet[Raw].load.decode("utf-8", errors="ignore")
                print(f"POST Data:{post_data}")

if __name__ == "__main__":
    print(get_if_list())
    sniff(prn=packet_callback, filter="tcp port 80")