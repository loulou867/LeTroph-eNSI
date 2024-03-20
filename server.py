import http.server
import socketserver
import threading
import urllib.parse

# Définir le port sur lequel écouter (443)
PORT = 443

# Liste pour stocker les messages
messages = []

# Gestionnaire de requêtes HTTP pour notre chat room
class ChatRoomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Vérifier si la demande est pour la page principale du chat room
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Afficher le formulaire de chat
            self.wfile.write(b'''
                <html>
                <head><title>Chat Room</title></head>
                <body>
                <h1>Welcome to the Chat Room</h1>
                <form method="post">
                <input type="text" name="message" autocomplete="off">
                <input type="submit" value="Send">
                </form>
                <div id="messages">
            ''')
            # Afficher les messages précédents
            for message in messages:
                self.wfile.write(f'<p>{message}</p>'.encode('utf-8'))
            self.wfile.write(b'</div></body></html>')
        else:
            super().do_GET()

    def do_POST(self):
        # Récupérer les données du formulaire
        content_length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(content_length).decode('utf-8'))
        message = post_data['message'][0]
        # Ajouter le message à la liste des messages
        messages.append(message)
        # Rediriger vers la page principale du chat room
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

# Fonction pour démarrer le serveur HTTP
def start_server():
    with socketserver.TCPServer(("", PORT), ChatRoomHandler) as httpd:
        print("Server is listening on port", PORT)
        httpd.serve_forever()

# Démarrer le serveur dans un thread séparé
server_thread = threading.Thread(target=start_server)
server_thread.start()
