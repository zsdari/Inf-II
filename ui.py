import socket
import threading
from typing import Optional, Callable
import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk  # Add this import for Separator


class Connection:
    """TCP connection handler class using socket module."""

    def __init__(self, ip: str, port: int):
        """
        Initialize the connection object.

        Args:
            ip: Target IP address
            port: Target port number
        """
        self.ip = ip
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.receive_thread: Optional[threading.Thread] = None
        self.is_connected = False
        self.running = False
        self.buffer_size = 4096

    def connect(self) -> bool:
        """
        Establish connection to the remote server.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.is_connected = True
            self.running = True
            print(f"Connected to: {self.ip}:{self.port}")
            return True
        except (socket.error, ConnectionRefusedError) as e:
            print(f"Connection error: {e}")
            self.is_connected = False
            return False

    def send(self, msg: str) -> bool:
        """
        Send a message through the connection.

        Args:
            msg: Message to send as string

        Returns:
            bool: True if send successful, False otherwise
        """
        if not self.is_connected or self.socket is None:
            print("No active connection")
            return False

        try:
            # Send message with UTF-8 encoding
            self.socket.sendall(msg.encode('utf-8'))
            return True
        except socket.error as e:
            print(f"Error sending message: {e}")
            self.is_connected = False
            return False

    def receive(self, callback: Callable[[str], None]) -> None:
        """
        Start a thread that continuously listens for incoming messages.

        Args:
            callback: Function to call with each received message
        """
        if not self.is_connected or self.socket is None:
            print("No active connection for receiving")
            return

        if self.receive_thread is not None and self.receive_thread.is_alive():
            print("Receive thread already running")
            return

        self.running = True
        self.receive_thread = threading.Thread(
            target=self._receive_loop,
            args=(callback,),
            daemon=True,  # Daemon thread automatically stops when main program exits
            name="ReceiveThread"
        )
        self.receive_thread.start()
        print("Receive thread started")

    def _receive_loop(self, callback: Callable[[str], None]) -> None:
        """
        Internal method: main loop for the receiving thread.

        Args:
            callback: Function to call with each received message
        """
        while self.running and self.is_connected:
            try:
                # Receive data from socket
                data = self.socket.recv(self.buffer_size)

                # If no data (connection closed)
                if not data:
                    print("Connection closed by remote server")
                    self.is_connected = False
                    break

                # Decode and call callback
                message = data.decode('utf-8')
                callback(message)

            except socket.timeout:
                # Continue loop on timeout
                continue
            except socket.error as e:
                print(f"Error receiving data: {e}")
                self.is_connected = False
                break
            except UnicodeDecodeError as e:
                print(f"Error decoding message: {e}")
                # Continue trying to receive next message
                continue

    def close(self) -> None:
        """
        Close connection and free resources.
        """
        print("Closing connection...")
        self.running = False
        self.is_connected = False

        # Wait for receive thread to finish
        if self.receive_thread is not None and self.receive_thread.is_alive():
            self.receive_thread.join(timeout=2.0)

        # Close socket
        if self.socket is not None:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except socket.error:
                pass  # Ignore if already closed
            finally:
                self.socket = None

        print("Connection closed")

    def __enter__(self):
        """Context manager entry point."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - ensures connection is closed."""
        self.close()
        return False  # Don't suppress exceptions


class App():
    def __init__(self, root):
        self.root = root
        self.connection = None
        self._init_ui()

    def _init_ui(self):
        # Window settings
        self.root.geometry("500x500")
        self.set_title("Socket Tester")

        # Configure grid weights for resizing
        self.root.grid_rowconfigure(3, weight=1)  # Make memo row expandable
        self.root.grid_columnconfigure(1, weight=1)  # Make entry columns expandable

        # Connection Frame
        # IP Address
        tk.Label(self.root, text="IP Address:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.ip_entry = tk.Entry(self.root, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.ip_entry.insert(0, "127.0.0.1")  # Default value

        # Port
        tk.Label(self.root, text="Port:").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )
        self.port_entry = tk.Entry(self.root, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.port_entry.insert(0, "8080")  # Default value

        # Connect Button
        self.connect_btn = tk.Button(
            self.root,
            text="Connect",
            command=self._toggle_connection,
            bg="lightblue"
        )
        self.connect_btn.grid(row=0, column=4, padx=5, pady=5)

        # Separator
        ttk.Separator(self.root, orient='horizontal').grid(
            row=1, column=0, columnspan=5, sticky="ew", pady=10
        )

        # HTTP Request Frame
        # GET Button
        self.get_btn = tk.Button(
            self.root,
            text="GET",
            command=self._send_get,
            bg="lightgreen",
            state="disabled"  # Disabled until connected
        )
        self.get_btn.grid(row=2, column=0, padx=5, pady=5)

        # POST Button
        self.post_btn = tk.Button(
            self.root,
            text="POST",
            command=self._send_post,
            bg="lightyellow",
            state="disabled"  # Disabled until connected
        )
        self.post_btn.grid(row=2, column=1, padx=5, pady=5)

        # Message Entry (for POST data or custom messages)
        tk.Label(self.root, text="Message:").grid(
            row=2, column=2, padx=5, pady=5, sticky="w"
        )
        self.message_entry = tk.Entry(self.root)
        self.message_entry.grid(row=2, column=3, columnspan=2, padx=5, pady=5, sticky="ew")
        self.message_entry.insert(0, "Hello Server!")

        # Memo (ScrolledText for received messages)
        tk.Label(self.root, text="Received Messages:").grid(
            row=3, column=0, padx=5, pady=(10, 0), sticky="sw"
        )

        self.memo = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=60,
            height=15
        )
        self.memo.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        self.status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=4, column=0, columnspan=5, sticky="ew")

    def _toggle_connection(self):
        """Connect or disconnect from server."""
        if self.connection and self.connection.is_connected:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        """Establish connection to the server."""
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()

        if not ip or not port:
            self._update_memo("Error: IP and Port are required!")
            return

        try:
            port = int(port)
        except ValueError:
            self._update_memo("Error: Port must be a number!")
            return

        # Create connection
        self.connection = Connection(ip, port)

        # Try to connect in a separate thread to not block GUI
        def connect_thread():
            if self.connection.connect():
                self.root.after(0, self._on_connect_success)
            else:
                self.root.after(0, self._on_connect_failure)

        self._update_memo(f"Connecting to {ip}:{port}...")
        thread = threading.Thread(target=connect_thread, daemon=True)
        thread.start()

    def _on_connect_success(self):
        """Handle successful connection."""
        self._update_memo("Connected successfully!")
        self.status_var.set(f"Connected to {self.connection.ip}:{self.connection.port}")
        self.connect_btn.config(text="Disconnect", bg="lightcoral")
        self.get_btn.config(state="normal")
        self.post_btn.config(state="normal")

        # Start receiving messages
        self.connection.receive(self._handle_received_message)

    def _on_connect_failure(self):
        """Handle connection failure."""
        self._update_memo("Connection failed!")
        self.status_var.set("Disconnected")
        self.connection = None

    def _disconnect(self):
        """Disconnect from server."""
        if self.connection:
            self.connection.close()
            self.connection = None

        self._update_memo("Disconnected")
        self.status_var.set("Disconnected")
        self.connect_btn.config(text="Connect", bg="lightblue")
        self.get_btn.config(state="disabled")
        self.post_btn.config(state="disabled")

    def _send_get(self):
        """Send GET request."""
        if not self.connection or not self.connection.is_connected:
            self._update_memo("Error: Not connected!")
            return

        # Simple GET request simulation
        message = self.message_entry.get().strip() or "GET / HTTP/1.1"
        if self.connection.send(message):
            self._update_memo(f"GET sent: {message}")
        else:
            self._update_memo("Error sending GET request")
            self._disconnect()

    def _send_post(self):
        """Send POST request with data."""
        if not self.connection or not self.connection.is_connected:
            self._update_memo("Error: Not connected!")
            return

        # Simple POST request simulation
        data = self.message_entry.get().strip()
        if not data:
            data = "Hello Server!"

        message = f"POST / HTTP/1.1\r\nContent-Length: {len(data)}\r\n\r\n{data}"
        if self.connection.send(message):
            self._update_memo(f"POST sent with data: {data}")
        else:
            self._update_memo("Error sending POST request")
            self._disconnect()

    def _handle_received_message(self, message: str):
        """Handle received messages from the connection."""
        # Use after() to safely update GUI from thread
        self.root.after(0, self._update_memo, f"Received: {message}")

    def _update_memo(self, message: str):
        """Add message to the memo widget."""
        self.memo.insert(tk.END, f"{message}\n")
        self.memo.see(tk.END)  # Auto-scroll to bottom

    def set_title(self, title="Window title"):
        """Set the window title."""
        self.root.title(title)

    def run(self):
        """Start the GUI application."""

        # Handle window closing
        def on_closing():
            if self.connection:
                self.connection.close()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()