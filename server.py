import socket
import sys
import threading
from utility import encodeMessage, decodeMessage

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Mettre l'adresse IP publique du serveur cloud
IP_ADDR = 'XXX.XXX.XXX.XXX'  # Remplacer XXX.XXX.XXX.XXX par l'adresse IP publique du serveur
PORT = 4444
server.bind((IP_ADDR, PORT))
server.listen(100)
clients = {}  # Mapping des connexions client avec leur nom de client

def main():
    print('En attente de clients pour se connecter...')
    while True:
        conn, addr = server.accept()
        clients[conn] = ''
        print('{} client connecté: {}'.format(len(clients), addr[0]))
        print('{} connecté'.format(addr))
        t = threading.Thread(target=newClient, args=(conn, addr,))
        t.start()
    server.close()

def newClient(conn, addr):
    clientName = str(addr[0]) + '.' + str(addr[1])
    conn.send(encodeMessage('Bienvenue dans le salon de discussion, entrez votre nom : '))
    clientName = decodeMessage(conn.recv(4096))
    clients[conn] = clientName
    broadcast(encodeMessage('{} connecté'.format(clientName)), conn)
    while True:
        try:
            msg = conn.recv(4096)
            if msg:
                msg = clientName + ': ' + decodeMessage(msg)
                print(msg)
                broadcast(encodeMessage(msg), conn)
            else:
                removeClient(conn)
                break
        except:
            continue

def broadcast(msg, conn=None):
    for client in clients:
        if(client == conn):
            continue
        try:
            client.send(msg)
        except:
            removeClient(client)

def removeClient(curClient):
    if curClient in clients:
        broadcast(encodeMessage('{} déconnecté'.format(clients[curClient])), curClient)
        clients.pop(curClient)

if __name__ == '__main__':
    main()
