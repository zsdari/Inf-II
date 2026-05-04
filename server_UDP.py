import socket

HOST = '0.0.0.0'
PORT = 23456

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((HOST, PORT))

print(f"UDP szerver {HOST}:{PORT}-on var")
while True:
    data, addr = s.recvfrom(1024)
    msg = data.decode('utf-8')
    print(f"Kaptam {addr}-tól: {msg}")
    s.sendto("Uzenetet fogadtam".encode('utf-8'), addr)