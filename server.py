import socket
import threading

# Adresse IP et ports du serveur
IP_SERVER = "0.0.0.0"  # Laissez cette chaîne vide pour lier le serveur à toutes les interfaces disponibles
PORT_HTTPS = 443
PORT_OTHER = 6969

# Création du socket serveur pour HTTPS
server_https = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_https.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_https.bind((IP_SERVER, PORT_HTTPS))

# Création du socket serveur pour l'autre port
server_other = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_other.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_other.bind((IP_SERVER, PORT_OTHER))

# Nombre maximal de connexions en attente autorisées (backlog)
server_https.listen(5)
server_other.listen(5)

# Affichage de l'adresse IP et des ports du serveur
if IP_SERVER:
    print(f"[*] Server running, listening on {IP_SERVER}")
else:
    IP_SERVER = socket.gethostbyname(socket.gethostname())
    print(f"[*] Server running, listening on {IP_SERVER}")

print(f"[*] Server listening on HTTPS port {PORT_HTTPS}")
print(f"[*] Server listening on other port {PORT_OTHER}")


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
def handle_client_connection(server_socket: socket.socket):
    while True:
        try:
            # Accepter une nouvelle connexion du client
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from: {client_address[0]}:{client_address[1]}")
            # Ajouter le client à la liste des clients connectés
            clients.append(client_socket)
            # Démarrer un thread pour gérer les messages du client
            threading.Thread(target=handle_received_message, args=(client_socket,)).start()
        except Exception as e:
            print(f'[!] Error accepting client connection: {e}')
            break


# Fonction pour démarrer le serveur
def start_server(server_socket: socket.socket):
    try:
        while True:
            # Gérer les connexions des clients
            handle_client_connection(server_socket)
    except KeyboardInterrupt:
        print("[*] Server stopped.")
    finally:
        # Fermer tous les sockets clients restants
        for client in clients:
            client.close()
        # Fermer le socket serveur
        server_socket.close()


# Démarrer le serveur dans un thread séparé pour chaque port
threading.Thread(target=start_server, args=(server_https,)).start()
threading.Thread(target=start_server, args=(server_other,)).start()
