#!/bin/bash
# Script de déploiement pour Odoo SaaS Tools

set -e

echo "🚀 Déploiement Odoo SaaS Tools"

# Variables
PROJECT_DIR="/opt/odoo-saas-tools"
ODOO_USER="odoo"
POSTGRES_USER="odoo"
POSTGRES_PASSWORD="odoo_password_secure"

# Mise à jour du système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
echo "🔧 Installation des dépendances..."
sudo apt install -y python3.11 python3.11-pip python3.11-venv postgresql postgresql-contrib nginx git

# Création de l'utilisateur odoo
echo "👤 Création de l'utilisateur odoo..."
sudo useradd -m -s /bin/bash $ODOO_USER || true

# Configuration PostgreSQL
echo "🗄️ Configuration PostgreSQL..."
sudo -u postgres psql -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE odoo OWNER $POSTGRES_USER;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE odoo TO $POSTGRES_USER;"

# Clonage du projet
echo "📁 Clonage du projet..."
sudo git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git $PROJECT_DIR
sudo chown -R $ODOO_USER:$ODOO_USER $PROJECT_DIR

# Configuration Python
echo "🐍 Configuration Python..."
sudo -u $ODOO_USER python3.11 -m venv $PROJECT_DIR/venv
sudo -u $ODOO_USER $PROJECT_DIR/venv/bin/pip install -r $PROJECT_DIR/requirements.txt

# Configuration Odoo
echo "⚙️ Configuration Odoo..."
sudo -u $ODOO_USER cat > $PROJECT_DIR/odoo.conf << EOF
[options]
admin_passwd = $POSTGRES_PASSWORD
db_host = localhost
db_port = 5432
db_user = $POSTGRES_USER
db_password = $POSTGRES_PASSWORD
addons_path = $PROJECT_DIR
data_dir = $PROJECT_DIR/filestore
xmlrpc_port = 8069
workers = 4
max_cron_threads = 2
EOF

# Configuration Nginx
echo "🌐 Configuration Nginx..."
sudo cat > /etc/nginx/sites-available/odoo << EOF
upstream odoo {
    server 127.0.0.1:8069;
}

server {
    listen 80;
    server_name votre-domaine.com;
    
    client_max_body_size 200M;
    
    location / {
        proxy_pass http://odoo;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Service systemd
echo "🔧 Configuration du service systemd..."
sudo cat > /etc/systemd/system/odoo-saas.service << EOF
[Unit]
Description=Odoo SaaS Tools
After=postgresql.service

[Service]
Type=simple
User=$ODOO_USER
Group=$ODOO_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python3 saas.py --portal-create --server-create --plan-create --run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable odoo-saas
sudo systemctl start odoo-saas

echo "✅ Déploiement terminé!"
echo "🌐 Accès: http://votre-domaine.com"
echo "📊 Status: sudo systemctl status odoo-saas"
echo "📝 Logs: sudo journalctl -u odoo-saas -f"
