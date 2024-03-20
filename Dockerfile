# Utiliser l'image Python officielle comme image de base
FROM python:3.11

# Mettre à jour pip
RUN pip install --upgrade pip

# Créer un répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier server.py depuis le répertoire local vers le conteneur
COPY server.py /app/

# Exposer le port 8080
EXPOSE 6969

# Définir le point d'entrée pour le conteneur
CMD ["python", "server.py", "8080"]
