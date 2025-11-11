#!/bin/bash
# User data script pour instances EC2 Odoo SaaS Tools
# Ce script s'exécute au démarrage de l'instance

set -e

# Variables
PROJECT_DIR="/opt/odoo-saas-tools"
ODOO_USER="odoo"
LOG_FILE="/var/log/user-data.log"

# Rediriger toutes les sorties vers le log
exec > >(tee -a $LOG_FILE)
exec 2>&1

echo "🚀 Démarrage configuration Odoo SaaS Tools - $(date)"

# Mise à jour système
echo "📦 Mise à jour du système..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get upgrade -y

# Installation dépendances système
echo "🔧 Installation des dépendances..."
apt-get install -y \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    python3.11-dev \
    postgresql-client-15 \
    libpq-dev \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    build-essential \
    curl \
    wget \
    htop \
    ufw \
    awscli \
    unzip \
    software-properties-common

# Configuration firewall
echo "🔥 Configuration firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Création utilisateur odoo
echo "👤 Création utilisateur..."
useradd -m -s /bin/bash $ODOO_USER || true
mkdir -p $PROJECT_DIR
chown $ODOO_USER:$ODOO_USER $PROJECT_DIR

# Installation boto3 pour intégration AWS
echo "📦 Installation boto3..."
pip3 install boto3 boto

# Clonage projet
echo "📁 Configuration projet..."
cd /tmp
sudo -u $ODOO_USER git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git $PROJECT_DIR || {
    echo "⚠️ Impossible de cloner depuis GitHub, utilisation du code local ou S3"
}

# Création environnement virtuel
echo "🐍 Configuration Python..."
sudo -u $ODOO_USER python3.11 -m venv $PROJECT_DIR/venv
sudo -u $ODOO_USER $PROJECT_DIR/venv/bin/pip install --upgrade pip
sudo -u $ODOO_USER $PROJECT_DIR/venv/bin/pip install -r $PROJECT_DIR/requirements.txt || {
    echo "⚠️ Fichier requirements.txt non trouvé, installation des dépendances de base..."
    sudo -u $ODOO_USER $PROJECT_DIR/venv/bin/pip install \
        psycopg2-binary \
        boto3 \
        oauthlib \
        requests \
}

# Configuration Odoo
echo "⚙️ Configuration Odoo..."
sudo -u $ODOO_USER mkdir -p $PROJECT_DIR/filestore
sudo -u $ODOO_USER mkdir -p /var/log/odoo

sudo -u $ODOO_USER tee $PROJECT_DIR/odoo.conf > /dev/null <<EOF
[options]
# Base de données
admin_passwd = $(openssl rand -hex 32)
db_host = ${db_host}
db_port = 5432
db_user = ${db_user}
db_password = ${db_password}
db_name = ${db_name}

# Chemins
addons_path = $PROJECT_DIR,/opt/odoo/addons
data_dir = $PROJECT_DIR/filestore

# Réseau
xmlrpc_port = 8069
longpolling_port = 8072
workers = 4
max_cron_threads = 2

# Performance
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200

# Logs
log_level = info
log_handler = :INFO
logfile = /var/log/odoo/odoo.log

# Sécurité
proxy_mode = True
without_demo = True

# SaaS spécifique
saas_portal_domain = portal.${domain_name}
saas_server_domain = server.${domain_name}
EOF

# Configuration Nginx
echo "🌐 Configuration Nginx..."
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

tee /etc/nginx/sites-available/odoo > /dev/null <<EOF
upstream odoo {
    server 127.0.0.1:8069;
    keepalive 64;
}

# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name ${domain_name} www.${domain_name} *.${domain_name};
    return 301 https://\$host\$request_uri;
}

# Configuration HTTPS
server {
    listen 443 ssl http2;
    server_name ${domain_name} www.${domain_name} *.${domain_name};

    # SSL (sera configuré par ACM via ALB)
    # ssl_certificate /etc/letsencrypt/live/${domain_name}/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/${domain_name}/privkey.pem;
    
    client_max_body_size 200M;
    proxy_read_timeout 660s;
    proxy_connect_timeout 660s;
    proxy_send_timeout 660s;

    # Logs
    access_log /var/log/nginx/odoo-access.log;
    error_log /var/log/nginx/odoo-error.log;

    # Proxy vers Odoo
    location / {
        proxy_pass http://odoo;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        proxy_redirect off;
    }

    # WebSocket support
    location /websocket {
        proxy_pass http://odoo;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_read_timeout 3600s;
    }

    # Long polling
    location /longpolling {
        proxy_pass http://odoo;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Health check
    location /web/health {
        proxy_pass http://odoo;
        access_log off;
    }
}
EOF

ln -sf /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test et rechargement Nginx
nginx -t && systemctl reload nginx

# Service systemd
echo "🔧 Configuration service..."
tee /etc/systemd/system/odoo-saas.service > /dev/null <<EOF
[Unit]
Description=Odoo SaaS Tools
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=$ODOO_USER
Group=$ODOO_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=$PROJECT_DIR/venv/bin/python3.11 ../odoo/odoo-bin -c $PROJECT_DIR/odoo.conf
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=odoo-saas

# Limites de sécurité
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable odoo-saas
systemctl start odoo-saas

# Configuration CloudWatch Agent (optionnel)
echo "📊 Configuration CloudWatch..."
mkdir -p /opt/aws/amazon-cloudwatch-agent/etc
tee /opt/aws/amazon-cloudwatch-agent/etc/config.json > /dev/null <<EOF
{
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/var/log/odoo/odoo.log",
                        "log_group_name": "/aws/ec2/${project_name}",
                        "log_stream_name": "{instance_id}/odoo.log"
                    },
                    {
                        "file_path": "/var/log/nginx/odoo-access.log",
                        "log_group_name": "/aws/ec2/${project_name}",
                        "log_stream_name": "{instance_id}/nginx-access.log"
                    },
                    {
                        "file_path": "/var/log/nginx/odoo-error.log",
                        "log_group_name": "/aws/ec2/${project_name}",
                        "log_stream_name": "{instance_id}/nginx-error.log"
                    }
                ]
            }
        }
    }
}
EOF

# Télécharger et installer CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb -O /tmp/amazon-cloudwatch-agent.deb
dpkg -i /tmp/amazon-cloudwatch-agent.deb || true
systemctl enable amazon-cloudwatch-agent
systemctl start amazon-cloudwatch-agent || true

# Vérification finale
echo "✅ Vérification installation..."
sleep 10
systemctl status odoo-saas --no-pager || true

echo "✅ Configuration terminée - $(date)"
echo "🌐 Instance prête pour le déploiement"
echo "📝 Logs disponibles dans: $LOG_FILE"

