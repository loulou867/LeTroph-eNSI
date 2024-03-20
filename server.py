from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Liste pour stocker les connexions des clients HTTP
http_clients = []
lock = threading.Lock()  # Verrou pour assurer la cohérence de la liste http_clients

# Classe pour gérer les requêtes HTTP
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = post_data.decode('utf-8')
        print("Received message:", message)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with lock:
            for client in http_clients:
                client.wfile.write(message.encode('utf-8'))

# Fonction pour démarrer le serveur HTTP
def start_http_server():
    server_address = ('', 443)  # Écoute sur toutes les interfaces réseau disponibles
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print("HTTP Server is listening on port 443")
    httpd.serve_forever()

# Démarrer le serveur HTTP dans un thread séparé
http_server_thread = threading.Thread(target=start_http_server)
http_server_thread.start()
