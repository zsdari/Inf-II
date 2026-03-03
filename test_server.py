import socket
import threading


def handle_client(client_socket, address):
    """Handle individual client connections"""
    print(f"New connection from {address}")

    try:
        while True:
            # Receive data from client
            data = client_socket.recv(4096)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Received from {address}: {message}")

            # Send response back to client
            response = f"Server received: {message}"
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error with client {address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed from {address}")


def start_server(host='127.0.0.1', port=8080):
    """Start a test server"""

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind to address
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Test server listening on {host}:{port}")
        print("Press Ctrl+C to stop the server")

        while True:
            # Accept new connections
            client_socket, address = server_socket.accept()

            # Handle each client in a new thread
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        print("Server stopped")


if __name__ == "__main__":
    start_server()