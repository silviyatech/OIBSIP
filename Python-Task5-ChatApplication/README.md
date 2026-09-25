# Chat Application

A Python-based real-time Chat Application developed as part of the Oasis Infobyte Python Programming Internship.

## Task

**Task 5 - Chat Application**

## Description

This project is a real-time client-server chat application developed using Python.

The application allows multiple users to connect to a central server and exchange messages in real time. The server manages connected clients, while each client provides a graphical chat interface.

## Features

- Real-time messaging
- Client-server architecture
- Multiple client support
- Username-based connection
- Message timestamps
- Send and receive messages
- Graphical user interface using Tkinter
- Connect and disconnect functionality
- Clear chat option
- Enter key support for sending messages
- Graceful client disconnection
- Multi-threaded server
- Error handling

## Technologies Used

- Python
- Socket Programming
- Tkinter
- Threading

## How It Works

The application consists of two main components:

### Server

The server listens for incoming client connections and manages communication between connected users.

### Client

Each client connects to the server using a username and provides a graphical interface for sending and receiving messages.

Messages sent by one client are broadcast to the other connected clients.

## How to Run

### 1. Start the Server

Open the VS Code terminal and run:

```bash
python server.py