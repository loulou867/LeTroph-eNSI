# Importer les modules nécessaires
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
import socket
import threading

# Définir une classe pour l'application de chat client
class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Client")  # Définir le titre de la fenêtre
        self.setGeometry(100, 100, 400, 500)  # Définir la taille de la fenêtre

        layout = QVBoxLayout()  # Créer un layout vertical pour organiser les widgets

        # Créer une zone de texte pour afficher les messages
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)  # Rendre la zone de texte en lecture seule
        layout.addWidget(self.message_log)

        # Créer un champ de saisie pour écrire les messages
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        # Créer un bouton pour envoyer les messages
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)  # Connecter le clic sur le bouton à une fonction
        layout.addWidget(self.send_button)

        self.setLayout(layout)  # Définir le layout pour la fenêtre

        # Demander le surnom (nickname) de l'utilisateur
        self.nickname = input("Name: ")

        # Se connecter au serveur
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 12345))  # Se connecter à l'adresse IP et au port spécifiés

        # Démarrer un thread pour recevoir les messages du serveur
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    # Fonction pour envoyer un message au serveur
    def send_message(self):
        message = self.input_field.text()
        if message:
            self.client.send('{}: {}'.format(self.nickname, message).encode('ascii'))  # Envoyer le message au serveur
            self.input_field.clear()  # Effacer le champ de saisie après l'envoi

    # Fonction pour recevoir les messages du serveur
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')  # Recevoir un message du serveur
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))  # Envoyer le surnom au serveur si nécessaire
                else:
                    self.message_log.append(message)  # Ajouter le message reçu à la zone de texte
            except:
                print("An error occurred!")
                self.client.close()  # Fermer la connexion avec le serveur en cas d'erreur
                break

# Point d'entrée de l'application
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Créer une application Qt
    client_window = ChatClient()  # Créer une instance de la classe ChatClient
    client_window.show()  # Afficher la fenêtre
    sys.exit(app.exec_())  # Lancer l'application et attendre la sortie
