import socket
import threading

# Adresse IP et port du serveur
IP_SERVER = ""  # Laissez cette chaîne vide pour lier le serveur à toutes les interfaces disponibles
PORT = 443

# Création du socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du socket à l'adresse IP et au port spécifiés
server.bind((IP_SERVER, PORT))

# Nombre maximal de connexions en attente autorisées (backlog)
server.listen(5)

# Affichage de l'adresse IP et du port du serveur
if IP_SERVER:
    print(f"[*] Server running, listening on {IP_SERVER}:{PORT}")
else:
    IP_SERVER = socket.gethostbyname(socket.gethostname())
    print(f"[*] Server running, listening on {IP_SERVER}:{PORT}")


# Fonction pour gérer les messages entrants du client
def handle_received_message(client_socket: socket.socket):
    while True:
        try:
            # Recevoir le message du client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[Client]: {message}")
                # Diffuser le message à tous les autres clients
                broadcast_message(message, client_socket)
            else:
                # Fermer la connexion si le message est vide
                client_socket.close()
                break
        except Exception as e:
            print(f'[!] Error handling message from client: {e}')
            client_socket.close()
            break


# Fonction pour diffuser un message à tous les clients sauf l'expéditeur
def broadcast_message(message: str, sender_socket: socket.socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f'[!] Error broadcasting message to client: {e}')
                client.close()
                clients.remove(client)


# Liste pour stocker les connexions des clients
clients = []

# Fonction pour gérer les connexions des clients
def handle_client_connection():
    while True:
        try:
            # Accepter une nouvelle connexion du client
            client_socket, client_address = server.accept()
            print(f"[*] Accepted connection from: {client_address[0]}:{client_address[1]}")
            # Ajouter le client à la liste des clients connectés
            clients.append(client_socket)
            # Démarrer un thread pour gérer les messages du client
            threading.Thread(target=handle_received_message, args=(client_socket,)).start()
        except Exception as e:
            print(f'[!] Error accepting client connection: {e}')
            break


# Fonction pour démarrer le serveur
def start_server():
    try:
        while True:
            # Gérer les connexions des clients
            handle_client_connection()
    except KeyboardInterrupt:
        print("[*] Server stopped.")
    finally:
        # Fermer tous les sockets clients restants
        for client in clients:
            client.close()
        # Fermer le socket serveur
        server.close()


# Démarrer le serveur dans un thread séparé
server_thread = threading.Thread(target=start_server)
server_thread.start()
