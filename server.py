import http.server
import socketserver

# Définir le port sur lequel écouter (443)
PORT = 443

# Définir le gestionnaire de requêtes HTTP
Handler = http.server.SimpleHTTPRequestHandler

# Créer un serveur HTTP
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server is listening on port", PORT)
    # Démarrer le serveur et le maintenir en écoute
    httpd.serve_forever()
