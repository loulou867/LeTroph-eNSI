import socket
import threading

# Données de connexion
hôte = '127.0.0.1'  # IP de votre hôte
port = 12345  # Ne pas utiliser de ports réservés

# Démarrage du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket Internet
serveur.bind((hôte, port))  # Le serveur est lié à l'hôte local et à un port
serveur.listen()  # Le serveur est en mode écoute

# Listes des clients et de leurs surnoms
clients = []
surnoms = []

# Envoi de messages à tous les clients connectés
def diffuser(message):
    for client in clients:
        client.send(message)

# Gestion des messages des clients
def gérer(client):
    while True:
        try:
            # Diffusion des messages
            message = client.recv(1024)
            diffuser(message)
        except:
            # Suppression et fermeture des clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            surnom = surnoms[index]
            diffuser('{} est parti!'.format(surnom).encode('ascii'))
            surnoms.remove(surnom)
            break

# Fonction de réception/écoute
def recevoir():
    while True:
        # Accepter la connexion
        client, adresse = serveur.accept()
        print("Connecté avec {}".format(str(adresse)))

        # Demander et stocker le surnom
        client.send('NICK'.encode('ascii'))
        surnom = client.recv(1024).decode('ascii')
        surnoms.append(surnom)
        clients.append(client)

        # Afficher et diffuser le surnom
        print("Le nom est {}".format(surnom))
        diffuser("{} a rejoint!".format(surnom).encode('ascii'))
        client.send('Connecté au serveur!'.encode('ascii'))

        # Démarrer le thread de gestion pour le client
        thread = threading.Thread(target=gérer, args=(client,))
        thread.start()

print("Le serveur est démarré................,:)")
recevoir()
