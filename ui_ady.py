import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from typing import Optional, Callable

class Connection:
    """Socket connection handler class with non-blocking receive functionality."""

    def __init__(self, ip: str, port: int,logger):
        """
        Initialize the Connection object.

        Args:
            ip: Target IP address
            port: Target port number
        """
        self.ip = ip
        self.port = port
        self.logger = logger
        self.socket: Optional[socket.socket] = None
        self._receive_thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.Lock()

    def connect(self) -> bool:
        """
        Create socket connection to the specified IP address and port.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)  # Set timeout

            # Establish connection
            self.socket.connect((self.ip, self.port))
            self.logger(f"Successfully connected to {self.ip}:{self.port}")
            return True

        except socket.error as e:
            self.logger(f"Connection error: {e}")
            self.socket = None
            return False

    def send(self, msg: str) -> bool:
        """
        Send message through the socket.

        Args:
            msg: Message to send as string

        Returns:
            bool: True if send successful, False otherwise
        """
        if not self.socket:
            self.logger("No active connection")
            return False

        try:
            # Encode and send string
            self.socket.send(msg.encode('utf-8'))
            self.logger(f"Message sent: {msg}")
            return True

        except socket.error as e:
            self.logger(f"Error sending message: {e}")
            return False

    def recv(self, callback: Callable[[str], None]) -> None:
        """
        Start a thread that continuously reads from the socket.
        Converts incoming messages to string and calls the callback function.

        Args:
            callback: Callback function to process received messages
        """
        if not self.socket:
            self.logger("No active connection")
            return

        if self._running:
            self.logger("Receive thread already running")
            return

        self._running = True
        self._receive_thread = threading.Thread(
            target=self._receive_loop,
            args=(callback,),
            daemon=True  # Daemon thread closes with main thread
        )
        self._receive_thread.start()
        self.logger("Receive thread started")

    def _receive_loop(self, callback: Callable[[str], None]) -> None:
        """
        Internal method running in thread to receive messages.

        Args:
            callback: Callback function for processed messages
        """
        buffer_size = 4096

        while self._running and self.socket:
            try:
                # Receive data (non-blocking for main thread)
                data = self.socket.recv(buffer_size)

                if not data:
                    # Connection closed by remote host
                    self.logger("Connection closed by remote host")
                    break

                # Decode data to string
                message = data.decode('utf-8')
                self.logger(f"Message received: {message}")

                # Call callback with received message
                try:
                    callback(message)
                except Exception as e:
                    self.logger(f"Error in callback execution: {e}")

            except socket.timeout:
                # Continue loop on timeout
                continue

            except socket.error as e:
                if self._running:  # Only log if we're still supposed to run
                    self.logger(f"Error receiving data: {e}")
                break

        self.logger("Receive thread stopped")

    def close(self) -> None:
        """
        Close the connection and stop the receive thread.
        """
        self._running = False

        if self.socket:
            try:
                self.socket.close()
                self.logger("Socket closed")
            except socket.error as e:
                self.logger(f"Error closing socket: {e}")
            finally:
                self.socket = None

        # Wait for thread to finish
        if self._receive_thread and self._receive_thread.is_alive():
            self._receive_thread.join(timeout=2.0)

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - guaranteed connection closure."""
        self.close()

    @property
    def is_connected(self) -> bool:
        """Return whether there is an active connection."""
        return self.socket is not None and self._running


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.connection: Optional[Connection] = None
        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface with grid layout."""
        self.geometry("500x600")
        self.set_title("Socket Tester")

        # Configure grid weights for responsive layout
        self.grid_columnconfigure(1, weight=1)  # Entry column expands
        self.grid_columnconfigure(2, weight=0)  # Button column fixed
        self.grid_rowconfigure(4, weight=1)  # Memo row expands

        # Connection frame (row 0)
        # IP Address
        tk.Label(self, text="IP:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ip_entry = tk.Entry(self, width=15)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.ip_entry.insert(0, "127.0.0.1")  # Default value

        # Port
        tk.Label(self, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.port_entry = tk.Entry(self, width=8)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.port_entry.insert(0, "8080")  # Default value

        # Connect button
        self.connect_btn = tk.Button(
            self,
            text="Connect",
            command=self._toggle_connection,
            bg="lightblue"
        )
        self.connect_btn.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # HTTP Method buttons (row 1)
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")

        self.get_btn = tk.Button(
            button_frame,
            text="GET",
            command=self._send_get,
            width=10,
            state="disabled"
        )
        self.get_btn.pack(side="left", padx=5)

        self.post_btn = tk.Button(
            button_frame,
            text="POST",
            command=self._send_post,
            width=10,
            state="disabled"
        )
        self.post_btn.pack(side="left", padx=5)

        # Message entry (row 2)
        tk.Label(self, text="Message:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.message_entry = tk.Text(self, height=3, width=40)
        self.message_entry.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="ew")

        # Send button (row 3)
        self.send_btn = tk.Button(
            self,
            text="Send Message",
            command=self._send_message,
            state="disabled"
        )
        self.send_btn.grid(row=3, column=1, columnspan=2, pady=5)

        # Response display (row 4) - expands with window
        tk.Label(self, text="Response:").grid(row=4, column=0, padx=5, pady=5, sticky="nw")

        self.response_memo = scrolledtext.ScrolledText(
            self,
            height=15,
            width=50,
            wrap=tk.WORD
        )
        self.response_memo.grid(row=4, column=1, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Status bar (row 5)
        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        self.status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=5, column=0, columnspan=5, sticky="ew")

    def _toggle_connection(self):
        """Toggle connection state (connect/disconnect)."""
        if self.connection and self.connection.is_connected:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        """Establish socket connection."""
        ip = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()

        if not ip or not port_str:
            self._update_status("Please enter IP and port")
            return

        try:
            port = int(port_str)
        except ValueError:
            self._update_status("Invalid port number")
            return

        # Create connection in a separate thread to avoid UI freeze
        def connect_thread():
            self.connection = Connection(ip, port, self.logger)
            if self.connection.connect():
                # Start receiving thread
                self.connection.recv(self._on_message_received)

                # Update UI in main thread
                self.after(0, self._on_connect_success)
            else:
                self.after(0, lambda: self._update_status("Connection failed"))

        threading.Thread(target=connect_thread, daemon=True).start()
        self._update_status("Connecting...")

    def _on_connect_success(self):
        """Update UI after successful connection."""
        self.connect_btn.config(text="Disconnect", bg="lightcoral")
        self.get_btn.config(state="normal")
        self.post_btn.config(state="normal")
        self.send_btn.config(state="normal")
        self._update_status(f"Connected to {self.ip_entry.get()}:{self.port_entry.get()}")

    def _disconnect(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

        self.connect_btn.config(text="Connect", bg="lightblue")
        self.get_btn.config(state="disabled")
        self.post_btn.config(state="disabled")
        self.send_btn.config(state="disabled")
        self._update_status("Disconnected")

    def _send_get(self):
        """Send a simple GET request."""
        if self.connection and self.connection.is_connected:
            self.connection.send("GET / HTTP/1.1\r\n\r\n")
            self._update_status("GET request sent")

    def _send_post(self):
        """Send a simple POST request."""
        if self.connection and self.connection.is_connected:
            message = self.message_entry.get("1.0", tk.END).strip()
            if not message:
                message = "test data"

            post_request = f"POST / HTTP/1.1\r\nContent-Length: {len(message)}\r\n\r\n{message}"
            self.connection.send(post_request)
            self._update_status("POST request sent")

    def _send_message(self):
        """Send custom message."""
        if self.connection and self.connection.is_connected:
            message = self.message_entry.get("1.0", tk.END).strip()
            if message:
                self.connection.send(message)
                self._update_status("Message sent")
            else:
                self._update_status("Please enter a message")

    def _on_message_received(self, message: str):
        """
        Callback for received messages.
        Updates the response memo in the main thread.

        Args:
            message: Received message
        """
        parsed = message
        if message.startswith("HTTP/1.1"):
            parsed = self.parse_http_response(message)

        def update_ui():
            self.response_memo.insert(tk.END, f"Received: {message}\n")
            self.response_memo.see(tk.END)  # Auto-scroll to bottom
            self._update_status("Message received")

        self.after(0, update_ui)

    def parse_http_response(self, response):
        """Parse HTTP response and return wit headers and
        os, web server and content manager type"""
        parts = response.split("\r\n\r\n")
        new_msg = ""
        headers = parts[0]
        for header in headers.split("\r\n"):
            key_value = header.split(": ")
            if len(key_value) >= 2:
                key = key_value[0]
                if key.upper() == "SERVER":
                    new_msg += f"Find Server: {key_value[1]}"

        body = parts[1] if len(parts) > 1 else ""
        return new_msg

    def logger(self,msg):
        self.response_memo.insert(tk.END, f"Logging: {msg}\n")
        self.response_memo.see(tk.END)

    def _update_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(message)

    def set_title(self, title="Window title"):
        """Set the window title."""
        self.title(title)

    def run(self):
        """Start the application main loop."""
        self.mainloop()


# Usage example:
if __name__ == "__main__":
    app = App()
    app.run()