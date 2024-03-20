import socket
import threading

# Données de connexion
hôte = '127.0.0.1'  # C'est l'adresse IP de notre ordinateur.
port = 12345        # C'est le port que nous utilisons pour la connexion.

# Commençons par lancer le serveur.
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création d'un tunnel TCP en IPV4
serveur.bind((hôte, port))                                  # Relion-le à notre adresse IP et notre port.
serveur.listen()                                            # Mettons-le en mode écoute.

# Créons des listes pour stocker les clients et leurs pseudonymes.
clients = [] 
pseudonymes = []

# Diffusion des messages du client à tous les autres clients connectés.
def diffusion(message): 
    for client in clients:
        client.send(message)  # Envoyons le message à chaque client.

# Gérons les messages reçus des clients.
def gestion(client):
    while True:
        try:
            # Listening des messages.
            message = client.recv(1024)  # .recv(1024 bytes) = recoit le message                    
            diffusion(message)  # Après avoir reçu un message, renvoyer-le à tout le monde.
        except:
            # Si client se déconnecte, retire le de la liste.
            index = clients.index(client)        
            clients.remove(client)       
            client.close() # fermeture du client
            pseudonyme = pseudonymes[index]  # Retirons également son pseudonyme.
            diffusion('{} a quitté!'.format(pseudonyme).encode('ascii'))  
            pseudonymes.remove(pseudonyme)
            break        

# Fonction pour recevoir les connexions des clients.
def recevoir():
    while True:
        # Accepter les connexions entrantes.
        client, adresse = serveur.accept()  
        print("Connecté avec {}".format(str(adresse)))  

        # demande au client son pseudonyme.
        client.send('NICK'.encode('ascii'))  
        pseudonyme = client.recv(1024).decode('ascii')  
        pseudonymes.append(pseudonyme)
        clients.append(client)

        # Affichons le nickname du nouveau client.
        print("Le pseudonyme est {}".format(pseudonyme))
        diffusion("{} a rejoint!".format(pseudonyme).encode('ascii'))  
        client.send('Connecté au serveur!'.encode('ascii'))  

        # Demarre un thread pour gérer les messages du client.
        thread = threading.Thread(target=gestion, args=(client,))  
        thread.start()  

print("Le serveur est prêt à recevoir des messages !")
recevoir()  # Allons-y !
