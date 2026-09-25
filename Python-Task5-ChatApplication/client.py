import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# ============================================================
# SERVER SETTINGS
# ============================================================

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5555


# ============================================================
# GLOBAL VARIABLES
# ============================================================

client_socket = None
connected = False


# ============================================================
# ADD MESSAGE TO CHAT
# ============================================================

def add_message(message):

    chat_text.config(state="normal")

    chat_text.insert(
        tk.END,
        message + "\n"
    )

    chat_text.see(tk.END)

    chat_text.config(state="disabled")


# ============================================================
# CONNECT TO SERVER
# ============================================================

def connect_to_server():

    global client_socket
    global connected

    username = username_entry.get().strip()

    if not username:

        messagebox.showwarning(
            "Username Required",
            "Please enter your username."
        )

        return

    if connected:
        return

    try:

        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client_socket.connect(
            (SERVER_HOST, SERVER_PORT)
        )

        client_socket.send(
            username.encode("utf-8")
        )

        connected = True

        username_entry.config(
            state="disabled"
        )

        connect_button.config(
            state="disabled"
        )

        message_entry.config(
            state="normal"
        )

        send_button.config(
            state="normal"
        )

        disconnect_button.config(
            state="normal"
        )

        status_label.config(
            text="● Connected",
            fg="#198754"
        )

        add_message(
            "System: You are connected to the chat server."
        )

        receive_thread = threading.Thread(
            target=receive_messages,
            daemon=True
        )

        receive_thread.start()

    except ConnectionRefusedError:

        messagebox.showerror(
            "Connection Failed",
            "Could not connect to the server.\n\n"
            "Make sure server.py is running first."
        )

        if client_socket:
            client_socket.close()

        client_socket = None

    except Exception as error:

        messagebox.showerror(
            "Connection Error",
            f"Unable to connect:\n{error}"
        )

        if client_socket:
            client_socket.close()

        client_socket = None


# ============================================================
# RECEIVE MESSAGES
# ============================================================

def receive_messages():

    global connected

    try:

        while connected:

            data = client_socket.recv(4096)

            if not data:
                break

            message = data.decode("utf-8")

            root.after(
                0,
                add_message,
                message
            )

    except:

        pass

    finally:

        if connected:

            connected = False

            root.after(
                0,
                connection_lost
            )


# ============================================================
# CONNECTION LOST
# ============================================================

def connection_lost():

    global client_socket
    global connected

    connected = False

    username_entry.config(
        state="normal"
    )

    connect_button.config(
        state="normal"
    )

    message_entry.config(
        state="disabled"
    )

    send_button.config(
        state="disabled"
    )

    disconnect_button.config(
        state="disabled"
    )

    status_label.config(
        text="● Disconnected",
        fg="#dc3545"
    )

    add_message(
        "System: Connection to the server was lost."
    )

    client_socket = None


# ============================================================
# SEND MESSAGE
# ============================================================

def send_message(event=None):

    if not connected:
        return

    message = message_entry.get().strip()

    if not message:
        return

    try:

        client_socket.send(
            message.encode("utf-8")
        )

        message_entry.delete(
            0,
            tk.END
        )

    except Exception:

        messagebox.showerror(
            "Send Error",
            "Unable to send the message."
        )


# ============================================================
# DISCONNECT
# ============================================================

def disconnect():

    global client_socket
    global connected

    if not connected:
        return

    connected = False

    try:
        client_socket.shutdown(
            socket.SHUT_RDWR
        )
    except:
        pass

    try:
        client_socket.close()
    except:
        pass

    client_socket = None

    username_entry.config(
        state="normal"
    )

    connect_button.config(
        state="normal"
    )

    message_entry.config(
        state="disabled"
    )

    send_button.config(
        state="disabled"
    )

    disconnect_button.config(
        state="disabled"
    )

    status_label.config(
        text="● Disconnected",
        fg="#dc3545"
    )

    add_message(
        "System: You disconnected from the chat."
    )


# ============================================================
# CLEAR CHAT
# ============================================================

def clear_chat():

    chat_text.config(
        state="normal"
    )

    chat_text.delete(
        "1.0",
        tk.END
    )

    chat_text.config(
        state="disabled"
    )


# ============================================================
# CLOSE APPLICATION
# ============================================================

def close_application():

    global connected

    if connected:
        disconnect()

    root.destroy()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Python Chat Application"
)

root.geometry(
    "900x650"
)

root.minsize(
    800,
    600
)

root.configure(
    bg="#f4f6f8"
)


# ============================================================
# TITLE BAR
# ============================================================

title_frame = tk.Frame(
    root,
    bg="#1688e8",
    height=75
)

title_frame.pack(
    fill="x"
)

title_frame.pack_propagate(
    False
)


title_label = tk.Label(
    title_frame,
    text="Chat Application",
    font=("Arial", 23, "bold"),
    bg="#1688e8",
    fg="white"
)

title_label.pack(
    side="left",
    padx=30,
    pady=18
)


subtitle_label = tk.Label(
    title_frame,
    text="Real-time Client-Server Messaging",
    font=("Arial", 10),
    bg="#1688e8",
    fg="white"
)

subtitle_label.pack(
    side="left",
    padx=5
)


# ============================================================
# MAIN FRAME
# ============================================================

main_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=20
)


# ============================================================
# CONNECTION PANEL
# ============================================================

connection_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

connection_frame.pack(
    fill="x",
    pady=(0, 15)
)


connection_title = tk.Label(
    connection_frame,
    text="Connection",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#222222"
)

connection_title.pack(
    side="left",
    padx=20,
    pady=15
)


username_label = tk.Label(
    connection_frame,
    text="Username:",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#444444"
)

username_label.pack(
    side="left",
    padx=(10, 5)
)


username_entry = tk.Entry(
    connection_frame,
    font=("Arial", 10),
    width=18,
    bd=1,
    relief="solid"
)

username_entry.pack(
    side="left",
    ipady=5,
    padx=5
)


connect_button = tk.Button(
    connection_frame,
    text="Connect",
    font=("Arial", 10, "bold"),
    bg="#1688e8",
    fg="white",
    activebackground="#0d72c7",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=connect_to_server
)

connect_button.pack(
    side="left",
    padx=5,
    ipadx=10,
    ipady=5
)


disconnect_button = tk.Button(
    connection_frame,
    text="Disconnect",
    font=("Arial", 10, "bold"),
    bg="#dc3545",
    fg="white",
    activebackground="#b02a37",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    state="disabled",
    command=disconnect
)

disconnect_button.pack(
    side="left",
    padx=5,
    ipadx=10,
    ipady=5
)


status_label = tk.Label(
    connection_frame,
    text="● Disconnected",
    font=("Arial", 9, "bold"),
    bg="white",
    fg="#dc3545"
)

status_label.pack(
    side="right",
    padx=20
)


# ============================================================
# CHAT FRAME
# ============================================================

chat_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid"
)

chat_frame.pack(
    fill="both",
    expand=True
)


chat_title_frame = tk.Frame(
    chat_frame,
    bg="white"
)

chat_title_frame.pack(
    fill="x"
)


chat_title = tk.Label(
    chat_title_frame,
    text="Conversation",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#222222"
)

chat_title.pack(
    side="left",
    padx=20,
    pady=15
)


clear_button = tk.Button(
    chat_title_frame,
    text="Clear Chat",
    font=("Arial", 9, "bold"),
    bg="#eeeeee",
    fg="#333333",
    activebackground="#dddddd",
    bd=0,
    cursor="hand2",
    command=clear_chat
)

clear_button.pack(
    side="right",
    padx=20,
    pady=10
)


# ============================================================
# CHAT TEXT AREA
# ============================================================

chat_area = tk.Frame(
    chat_frame,
    bg="white"
)

chat_area.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)


chat_text = tk.Text(
    chat_area,
    font=("Consolas", 10),
    bg="#f8f9fa",
    fg="#333333",
    bd=1,
    relief="solid",
    wrap="word",
    state="disabled"
)

chat_text.pack(
    side="left",
    fill="both",
    expand=True
)


chat_scrollbar = tk.Scrollbar(
    chat_area,
    command=chat_text.yview
)

chat_scrollbar.pack(
    side="right",
    fill="y"
)


chat_text.config(
    yscrollcommand=chat_scrollbar.set
)


# ============================================================
# MESSAGE INPUT
# ============================================================

message_frame = tk.Frame(
    chat_frame,
    bg="white"
)

message_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)


message_entry = tk.Entry(
    message_frame,
    font=("Arial", 11),
    bd=1,
    relief="solid",
    state="disabled"
)

message_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8
)


send_button = tk.Button(
    message_frame,
    text="Send",
    font=("Arial", 10, "bold"),
    bg="#1688e8",
    fg="white",
    activebackground="#0d72c7",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    state="disabled",
    command=send_message
)

send_button.pack(
    side="left",
    padx=(10, 0),
    ipadx=20,
    ipady=7
)


# ============================================================
# ENTER KEY TO SEND
# ============================================================

message_entry.bind(
    "<Return>",
    send_message
)


# ============================================================
# INITIAL MESSAGE
# ============================================================

add_message(
    "System: Start server.py first, then connect using your username."
)


# ============================================================
# CLOSE EVENT
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ============================================================
# START GUI
# ============================================================

root.mainloop()