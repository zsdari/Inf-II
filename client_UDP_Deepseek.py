import socket

SERVER_HOST = '127.0.0.1'  # Ha a szerver ugyanazon a gépen fut
SERVER_PORT = 23456

# Üzenet, amit küldeni szeretnénk
uzenet = "Pina"

# UDP socket létrehozása
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Üzenet küldése a szervernek
    client_socket.sendto(uzenet.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
    print(f"Küldött üzenet: {uzenet}")

    # Válasz fogadása (max 1024 bájt)
    valasz, szerver_cim = client_socket.recvfrom(1024)
    print(f"Válasz a szervertől ({szerver_cim}): {valasz.decode('utf-8')}")

finally:
    client_socket.close()