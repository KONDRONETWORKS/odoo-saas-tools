FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /opt/odoo

# Copier les fichiers de requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 odoo && chown -R odoo:odoo /opt/odoo
USER odoo

# Exposer le port
EXPOSE 8069

# Commande par défaut
CMD ["python3", "saas.py", "--portal-create", "--server-create", "--plan-create", "--run"]