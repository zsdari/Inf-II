"""
TCP - 3 handshake - van visszacsatolás, visszaigazolás
UDP - nem fontos, hogy minden megérkezzen, broadcastba szór, 2 handshake
HTTP
HTTPS
SSL
ARP
+par dolog innen zh-ba belecsempeszve
"""

import socket

HOST = "0.0.0.0"
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

s.listen(5)
print(f'[*] Server Listening {HOST}:{PORT}')

conn, addr = s.accept()
print(f'[*] Connected to: {addr}')

data = conn.recv(1024)
print(f'[*] Received: {data}')

result = "Msg received!"
conn.sendall(result.encode('utf-8'))

conn.close()