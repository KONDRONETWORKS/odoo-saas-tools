# Dockerfile pour Odoo SaaS Tools 18.0
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV ODOO_VERSION=18.0

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN useradd -ms /bin/bash odoo

# Définir le répertoire de travail
WORKDIR /opt/odoo

# Copier les fichiers de dépendances
COPY requirements.txt requirements-dev.txt ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Changer les permissions
RUN chown -R odoo:odoo /opt/odoo

# Passer à l'utilisateur odoo
USER odoo

# Exposer le port
EXPOSE 8069

# Script de démarrage
CMD ["python3", "saas.py", "--run"]
