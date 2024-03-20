import socket
import threading

# Host and port
HOST = '0.0.0.0'
PORT = 6969

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server.bind((HOST, PORT))

# Listen for incoming connections
server.listen()

# List to keep track of clients and their nicknames
clients = {}
addresses = {}

# Function to broadcast messages to all clients
def broadcast(message):
    for client_socket in clients:
        client_socket.send(message)

# Function to handle client connections
def handle_client(client_socket, address):
    print(f"New connection from {address}.")

    # Send a welcome message to the client
    client_socket.send("Welcome to the chatroom!".encode("utf-8"))

    # Prompt the client for a nickname
    client_socket.send("Please enter your nickname: ".encode("utf-8"))
    nickname = client_socket.recv(1024).decode("utf-8")

    # Add the client and their nickname to the list
    clients[client_socket] = nickname
    addresses[client_socket] = address

    # Broadcast the new connection to all clients
    broadcast(f"{nickname} has joined the chat!".encode("utf-8"))

    while True:
        # Wait for messages from the client
        message = client_socket.recv(1024)

        # If the client disconnects, remove them from the list and broadcast the event
        if not message:
            client_socket.close()
            del clients[client_socket]
            broadcast(f"{nickname} has left the chat.".encode("utf-8"))
            break

        # Broadcast the message to all other clients
        broadcast(f"{nickname}: {message}".encode("utf-8"))

# Main function to accept incoming connections
def accept_connections():
    print("Server is listening...")
    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# Start accepting connections
accept_connections()
