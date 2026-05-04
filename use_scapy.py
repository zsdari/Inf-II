from scapy.all import *

dest = "8.8.8.8"
packet = IP(dst=dest)/ICMP()

answer = sr1(packet, timeout=5)
if answer:
    print(f"{dest} is online, Answer: {answer}")
else:
    print(f"{dest} is offline, no answer were received!")