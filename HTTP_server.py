import socket
import json

HOST = ''
PORT = 23456

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print("Waiting for connection")

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    print("Request:", request)
    if not request:
        conn.close()
        continue

    # Válasz törzse: egy egyszerű JSON objektum
    response_body = json.dumps({"status": "ok", "message": "Server received request"})

    # HTTP válasz összeállítása (egyetlen string)
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json; charset=utf-8\r\n"
        f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{response_body}"
    )

    conn.sendall(response.encode('utf-8'))
    conn.close()