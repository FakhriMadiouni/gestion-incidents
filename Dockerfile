# Image de base
FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Copier requirements.txt d'abord (profite du cache des couches Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Dossier de la base SQLite (sera monté en volume)
RUN mkdir -p /app/data

# Port de l'application
EXPOSE 5000

# Commande de démarrage
CMD ["python", "run.py"]
