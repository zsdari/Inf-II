import socket
import threading

class TCPServer:

    def __init__(self, host = "localhost", port = 10000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True
        print(f"Server listening on {self.host}:{self.port}")

        while self.running:
            client_socket, client_address = self.socket.accept()
            print(f"Accepted connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                text = data.decode('utf-8').strip()
                response = text.upper()
                client_socket.sendall(response.encode('utf-8'))
        print(f"Connection closed")

if __name__ == "__main__":
    server = TCPServer()
    server.start()
