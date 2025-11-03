# 🚀 Guide de Déploiement AWS - Production

Ce guide explique comment déployer votre plateforme Odoo SaaS Tools sur AWS en production en utilisant Terraform.

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Architecture](#architecture)
3. [Configuration Initiale](#configuration-initiale)
4. [Déploiement](#déploiement)
5. [Post-Déploiement](#post-déploiement)
6. [Monitoring](#monitoring)
7. [Dépannage](#dépannage)

---

## 📦 Prérequis

### Outils Requis

- **AWS CLI** : Installé et configuré avec vos credentials
- **Terraform** : Version >= 1.0
- **Une clé SSH AWS** : Créée dans AWS EC2
- **Un domaine** : Configuré et accessible pour Route53

### Installation des Outils

#### macOS
```bash
# AWS CLI
brew install awscli

# Terraform
brew install terraform

# Configuration AWS
aws configure
```

#### Linux
```bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

### Vérification

```bash
# Vérifier AWS CLI
aws --version
aws sts get-caller-identity

# Vérifier Terraform
terraform version
```

---

## 🏗️ Architecture

L'infrastructure déployée comprend :

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

### Composants

- **VPC** : Réseau virtuel isolé avec subnets publics et privés
- **Application Load Balancer** : Répartition de charge et SSL termination
- **Auto Scaling Group** : Scaling automatique selon la charge
- **RDS PostgreSQL** : Base de données Multi-AZ haute disponibilité
- **S3** : Stockage pour backups et filestore
- **Route53** : Gestion DNS
- **CloudWatch** : Monitoring et logs
- **ACM** : Certificats SSL

---

## ⚙️ Configuration Initiale

### 1. Créer une Clé SSH AWS

```bash
# Créer la clé dans AWS
aws ec2 create-key-pair \
    --key-name odoo-saas-key \
    --query 'KeyMaterial' \
    --output text > ~/.ssh/odoo-saas-key.pem

# Sécuriser la clé
chmod 400 ~/.ssh/odoo-saas-key.pem
```

### 2. Configurer Terraform Variables

Copiez le fichier d'exemple et modifiez-le :

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
```

Éditez `terraform.tfvars` :

```hcl
aws_region = "eu-west-1"
project_name = "odoo-saas"
domain_name = "saas.votre-domaine.com"
environment = "production"

instance_type = "t3.xlarge"
db_instance_class = "db.t3.medium"
db_allocated_storage = 100

key_pair_name = "odoo-saas-key"
allowed_ssh_cidr = "123.45.67.89/32"  # Votre IP publique

min_instances = 2
max_instances = 10
desired_capacity = 2
```

### 3. Créer le Bucket S3 pour Terraform State

Le script de déploiement le créera automatiquement, mais vous pouvez le faire manuellement :

```bash
aws s3 mb s3://odoo-saas-terraform-state --region eu-west-1
aws s3api put-bucket-versioning \
    --bucket odoo-saas-terraform-state \
    --versioning-configuration Status=Enabled

# Table DynamoDB pour locking
aws dynamodb create-table \
    --table-name terraform-state-lock \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region eu-west-1
```

---

## 🚀 Déploiement

### Déploiement Automatique (Recommandé)

```bash
# Rendre le script exécutable
chmod +x infrastructure/deploy-aws-production.sh

# Exécuter le déploiement
./infrastructure/deploy-aws-production.sh
```

Le script va :
1. Vérifier les prérequis
2. Initialiser Terraform
3. Planifier les changements
4. Demander confirmation
5. Déployer l'infrastructure
6. Afficher les informations importantes

### Déploiement Manuel avec Terraform

```bash
cd infrastructure/terraform

# Initialiser
terraform init

# Planifier
terraform plan

# Appliquer
terraform apply
```

---

## 📝 Post-Déploiement

### 1. Configurer le DNS

Récupérez les name servers Route53 :

```bash
cd infrastructure/terraform
terraform output route53_name_servers
```

Configurez votre domaine pour utiliser ces name servers.

### 2. Valider le Certificat SSL

Le certificat ACM doit être validé via DNS. Une fois le DNS configuré, le certificat sera validé automatiquement.

### 3. Récupérer les Informations de Connexion

```bash
cd infrastructure/terraform

# URL de l'application
terraform output application_url

# Endpoint RDS (mot de passe dans outputs)
terraform output rds_endpoint

# Buckets S3
terraform output s3_backups_bucket
terraform output s3_filestore_bucket
```

### 4. Configurer AWS dans Odoo

1. Connectez-vous à Odoo via l'URL de l'application
2. Installez les modules :
   - `saas_sysadmin_aws`
   - `saas_sysadmin_aws_route53`
   - `saas_server_backup_s3`
3. Configurez les credentials AWS dans **Système > SaaS > Configuration AWS**
4. Utilisez les valeurs des outputs Terraform

### 5. Créer un Utilisateur IAM pour Odoo

```bash
# Créer l'utilisateur
aws iam create-user --user-name odoo-saas-app

# Attacher les politiques
aws iam attach-user-policy \
    --user-name odoo-saas-app \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-user-policy \
    --user-name odoo-saas-app \
    --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess

# Créer les credentials
aws iam create-access-key --user-name odoo-saas-app
```

**⚠️ Important** : Utilisez ces credentials dans Odoo, pas vos credentials AWS root.

---

## 📊 Monitoring

### CloudWatch Logs

```bash
# Voir les logs Odoo
aws logs tail /aws/ec2/odoo-saas --follow

# Voir les logs d'une instance spécifique
aws logs tail /aws/ec2/odoo-saas --filter-pattern "INSTANCE_ID" --follow
```

### CloudWatch Metrics

- CPU Utilization
- Memory Utilization
- Network In/Out
- RDS Connections
- ALB Request Count

### Alertes

Des alertes CloudWatch sont configurées automatiquement pour :
- CPU > 80%
- Mémoire > 85%
- RDS CPU > 80%
- Health check failures

---

## 🔧 Dépannage

### Vérifier le Statut des Instances

```bash
# Lister les instances
aws ec2 describe-instances \
    --filters "Name=tag:Project,Values=odoo-saas" \
    --query "Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]"

# Vérifier les logs d'une instance
aws ssm start-session --target i-xxxxx
```

### Vérifier RDS

```bash
# Statut RDS
aws rds describe-db-instances \
    --db-instance-identifier odoo-saas-db

# Logs RDS
aws rds describe-db-log-files \
    --db-instance-identifier odoo-saas-db
```

### Vérifier l'ALB

```bash
# Health checks
aws elbv2 describe-target-health \
    --target-group-arn $(terraform output -raw target_group_arn)
```

### Connexion SSH à une Instance

```bash
# Obtenir l'IP publique
INSTANCE_IP=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=odoo-saas-instance" \
    --query "Reservations[0].Instances[0].PublicIpAddress" \
    --output text)

# Se connecter
ssh -i ~/.ssh/odoo-saas-key.pem ubuntu@$INSTANCE_IP
```

### Logs Odoo sur l'Instance

```bash
# Via SSH
sudo journalctl -u odoo-saas -f
sudo tail -f /var/log/odoo/odoo.log
sudo tail -f /var/log/nginx/odoo-error.log
```

---

## 🔄 Mise à Jour

### Mettre à Jour l'Infrastructure

```bash
cd infrastructure/terraform

# Voir les changements
terraform plan

# Appliquer
terraform apply
```

### Mettre à Jour l'Application

Les instances sont configurées automatiquement via user-data. Pour forcer une mise à jour :

```bash
# Redémarrer les instances dans l'ASG
aws autoscaling start-instance-refresh \
    --auto-scaling-group-name odoo-saas-asg
```

---

## 🗑️ Destruction

**⚠️ ATTENTION** : Cela supprimera toute l'infrastructure !

```bash
cd infrastructure/terraform
terraform destroy
```

---

## 📚 Ressources

- [Documentation Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Guide AWS RDS](https://docs.aws.amazon.com/rds/)
- [Guide AWS EC2](https://docs.aws.amazon.com/ec2/)
- [Guide AWS ALB](https://docs.aws.amazon.com/elasticloadbalancing/)

---

## ✅ Checklist de Déploiement

- [ ] AWS CLI installé et configuré
- [ ] Terraform installé
- [ ] Clé SSH AWS créée
- [ ] `terraform.tfvars` configuré
- [ ] Bucket S3 pour Terraform state créé
- [ ] Infrastructure déployée avec Terraform
- [ ] DNS configuré pour Route53
- [ ] Certificat SSL validé
- [ ] Odoo accessible via HTTPS
- [ ] Modules SaaS installés dans Odoo
- [ ] Credentials AWS configurés dans Odoo
- [ ] Backups S3 testés
- [ ] Monitoring CloudWatch configuré
- [ ] Alertes configurées

---

**Note** : Adaptez les valeurs selon vos besoins spécifiques (taille d'instance, région, etc.)

