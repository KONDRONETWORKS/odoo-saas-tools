# 🐳 Dockerfile Odoo SaaS - Production optimisée
# Base: Odoo 18 officiel
# OS: Debian 12 (Bookworm)

FROM odoo:18

USER root

# Variables d'environnement
ENV ODOO_VERSION=18.0 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Outils de base
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    # Bibliothèques Python
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    # Dépendances de compilation
    build-essential \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    # Outils pour PostgreSQL
    postgresql-client \
    # Bibliothèques graphiques (pour les rapports PDF)
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    zlib1g-dev \
    # Fonts pour les PDF
    fonts-liberation \
    # wkhtmltopdf pour les rapports PDF
    wkhtmltopdf \
    # Nettoyage
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Mise à jour pip
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Copier et installer les dépendances Python
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Installer les dépendances supplémentaires pour SaaS
RUN pip3 install --no-cache-dir \
    boto3>=1.34.0 \
    rotate-backups-s3>=0.3.0 \
    pysftp>=0.2.9 \
    oauthlib>=3.2.0 \
    ovh>=1.1.0 \
    psycopg2-binary>=2.9.0 \
    requests>=2.31.0 \
    cachetools>=5.0.0 \
    paramiko>=2.12.0 \
    cryptography>=41.0.0 \
    python-dotenv>=1.0.0

# Créer les répertoires nécessaires
RUN mkdir -p \
    /var/lib/odoo/filestore \
    /var/lib/odoo/backups \
    /var/log/odoo \
    /mnt/extra-addons \
    /opt/odoo/custom \
    && chown -R odoo:odoo /var/lib/odoo \
    && chown -R odoo:odoo /var/log/odoo \
    && chown -R odoo:odoo /mnt/extra-addons \
    && chown -R odoo:odoo /opt/odoo

# Configuration de wkhtmltopdf (pour les rapports PDF)
RUN ln -s /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf \
    && ln -s /usr/bin/wkhtmltoimage /usr/local/bin/wkhtmltoimage

# Copier le script d'entrée personnalisé
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copier les modules custom (si nécessaire)
# COPY ./custom-addons /mnt/extra-addons

# Retour à l'utilisateur odoo
USER odoo

# Volumes
VOLUME ["/var/lib/odoo", "/mnt/extra-addons"]

# Ports
EXPOSE 8069 8072

# Point d'entrée
ENTRYPOINT ["/docker-entrypoint.sh"]

# Commande par défaut
CMD ["odoo"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8069/web/health || exit 1

# Labels
LABEL maintainer="KONDRO Networks <apps@itexperts4africa.com>" \
      version="18.0.2024" \
      description="Odoo 18 SaaS Platform - Production Ready" \
      org.opencontainers.image.title="Odoo SaaS" \
      org.opencontainers.image.version="18.0" \
      org.opencontainers.image.vendor="KONDRO Networks"
