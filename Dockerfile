# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer dépendances système si besoin (pas nécessaire ici)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Lancer le bot
CMD ["python", "main.py"]