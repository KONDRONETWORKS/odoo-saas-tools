# 📋 Prérequis Complets - Infrastructure AWS

## 🎯 Checklist Complète

### 1. Prérequis AWS Account

#### Compte AWS
- [ ] Compte AWS créé et actif
- [ ] Email de vérification confirmé
- [ ] MFA activé (recommandé)
- [ ] Budget configuré avec alertes
- [ ] IAM User créé (pas le root)

#### Configuration Budget
```bash
# Créer un budget dans AWS Console
# Budget: $500-800/mois
# Alertes: 50%, 80%, 100%
```

#### Région AWS
- [ ] Région choisie (us-east-1 recommandé)
- [ ] Vérifier disponibilité des services
- [ ] Latence acceptable

### 2. Prérequis Domaine et DNS

#### Domaine
- [ ] Nom de domaine principal acheté/configuré
  - Exemple: `saas.votredomaine.com`
- [ ] Accès au registrar DNS
- [ ] Autorité pour modifier DNS

#### DNS
- [ ] Zone DNS créée dans Route 53 OU
- [ ] Accès au DNS actuel pour configuration
- [ ] Enregistrements A/CNAME configurés

#### Certificat SSL
- [ ] Certificat SSL/TLS (via AWS Certificate Manager)
- [ ] Validation DNS ou Email
- [ ] Certificat valide pour le domaine

### 3. Prérequis Techniques Locaux

#### Outils Requis
```bash
# AWS CLI
aws --version  # Doit être >= 2.0
# Installation: brew install awscli (macOS)

# Terraform
terraform --version  # Doit être >= 1.6.0
# Installation: brew install terraform (macOS)

# Docker (pour tests locaux)
docker --version
# Installation: brew install docker (macOS)

# Git
git --version
# Installation: brew install git (macOS)
```

#### Configuration AWS CLI
```bash
# Configurer AWS CLI
aws configure

# Vérifier les credentials
aws sts get-caller-identity

# Doit retourner:
# {
#   "UserId": "...",
#   "Account": "...",
#   "Arn": "..."
# }
```

#### Configuration Git
```bash
# Configurer Git
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"

# Vérifier accès GitHub
git remote -v
```

### 4. Prérequis GitHub

#### Repository
- [ ] Repository GitHub créé
- [ ] Code pushé sur GitHub
- [ ] Accès en écriture au repository

#### GitHub Secrets
- [ ] Accès à `Settings → Secrets and variables → Actions`
- [ ] Secrets configurés (voir section suivante)

#### GitHub Environments
- [ ] Accès à `Settings → Environments`
- [ ] Environnements créés: `staging`, `production`

### 5. Prérequis Terraform

#### Configuration Terraform
```bash
cd infrastructure/terraform

# Créer terraform.tfvars
cp terraform.tfvars.example terraform.tfvars

# Éditer terraform.tfvars
# Variables requises:
# - aws_region
# - project_name
# - environment
# - domain_name
# - key_pair_name
```

#### Backend Terraform (Optionnel mais Recommandé)
```bash
# Créer bucket S3 pour state
aws s3 mb s3://odoo-saas-terraform-state --region us-east-1

# Activer versioning
aws s3api put-bucket-versioning \
  --bucket odoo-saas-terraform-state \
  --versioning-configuration Status=Enabled
```

### 6. Prérequis IAM et Permissions

#### IAM User avec Permissions

**Politique IAM Recommandée:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:*",
        "ecr:*",
        "rds:*",
        "s3:*",
        "elasticloadbalancing:*",
        "route53:*",
        "cloudwatch:*",
        "acm:*",
        "ec2:*",
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "iam:CreateInstanceProfile",
        "iam:AddRoleToInstanceProfile",
        "logs:*",
        "cloudfront:*"
      ],
      "Resource": "*"
    }
  ]
}
```

**OU utiliser les politiques AWS gérées:**
- `AmazonECS_FullAccess`
- `AmazonRDS_FullAccess`
- `AmazonS3FullAccess`
- `ElasticLoadBalancingFullAccess`
- `Route53FullAccess`
- `CloudWatchFullAccess`
- `AWSCertificateManagerFullAccess`

#### Key Pair SSH (pour EC2 si nécessaire)
```bash
# Créer une key pair AWS
aws ec2 create-key-pair \
  --key-name odoo-saas-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/odoo-saas-key.pem

chmod 400 ~/.ssh/odoo-saas-key.pem
```

### 7. Prérequis Financiers

#### Budget Initial
- **Infrastructure staging:** $200-300/mois
- **Infrastructure production:** $431-551/mois
- **Configuration initiale:** $500-1,000 (temps DevOps)
- **Domaine:** $10-50/an
- **Total première année:** $8,000-10,000

#### Budget Mensuel Recommandé
- **Staging:** $200-300
- **Production:** $431-551
- **Total:** $631-851/mois

#### Alertes Budget
- [ ] Budget configuré dans AWS
- [ ] Alertes à 50%, 80%, 100%
- [ ] Email notifications configurées

### 8. Prérequis Organisationnels

#### Équipe
- [ ] 1 DevOps Engineer disponible (4 semaines)
- [ ] Accès GitHub pour l'équipe
- [ ] Accès AWS Console pour l'équipe
- [ ] Support technique disponible

#### Autorisations
- [ ] Budget approuvé par la direction
- [ ] Autorisation infrastructure cloud
- [ ] Autorisation dépenses AWS
- [ ] Accès aux domaines
- [ ] Autorisation CI/CD

#### Communication
- [ ] Stakeholders informés
- [ ] Timeline partagée
- [ ] Points de contrôle définis

### 9. Prérequis Spécifiques AWS

#### Services AWS à Activer

**Services Core:**
- [ ] ECS (Elastic Container Service)
- [ ] Fargate
- [ ] ECR (Elastic Container Registry)
- [ ] RDS (Relational Database Service)
- [ ] S3 (Simple Storage Service)
- [ ] VPC (Virtual Private Cloud)

**Services Networking:**
- [ ] Application Load Balancer (ALB)
- [ ] Route 53 (DNS)
- [ ] CloudFront (CDN)

**Services Monitoring:**
- [ ] CloudWatch (Logs & Metrics)
- [ ] CloudTrail (Audit)

**Services Security:**
- [ ] ACM (Certificate Manager)
- [ ] IAM (Identity and Access Management)
- [ ] Secrets Manager (optionnel)

#### Limites de Service

Vérifier les limites AWS:
```bash
# Vérifier les limites ECS
aws service-quotas get-service-quota \
  --service-code ecs \
  --quota-code L-3033A538

# Vérifier les limites RDS
aws service-quotas get-service-quota \
  --service-code rds \
  --quota-code L-7B6409FD
```

Si nécessaire, demander une augmentation:
```bash
# Demander augmentation
aws service-quotas request-service-quota-increase \
  --service-code ecs \
  --quota-code L-3033A538 \
  --desired-value 10
```

### 10. Prérequis Sécurité

#### MFA (Multi-Factor Authentication)
- [ ] MFA activé sur compte AWS root
- [ ] MFA activé sur IAM users
- [ ] Appareil MFA configuré

#### Secrets Management
- [ ] AWS Secrets Manager configuré (optionnel)
- [ ] Secrets GitHub configurés
- [ ] Pas de secrets en code

#### Audit
- [ ] CloudTrail activé
- [ ] Logs archivés
- [ ] Accès auditables

### 11. Prérequis Monitoring

#### CloudWatch
- [ ] CloudWatch Logs activé
- [ ] CloudWatch Metrics activé
- [ ] Alertes configurées

#### Notifications
- [ ] SNS Topic créé
- [ ] Email notifications configurées
- [ ] Slack/Teams intégration (optionnel)

### 12. Prérequis Backup

#### RDS Backups
- [ ] Automated backups activés
- [ ] Rétention configurée (7-35 jours)
- [ ] Backup window configurée

#### S3 Backups
- [ ] Bucket S3 pour backups créé
- [ ] Versioning activé
- [ ] Lifecycle policies configurées

---

## ✅ Checklist de Validation

### Avant Déploiement

#### Technique
- [ ] AWS Account créé et configuré
- [ ] AWS CLI installé et configuré
- [ ] Terraform installé
- [ ] Docker installé (pour tests)
- [ ] Git configuré
- [ ] GitHub repository accessible

#### Infrastructure
- [ ] Domaine configuré
- [ ] Certificat SSL obtenu
- [ ] Terraform variables configurées
- [ ] IAM permissions vérifiées
- [ ] Key pair créée (si EC2)

#### Organisationnel
- [ ] Budget approuvé
- [ ] Équipe disponible
- [ ] Autorisations obtenues
- [ ] Timeline validée

#### Sécurité
- [ ] MFA activé
- [ ] Secrets configurés
- [ ] Audit activé
- [ ] Monitoring configuré

### Après Déploiement

#### Validation
- [ ] Infrastructure déployée
- [ ] Application accessible
- [ ] Tests réussis
- [ ] Monitoring fonctionnel
- [ ] Backups vérifiés

---

## 🚀 Commandes de Vérification

### Vérifier AWS Setup
```bash
# Vérifier credentials
aws sts get-caller-identity

# Vérifier région
aws configure get region

# Lister les services disponibles
aws ec2 describe-regions
```

### Vérifier Terraform
```bash
cd infrastructure/terraform
terraform init
terraform validate
terraform plan
```

### Vérifier Docker
```bash
docker ps
docker build -t test -f config/Dockerfile .
```

### Vérifier Git
```bash
git remote -v
git status
```

---

## 📚 Documentation à Consulter

- **Architecture recommandée:** `ARCHITECTURE_RECOMMANDEE.md`
- **Présentation direction:** `PRESENTATION_DIRECTION.md`
- **Guide CI/CD:** `../docs/CI_CD_GUIDE.md`
- **Guide déploiement:** `../GUIDE_DEPLOIEMENT_AWS.md`

---

## 🆘 Support

En cas de problème:
1. Consulter la documentation
2. Vérifier les logs CloudWatch
3. Contacter: apps@itexperts4africa.com

---

**Dernière mise à jour:** 4 Novembre 2025

