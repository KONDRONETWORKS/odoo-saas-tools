# 🚀 Guide de Déploiement AWS - CI/CD Complet

## 📋 Vue d'Ensemble

Ce guide vous explique comment configurer et utiliser le CI/CD pour déployer Odoo SaaS Tools sur AWS de manière automatisée.

## 🏗️ Architecture CI/CD

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Push/PR
                         ▼
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions (CI/CD)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   CI     │  │  Build   │  │   CD     │              │
│  │  Tests   │→ │  Docker  │→ │  Deploy  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
    ┌──────────────┐      ┌──────────────┐
    │  AWS ECR     │      │  AWS ECS     │
    │  (Images)    │      │  (Services)  │
    └──────────────┘      └──────────────┘
              │                     │
              └──────────┬──────────┘
                         ▼
              ┌──────────────┐
              │  Production  │
              │  Environment │
              └──────────────┘
```

## 🔧 Configuration Initiale

### 1. Prérequis

```bash
# Installer les outils
brew install awscli terraform docker  # macOS
# ou
sudo apt install awscli terraform docker.io  # Linux

# Vérifier l'installation
aws --version
terraform --version
docker --version
```

### 2. Configuration AWS

```bash
# Configurer AWS CLI
aws configure

# Vérifier les credentials
aws sts get-caller-identity
```

### 3. Configuration GitHub Secrets

Allez sur: `https://github.com/VOTRE_ORG/odoo-saas-tools/settings/secrets/actions`

**Secrets à ajouter:**

```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_EC2_INSTANCE_ID=i-xxxxxxxxxxxxx
AWS_EC2_HOST=ec2-xx-xx-xx-xx.compute.amazonaws.com
AWS_EC2_USER=ubuntu
AWS_SSH_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----...
AWS_APP_URL=https://votre-domaine.com
```

### 4. Configuration GitHub Environments

Allez sur: `Settings → Environments`

Créez:
- **staging** (pour les tests)
- **production** (pour la prod)

Ajoutez les mêmes secrets dans chaque environnement.

## 🚀 Déploiement

### Option 1: Déploiement Automatique (Recommandé)

```bash
# 1. Commit et push
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin main

# 2. GitHub Actions exécute automatiquement:
#    - Tests (CI)
#    - Build Docker
#    - Push vers ECR
#    - Déploiement AWS (CD)
```

### Option 2: Déploiement Manuel via GitHub UI

1. Aller sur: `https://github.com/VOTRE_ORG/odoo-saas-tools/actions`
2. Sélectionner "CD - Déploiement AWS"
3. Cliquer "Run workflow"
4. Choisir l'environnement (staging/production)
5. Cliquer "Run workflow"

### Option 3: Déploiement Local avec Script

```bash
# Rendre le script exécutable
chmod +x scripts/deploy-aws.sh

# Déploiement staging
./scripts/deploy-aws.sh staging

# Déploiement production
./scripts/deploy-aws.sh production
```

## 📊 Workflows Disponibles

### 1. CI - Tests et Validation

**Fichier:** `.github/workflows/ci.yml`

**Déclenchement:**
- Push sur `main` ou `develop`
- Pull Request

**Actions:**
- ✅ Tests unitaires avec PostgreSQL
- ✅ Lint (black, flake8, isort)
- ✅ Sécurité (bandit, safety)
- ✅ Build Docker

**Badge:**
```markdown
[![CI](https://github.com/VOTRE_ORG/odoo-saas-tools/workflows/CI/badge.svg)](https://github.com/VOTRE_ORG/odoo-saas-tools/actions)
```

### 2. CD - Déploiement AWS ECS

**Fichier:** `.github/workflows/cd-aws.yml`

**Déclenchement:**
- Push sur `main`
- Tags version `v*`
- Workflow manuel

**Actions:**
- ✅ Build et push Docker vers ECR
- ✅ Déploiement sur ECS
- ✅ Déploiement infrastructure Terraform
- ✅ Health check

### 3. CD - Déploiement AWS EC2

**Fichier:** `.github/workflows/deploy-aws-ec2.yml`

**Déclenchement:**
- Push sur `main`
- Workflow manuel

**Actions:**
- ✅ Backup automatique
- ✅ Mise à jour du code
- ✅ Migration base de données
- ✅ Redémarrage services
- ✅ Health check

### 4. Terraform - Infrastructure

**Fichier:** `.github/workflows/terraform.yml`

**Déclenchement:**
- Push sur `main` (changements Terraform)
- Pull Request (validation)

**Actions:**
- ✅ Validation Terraform
- ✅ Format check
- ✅ Plan Terraform
- ✅ Apply (production uniquement)

## 📝 Configuration Terraform

### 1. Créer terraform.tfvars

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Éditer terraform.tfvars avec vos valeurs
```

### 2. Variables Requises

```hcl
aws_region       = "us-east-1"
project_name     = "odoo-saas-tools"
environment      = "production"
domain_name      = "saas.votredomaine.com"
key_pair_name    = "votre-key-pair"
```

### 3. Initialiser Terraform

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

## 🔍 Monitoring

### GitHub Actions

- **Dashboard:** `https://github.com/VOTRE_ORG/odoo-saas-tools/actions`
- **Logs:** Cliquer sur un run pour voir les logs détaillés

### AWS Console

- **ECS:** `https://console.aws.amazon.com/ecs/`
- **ECR:** `https://console.aws.amazon.com/ecr/`
- **CloudWatch:** `https://console.aws.amazon.com/cloudwatch/`

### Vérification Déploiement

```bash
# Vérifier le service ECS
aws ecs describe-services \
  --cluster odoo-saas-cluster \
  --services odoo-saas-service \
  --region us-east-1

# Vérifier l'application
curl https://votre-domaine.com/web/health
```

## 🛠️ Troubleshooting

### Erreur: AWS credentials

```bash
# Vérifier les credentials
aws sts get-caller-identity

# Configurer si nécessaire
aws configure
```

### Erreur: ECR repository non trouvé

Le workflow crée automatiquement le repository ECR si nécessaire.

Sinon, créer manuellement:
```bash
aws ecr create-repository \
  --repository-name odoo-saas-tools-production \
  --region us-east-1
```

### Erreur: Tests échouent

```bash
# Exécuter les tests localement
python3 -m pytest tests/ -v

# Vérifier PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=odoo postgres:15
```

### Erreur: ECS service non trouvé

Vérifier que l'infrastructure Terraform est déployée:
```bash
cd infrastructure/terraform
terraform plan
terraform apply
```

## 🎯 Bonnes Pratiques

### 1. Branches

- `main`: Production (déploiement automatique)
- `develop`: Staging (tests)
- `feature/*`: Développement (tests uniquement)

### 2. Tags de Version

```bash
# Créer une version
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0

# Déclenche le déploiement automatique
```

### 3. Rollback

```bash
# Rollback ECS
aws ecs update-service \
  --cluster odoo-saas-cluster \
  --service odoo-saas-service \
  --task-definition previous-version \
  --region us-east-1
```

### 4. Sécurité

- ✅ Secrets dans GitHub Secrets (jamais en code)
- ✅ IAM roles avec permissions minimales
- ✅ Scan de sécurité automatique
- ✅ Rotation régulière des secrets

## 📚 Documentation Complémentaire

- **Guide CI/CD complet:** `docs/CI_CD_GUIDE.md`
- **Configuration Docker:** `config/README_DOCKER.md`
- **Infrastructure AWS:** `infrastructure/README.md`
- **Terraform:** `infrastructure/terraform/`

## 🚀 Quick Start

```bash
# 1. Configurer AWS
aws configure

# 2. Configurer GitHub Secrets
# (Via GitHub UI)

# 3. Push sur main
git push origin main

# 4. Vérifier le déploiement
# GitHub Actions → Voir les workflows
```

---

**Dernière mise à jour:** 4 Novembre 2025

