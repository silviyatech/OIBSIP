import socket
import threading
from datetime import datetime


# ============================================================
# SERVER SETTINGS
# ============================================================

HOST = "127.0.0.1"
PORT = 5555


# ============================================================
# CLIENT STORAGE
# ============================================================

clients = {}
clients_lock = threading.Lock()


# ============================================================
# SEND MESSAGE TO ALL CLIENTS
# ============================================================

def broadcast(message, exclude_client=None):
    disconnected_clients = []

    with clients_lock:
        current_clients = list(clients.keys())

    for client in current_clients:
        if client == exclude_client:
            continue

        try:
            client.send(message.encode("utf-8"))
        except:
            disconnected_clients.append(client)

    for client in disconnected_clients:
        remove_client(client)


# ============================================================
# REMOVE CLIENT
# ============================================================

def remove_client(client):
    with clients_lock:
        username = clients.pop(client, None)

    try:
        client.close()
    except:
        pass

    if username:
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"[{timestamp}] {username} disconnected.")

        broadcast(
            f"[{timestamp}] {username} left the chat."
        )


# ============================================================
# HANDLE CLIENT
# ============================================================

def handle_client(client, address):

    try:
        # Receive username
        username = client.recv(1024).decode("utf-8").strip()

        if not username:
            username = "Guest"

        with clients_lock:
            clients[client] = username

        timestamp = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{timestamp}] {username} connected "
            f"from {address[0]}:{address[1]}"
        )

        # Send welcome message to the new client
        client.send(
            f"[{timestamp}] Connected to the chat server.".encode("utf-8")
        )

        # Inform other clients
        broadcast(
            f"[{timestamp}] {username} joined the chat.",
            exclude_client=client
        )

        # Receive messages
        while True:

            data = client.recv(1024)

            if not data:
                break

            message = data.decode("utf-8").strip()

            if not message:
                continue

            timestamp = datetime.now().strftime("%H:%M:%S")

            formatted_message = (
                f"[{timestamp}] {username}: {message}"
            )

            print(formatted_message)

            broadcast(formatted_message)

    except ConnectionResetError:
        pass

    except Exception as error:
        print(f"Client error: {error}")

    finally:
        remove_client(client)


# ============================================================
# START SERVER
# ============================================================

def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))

    server.listen()

    print("=" * 55)
    print("        PYTHON CHAT APPLICATION SERVER")
    print("=" * 55)
    print(f"Server running on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("Press Ctrl+C to stop the server.")
    print("=" * 55)

    try:

        while True:

            client, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )

            thread.start()

            with clients_lock:
                connected_count = len(clients)

            print(
                f"Active clients: {connected_count}"
            )

    except KeyboardInterrupt:

        print("\nServer shutting down...")

    finally:

        with clients_lock:
            current_clients = list(clients.keys())

        for client in current_clients:
            try:
                client.close()
            except:
                pass

        server.close()

        print("Server stopped.")


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    start_server()