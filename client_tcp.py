import socket

HOST = "127.0.0.1"
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

msg = "Msg for u"
s.sendall(msg.encode('utf-8'))

data = s.recv(1024)

s.close()