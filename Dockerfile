# 1. Utiliser l'image Python officielle
FROM python:3.12-slim

# 2. Définir le répertoire de travail
WORKDIR /app

# 3. Copier les fichiers du projet
COPY . .

# 4. Installer les dépendances
RUN pip install --no-cache-dir flask

# 5. Exposer le port 5000
EXPOSE 5000

# 6. Lancer le service
CMD ["python", "app.py"]
