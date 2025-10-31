# 🚀 Guide de Déploiement Odoo SaaS Tools sur AWS

Ce guide complet vous explique comment déployer votre plateforme SaaS Odoo sur Amazon Web Services (AWS).

## 📋 Table des Matières

1. [Architecture AWS Recommandée](#architecture-aws-recommandée)
2. [Prérequis](#prérequis)
3. [Option 1: Déploiement avec EC2 (Recommandé)](#option-1-déploiement-avec-ec2)
4. [Option 2: Déploiement avec ECS/Fargate](#option-2-déploiement-avec-ecsfargate)
5. [Option 3: Déploiement avec Elastic Beanstalk](#option-3-déploiement-avec-elastic-beanstalk)
6. [Configuration AWS (Route53, S3, etc.)](#configuration-aws)
7. [Sécurité et Monitoring](#sécurité-et-monitoring)
8. [Backup et Restauration](#backup-et-restauration)
9. [Optimisation et Scaling](#optimisation-et-scaling)
10. [Dépannage](#dépannage)

---

## 🏗️ Architecture AWS Recommandée

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Cloud                            │
│                                                          │
│  ┌─────────────┐    ┌──────────────┐                   │
│  │ Route53     │───▶│  CloudFront  │ (Optionnel)       │
│  │ (DNS)       │    │  (CDN)       │                   │
│  └─────────────┘    └──────┬───────┘                   │
│                            │                            │
│  ┌─────────────────────────▼──────────────┐            │
│  │      Application Load Balancer         │            │
│  │            (HTTPS/HTTP)                │            │
│  └───────────────┬────────────────────────┘            │
│                  │                                       │
│  ┌───────────────▼───────────────┐                      │
│  │     EC2 Auto Scaling Group    │                      │
│  │  ┌─────────┐  ┌─────────┐    │                      │
│  │  │ EC2 #1  │  │ EC2 #2  │    │ (Multi-AZ)          │
│  │  │ Odoo    │  │ Odoo    │    │                      │
│  │  └────┬────┘  └────┬────┘    │                      │
│  └───────┼─────────────┼──────────┘                     │
│          │             │                                 │
│  ┌───────▼─────────────▼──────────┐                     │
│  │    RDS PostgreSQL (Multi-AZ)    │                     │
│  │    - Primary: AZ-1              │                     │
│  │    - Standby: AZ-2              │                     │
│  └─────────────────────────────────┘                     │
│                                                           │
│  ┌──────────────────────────────────┐                    │
│  │   S3 Buckets                     │                    │
│  │   - backups/                     │                    │
│  │   - filestore/                   │                    │
│  └──────────────────────────────────┘                    │
│                                                           │
│  ┌──────────────────────────────────┐                    │
│  │   CloudWatch                     │                    │
│  │   - Monitoring & Logs            │                    │
│  └──────────────────────────────────┘                    │
└───────────────────────────────────────────────────────────┘
```

---

## 📦 Prérequis

### Compte AWS
- Compte AWS actif
- AWS CLI installé et configuré (`aws configure`)
- Permissions IAM appropriées (EC2, RDS, S3, Route53, CloudWatch)

### Outils Locaux
```bash
# Installation AWS CLI (macOS)
brew install awscli

# Installation AWS CLI (Linux)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Vérification
aws --version
```

### Configuration AWS CLI
```bash
aws configure
# AWS Access Key ID: [Votre clé]
# AWS Secret Access Key: [Votre secret]
# Default region name: eu-west-1 (ou votre région)
# Default output format: json
```

---

## 🖥️ Option 1: Déploiement avec EC2 (Recommandé)

### Étape 1: Créer une Instance EC2

#### 1.1. Lancement via Console AWS
1. Aller dans **EC2 Dashboard** → **Launch Instance**
2. **Nom**: `odoo-saas-tools-production`
3. **AMI**: Ubuntu Server 22.04 LTS (HVM, SSD Volume Type)
4. **Instance Type**: 
   - Développement: `t3.medium` (2 vCPU, 4 GB RAM)
   - Production: `t3.xlarge` (4 vCPU, 16 GB RAM) ou `m5.2xlarge`
5. **Key Pair**: Créer ou sélectionner une clé SSH
6. **Security Group**: 
   - SSH (22) depuis votre IP
   - HTTP (80) depuis partout (0.0.0.0/0)
   - HTTPS (443) depuis partout
   - Custom TCP 8069 depuis SG interne
7. **Storage**: 50-100 GB gp3 SSD
8. **Lancer l'instance**

#### 1.2. Lancement via AWS CLI
```bash
# Créer un security group
aws ec2 create-security-group \
    --group-name odoo-saas-sg \
    --description "Security group for Odoo SaaS Tools" \
    --vpc-id vpc-xxxxxxxxx

# Ajouter règles
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0  # Limiter à votre IP en production

aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Lancer l'instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.xlarge \
    --key-name votre-cle-ssh \
    --security-group-ids sg-xxxxxxxxx \
    --subnet-id subnet-xxxxxxxxx \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100,"VolumeType":"gp3"}}]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=odoo-saas-production}]'
```

### Étape 2: Configuration du Serveur

#### 2.1. Connexion SSH
```bash
ssh -i ~/.ssh/votre-cle.pem ubuntu@<IP_PUBLIQUE>
```

#### 2.2. Script d'Installation Automatisé
Créez le fichier `setup-aws.sh` sur votre serveur :

```bash
#!/bin/bash
set -e

echo "🚀 Configuration Odoo SaaS Tools sur AWS"

# Variables
PROJECT_DIR="/opt/odoo-saas-tools"
ODOO_USER="odoo"
POSTGRES_USER="odoo"
# ⚠️ CHANGEZ CE MOT DE PASSE EN PRODUCTION
POSTGRES_PASSWORD=$(openssl rand -hex 32)

# Mise à jour système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation dépendances
echo "🔧 Installation des dépendances..."
sudo apt install -y \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    postgresql-15 \
    postgresql-contrib \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    build-essential \
    libpq-dev \
    python3-dev \
    curl \
    wget \
    htop \
    ufw

# Configuration firewall
echo "🔥 Configuration firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Création utilisateur odoo
echo "👤 Création utilisateur..."
sudo useradd -m -s /bin/bash $ODOO_USER || true
sudo mkdir -p $PROJECT_DIR
sudo chown $ODOO_USER:$ODOO_USER $PROJECT_DIR

# Configuration PostgreSQL
echo "🗄️ Configuration PostgreSQL..."
sudo -u postgres psql << EOF
CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
CREATE DATABASE odoo OWNER $POSTGRES_USER;
GRANT ALL PRIVILEGES ON DATABASE odoo TO $POSTGRES_USER;
\q
EOF

# Configuration PostgreSQL pour acceptation connexions locales
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" /etc/postgresql/15/main/postgresql.conf

# Installation AWS CLI (si nécessaire)
if ! command -v aws &> /dev/null; then
    echo "📥 Installation AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
    unzip -q /tmp/awscliv2.zip -d /tmp
    sudo /tmp/aws/install
fi

# Installation boto3 pour intégration AWS
echo "📦 Installation boto3..."
sudo pip3 install boto3 boto

# Clonage projet (ou upload)
echo "📁 Configuration projet..."
cd $PROJECT_DIR
sudo -u $ODOO_USER git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git .

# Création environnement virtuel
echo "🐍 Configuration Python..."
sudo -u $ODOO_USER python3.11 -m venv venv
sudo -u $ODOO_USER venv/bin/pip install --upgrade pip
sudo -u $ODOO_USER venv/bin/pip install -r requirements.txt

# Configuration Odoo
echo "⚙️ Configuration Odoo..."
sudo -u $ODOO_USER cat > $PROJECT_DIR/odoo.conf << EOF
[options]
admin_passwd = ${POSTGRES_PASSWORD}
db_host = localhost
db_port = 5432
db_user = ${POSTGRES_USER}
db_password = ${POSTGRES_PASSWORD}
addons_path = ${PROJECT_DIR},/opt/odoo/addons
data_dir = ${PROJECT_DIR}/filestore
xmlrpc_port = 8069
workers = 4
max_cron_threads = 2
proxy_mode = True
EOF

# Configuration Nginx
echo "🌐 Configuration Nginx..."
DOMAIN_NAME="votre-domaine.com"  # ⚠️ CHANGEZ

sudo cat > /etc/nginx/sites-available/odoo << EOF
upstream odoo {
    server 127.0.0.1:8069;
}

server {
    listen 80;
    server_name ${DOMAIN_NAME} www.${DOMAIN_NAME};
    
    client_max_body_size 200M;
    
    location / {
        proxy_pass http://odoo;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 660s;
        proxy_connect_timeout 660s;
        proxy_send_timeout 660s;
    }
    
    # WebSocket support
    location /websocket {
        proxy_pass http://odoo;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# Certificat SSL (Let's Encrypt)
echo "🔒 Configuration SSL..."
sudo certbot --nginx -d ${DOMAIN_NAME} -d www.${DOMAIN_NAME} --non-interactive --agree-tos --email votre-email@example.com || true

# Service systemd
echo "🔧 Configuration service..."
sudo cat > /etc/systemd/system/odoo-saas.service << EOF
[Unit]
Description=Odoo SaaS Tools
After=postgresql.service network.target
Requires=postgresql.service

[Service]
Type=simple
User=${ODOO_USER}
Group=${ODOO_USER}
WorkingDirectory=${PROJECT_DIR}
Environment="PATH=${PROJECT_DIR}/venv/bin"
ExecStart=${PROJECT_DIR}/venv/bin/python3.11 ../odoo/odoo-bin -c ${PROJECT_DIR}/odoo.conf
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable odoo-saas
sudo systemctl start odoo-saas

# Vérification
echo "✅ Vérification installation..."
sleep 5
sudo systemctl status odoo-saas --no-pager

echo "✅ Déploiement terminé!"
echo "🌐 Accès: https://${DOMAIN_NAME}"
echo "📊 Status: sudo systemctl status odoo-saas"
echo "📝 Logs: sudo journalctl -u odoo-saas -f"
```

Exécutez le script :
```bash
chmod +x setup-aws.sh
sudo ./setup-aws.sh
```

### Étape 3: Configuration RDS (PostgreSQL)

Pour la production, utilisez Amazon RDS plutôt que PostgreSQL local :

```bash
# Créer un groupe de sous-réseaux
aws rds create-db-subnet-group \
    --db-subnet-group-name odoo-subnet-group \
    --db-subnet-group-description "Subnet group for Odoo RDS" \
    --subnet-ids subnet-xxx1 subnet-xxx2

# Créer l'instance RDS
aws rds create-db-instance \
    --db-instance-identifier odoo-production \
    --db-instance-class db.t3.medium \
    --engine postgres \
    --engine-version 15.4 \
    --master-username odoo \
    --master-user-password "VotreMotDePasseSecure" \
    --allocated-storage 100 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-subnet-group-name odoo-subnet-group \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted \
    --publicly-accessible false

# Mettre à jour odoo.conf avec l'endpoint RDS
# db_host = odoo-production.xxxxx.rds.amazonaws.com
```

---

## 🐳 Option 2: Déploiement avec ECS/Fargate

### Étape 1: Préparer l'Image Docker

```dockerfile
# Dockerfile.prod
FROM python:3.11-slim

WORKDIR /opt/odoo

# Installation dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier code source
COPY . .

# Créer utilisateur
RUN useradd -m -u 1000 odoo && chown -R odoo:odoo /opt/odoo
USER odoo

EXPOSE 8069

CMD ["python3.11", "../odoo/odoo-bin", "-c", "odoo.conf"]
```

### Étape 2: Créer l'Image et la Pousser vers ECR

```bash
# Créer un repository ECR
aws ecr create-repository --repository-name odoo-saas-tools

# Authentifier Docker
aws ecr get-login-password --region eu-west-1 | \
    docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com

# Build et tag
docker build -f Dockerfile.prod -t odoo-saas-tools:latest .
docker tag odoo-saas-tools:latest <ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com/odoo-saas-tools:latest

# Push
docker push <ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com/odoo-saas-tools:latest
```

### Étape 3: Créer la Tâche ECS

Créer `ecs-task-definition.json` :
```json
{
  "family": "odoo-saas-tools",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "odoo-saas",
      "image": "<ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com/odoo-saas-tools:latest",
      "portMappings": [
        {
          "containerPort": 8069,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DB_HOST", "value": "odoo-production.xxx.rds.amazonaws.com"},
        {"name": "DB_PORT", "value": "5432"},
        {"name": "DB_USER", "value": "odoo"},
        {"name": "DB_PASSWORD", "value": "your-password"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/odoo-saas-tools",
          "awslogs-region": "eu-west-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

```bash
# Enregistrer la définition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Créer un cluster
aws ecs create-cluster --cluster-name odoo-saas-cluster

# Créer un service
aws ecs create-service \
    --cluster odoo-saas-cluster \
    --service-name odoo-saas-service \
    --task-definition odoo-saas-tools \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx1,subnet-xxx2],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

---

## ☁️ Option 3: Déploiement avec Elastic Beanstalk

### Étape 1: Préparer l'Application

```bash
# Installer EB CLI
pip install awsebcli

# Initialiser
eb init -p "Docker running on 64bit Amazon Linux 2" odoo-saas-tools --region eu-west-1

# Créer environnement
eb create odoo-saas-prod \
    --instance-type t3.xlarge \
    --envvars DB_HOST=your-rds-endpoint,DB_USER=odoo,DB_PASSWORD=your-password
```

---

## 🌐 Configuration AWS

### Route53 (DNS)

1. **Créer une Zone Hosted**
```bash
aws route53 create-hosted-zone \
    --name votre-domaine.com \
    --caller-reference $(date +%s)
```

2. **Configurer les enregistrements DNS**
   - A Record pointant vers votre EC2/ALB
   - CNAME pour www

3. **Configurer dans Odoo** (avec module `saas_sysadmin_aws_route53`)
   - Aller dans **Système > SaaS > Configuration AWS**
   - Entrer Access Key ID et Secret Access Key
   - Configurer Route53 pour création automatique de sous-domaines

### S3 (Sauvegardes)

1. **Créer un bucket S3**
```bash
aws s3 mb s3://odoo-saas-backups-$(date +%s) \
    --region eu-west-1

# Activer versioning
aws s3api put-bucket-versioning \
    --bucket odoo-saas-backups-xxx \
    --versioning-configuration Status=Enabled
```

2. **Configurer dans Odoo** (avec module `saas_server_backup_s3`)
   - Configurer les credentials S3
   - Activer les backups automatiques

### CloudFront (CDN - Optionnel)

```bash
aws cloudfront create-distribution \
    --distribution-config file://cloudfront-config.json
```

---

## 🔒 Sécurité et Monitoring

### Security Groups

```bash
# Créer un SG pour Odoo
aws ec2 create-security-group \
    --group-name odoo-app-sg \
    --description "Odoo Application Security Group"

# Autoriser uniquement depuis ALB
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxx \
    --protocol tcp \
    --port 8069 \
    --source-group sg-alb-xxxxx
```

### IAM Roles

Créer un rôle IAM pour l'instance EC2 avec permissions :
- S3: PutObject, GetObject (pour backups)
- Route53: ChangeResourceRecordSets (pour DNS)
- CloudWatch: PutMetricData (pour monitoring)

### CloudWatch Monitoring

```bash
# Créer une alarme CPU
aws cloudwatch put-metric-alarm \
    --alarm-name odoo-high-cpu \
    --alarm-description "Alert when CPU exceeds 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

### Application Load Balancer

```bash
# Créer un ALB
aws elbv2 create-load-balancer \
    --name odoo-alb \
    --subnets subnet-xxx1 subnet-xxx2 \
    --security-groups sg-alb-xxxxx \
    --scheme internet-facing \
    --type application

# Créer un target group
aws elbv2 create-target-group \
    --name odoo-targets \
    --protocol HTTP \
    --port 8069 \
    --vpc-id vpc-xxxxx \
    --health-check-path /web/health \
    --health-check-interval-seconds 30

# Enregistrer les instances
aws elbv2 register-targets \
    --target-group-arn arn:aws:elasticloadbalancing:... \
    --targets Id=i-xxxxx1 Id=i-xxxxx2
```

---

## 💾 Backup et Restauration

### Backup Automatique vers S3

Avec le module `saas_server_backup_s3` :

1. Configurer les credentials S3 dans Odoo
2. Activer les backups automatiques
3. Configurer la rotation avec `saas_server_backup_rotate_s3`

### Script de Backup Manuel

```bash
#!/bin/bash
# backup-to-s3.sh

BACKUP_DIR="/tmp/odoo-backups"
BUCKET="s3://odoo-saas-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Créer backup PostgreSQL
pg_dump -U odoo odoo > $BACKUP_DIR/db_$DATE.sql

# Copier filestore
tar -czf $BACKUP_DIR/filestore_$DATE.tar.gz /opt/odoo-saas-tools/filestore

# Upload vers S3
aws s3 cp $BACKUP_DIR/db_$DATE.sql $BUCKET/databases/
aws s3 cp $BACKUP_DIR/filestore_$DATE.tar.gz $BUCKET/filestores/

# Nettoyer
rm -rf $BACKUP_DIR/*

echo "✅ Backup terminé: $DATE"
```

Ajouter au crontab :
```bash
0 2 * * * /opt/scripts/backup-to-s3.sh
```

---

## 📈 Optimisation et Scaling

### Auto Scaling Group

```bash
# Créer un Launch Template
aws ec2 create-launch-template \
    --launch-template-name odoo-launch-template \
    --launch-template-data file://launch-template-data.json

# Créer un Auto Scaling Group
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name odoo-asg \
    --launch-template LaunchTemplateName=odoo-launch-template \
    --min-size 2 \
    --max-size 10 \
    --desired-capacity 2 \
    --vpc-zone-identifier "subnet-xxx1,subnet-xxx2" \
    --target-group-arns arn:aws:elasticloadbalancing:... \
    --health-check-type ELB \
    --health-check-grace-period 300

# Créer une policy de scaling
aws autoscaling put-scaling-policy \
    --auto-scaling-group-name odoo-asg \
    --policy-name scale-up-cpu \
    --policy-type TargetTrackingScaling \
    --target-tracking-configuration '{
        "TargetValue": 70.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ASGAverageCPUUtilization"
        }
    }'
```

### RDS Read Replicas

Pour améliorer les performances :
```bash
aws rds create-db-instance-read-replica \
    --db-instance-identifier odoo-production-replica \
    --source-db-instance-identifier odoo-production
```

---

## 🔧 Dépannage

### Logs CloudWatch

```bash
# Voir les logs ECS
aws logs tail /ecs/odoo-saas-tools --follow

# Voir les logs EC2 (si configuré)
aws logs tail /aws/ec2/odoo --follow
```

### Connexion à l'instance

```bash
# Via Systems Manager (sans SSH)
aws ssm start-session --target i-xxxxx

# Via SSH classique
ssh -i key.pem ubuntu@<IP_PUBLIQUE>
```

### Monitoring Odoo

```bash
# Vérifier le statut
sudo systemctl status odoo-saas

# Voir les logs
sudo journalctl -u odoo-saas -f

# Vérifier PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT datname FROM pg_database;"
```

---

## 📝 Checklist de Déploiement

- [ ] Instance EC2 créée et configurée
- [ ] PostgreSQL installé ou RDS créé
- [ ] Projet cloné et dépendances installées
- [ ] Configuration Odoo complétée
- [ ] Nginx configuré avec SSL
- [ ] Service systemd créé et démarré
- [ ] Route53 configuré pour DNS
- [ ] S3 bucket créé pour backups
- [ ] Security Groups configurés
- [ ] CloudWatch monitoring activé
- [ ] Backup automatique configuré
- [ ] Test de connexion effectué
- [ ] Modules SaaS installés dans Odoo
- [ ] Configuration AWS (Route53, S3) dans Odoo

---

## 🔗 Ressources Utiles

- [Documentation AWS EC2](https://docs.aws.amazon.com/ec2/)
- [Documentation AWS RDS](https://docs.aws.amazon.com/rds/)
- [Documentation AWS ECS](https://docs.aws.amazon.com/ecs/)
- [Guide Odoo Production](https://www.odoo.com/documentation/18.0/administration/install.html)

---

**Note**: Ce guide est un point de départ. Adaptez-le selon vos besoins spécifiques et votre architecture AWS.

