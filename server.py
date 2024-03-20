import socketserver
import threading
import urllib.parse
import socket

# Définir le port sur lequel écouter (443 pour HTTP, 6969 pour le client Python)
HTTP_PORT = 443
def do_POST(self):
        message = post_data['message'][0]
        # Ajouter le message à la liste des messages
        messages.append(message)
        # Envoyer le message à tous les autres clients Python
        for client_socket in python_clients:
            client_socket.sendall(message.encode("utf-8"))
        # Rediriger vers la page principale du chat room
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

# Fonction pour démarrer le serveur HTTP
def start_http_server():
    with socketserver.TCPServer(("", HTTP_PORT), ChatRoomHandler) as httpd:
        print("HTTP Server is listening on port", HTTP_PORT)
        httpd.serve_forever()
# Liste pour stocker les connexions des clients Python
python_clients = []

# Fonction pour gérer les connexions des clients Python
def handle_python_client(client_socket):
    python_clients.append(client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print("Received message from Python client:", message)
            # Ajouter le message à la liste des messages
            messages.append(message)
            # Envoyer le message à tous les autres clients Python
            for socket in python_clients:
                if socket != client_socket:
                    socket.sendall(message.encode("utf-8"))
        except Exception as e:
            print("Error handling Python client:", e)
            break
    python_clients.remove(client_socket)
    client_socket.close()

# Fonction pour démarrer le serveur HTTP
def start_http_server():
    with socketserver.TCPServer(("", HTTP_PORT), ChatRoomHandler) as httpd:
        print("HTTP Server is listening on port", HTTP_PORT)
        httpd.serve_forever()

# Fonction pour démarrer le serveur Python
def start_python_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("", PYTHON_PORT))
        server_socket.listen()
        print("Python Server is listening on port", PYTHON_PORT)
        while True:
            client_socket, _ = server_socket.accept()
            client_thread = threading.Thread(target=handle_python_client, args=(client_socket,))
            client_thread.start()
# Démarrer les serveurs dans des threads séparés
http_server_thread = threading.Thread(target=start_http_server)
http_server_thread.start()
python_server_thread = threading.Thread(target=start_python_server)
python_server_thread.start()
