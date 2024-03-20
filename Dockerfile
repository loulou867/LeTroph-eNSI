# Utiliser l'image Python officielle comme image de base
FROM python:3.11

# Mettre à jour p


# Créer un répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier server.py depuisle répertoire local vers le conteneur
COPY server.py /app/

# Exposer le port 8080
EXPOSE 443

# Définir le point d'entrée pour le conteneur
CMD ["python", "server.py", "8080"]
