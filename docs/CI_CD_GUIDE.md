# 🚀 Guide CI/CD - Déploiement AWS

## 📋 Vue d'Ensemble

Ce guide explique comment configurer et utiliser le CI/CD pour déployer Odoo SaaS Tools sur AWS.

## 🏗️ Architecture CI/CD

```
┌─────────────────┐
│   GitHub Push    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GitHub Actions │
│   (CI Workflow) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Tests  │ │ Lint   │
└────────┘ └────────┘
    │
    ▼
┌─────────────────┐
│  Build Docker   │
│  Push to ECR    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deploy AWS     │
│  (CD Workflow)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│  ECS   │ │  EC2   │
└────────┘ └────────┘
```

## 📁 Structure des Workflows

```
.github/workflows/
├── ci.yml              # Tests et validation
├── cd-aws.yml          # Déploiement AWS (ECS)
├── deploy-aws-ec2.yml  # Déploiement AWS (EC2)
└── terraform.yml       # Infrastructure as Code
```

## 🔧 Configuration

### 1. Secrets GitHub

Ajoutez ces secrets dans GitHub → Settings → Secrets → Actions:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# AWS Resources
AWS_REGION=us-east-1
AWS_EC2_INSTANCE_ID=i-xxxxxxxxxxxxx
AWS_EC2_HOST=ec2-xx-xx-xx-xx.compute.amazonaws.com
AWS_EC2_USER=ubuntu
AWS_SSH_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----...

# Application
AWS_APP_URL=https://your-domain.com
```

### 2. Variables d'Environnement

Dans GitHub → Settings → Environments → production:

- `AWS_REGION`: us-east-1
- `ECR_REPOSITORY`: odoo-saas-tools
- `ECS_CLUSTER`: odoo-saas-cluster
- `ECS_SERVICE`: odoo-saas-service

## 🚀 Workflows Disponibles

### 1. CI - Tests et Validation (`ci.yml`)

**Déclenchement:**
- Push sur `main` ou `develop`
- Pull Request

**Actions:**
- ✅ Tests unitaires avec PostgreSQL
- ✅ Lint et formatage (black, flake8, isort)
- ✅ Analyse de sécurité (bandit, safety)
- ✅ Build Docker images

**Utilisation:**
```bash
# Automatique sur push/PR
git push origin main
```

### 2. CD - Déploiement AWS ECS (`cd-aws.yml`)

**Déclenchement:**
- Push sur `main`
- Tags version `v*`
- Workflow manuel

**Actions:**
- ✅ Build et push Docker vers ECR
- ✅ Déploiement sur ECS
- ✅ Déploiement infrastructure Terraform
- ✅ Notifications

**Utilisation:**
```bash
# Automatique sur push main
git push origin main

# Manuel via GitHub UI
# Actions → CD - Déploiement AWS → Run workflow
```

### 3. CD - Déploiement AWS EC2 (`deploy-aws-ec2.yml`)

**Déclenchement:**
- Push sur `main`
- Workflow manuel

**Actions:**
- ✅ Déploiement via SSH sur EC2
- ✅ Backup automatique
- ✅ Mise à jour du code
- ✅ Migration base de données
- ✅ Redémarrage services
- ✅ Health check

**Utilisation:**
```bash
# Automatique sur push main
git push origin main

# Manuel
# Actions → CD - Déploiement AWS EC2 → Run workflow
```

### 4. Terraform - Infrastructure (`terraform.yml`)

**Déclenchement:**
- Push sur `main` (changements Terraform)
- Pull Request (validation)

**Actions:**
- ✅ Validation Terraform
- ✅ Format check
- ✅ Plan Terraform
- ✅ Apply (production uniquement)

## 📝 Utilisation

### Déploiement Automatique

```bash
# 1. Commit et push
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin main

# 2. GitHub Actions exécute automatiquement:
#    - CI: Tests et validation
#    - CD: Build et déploiement AWS
```

### Déploiement Manuel

1. Aller sur GitHub → Actions
2. Sélectionner le workflow (ex: "CD - Déploiement AWS")
3. Cliquer "Run workflow"
4. Choisir l'environnement (staging/production)
5. Cliquer "Run workflow"

### Déploiement Local avec Script

```bash
# Déploiement staging
./scripts/deploy-aws.sh staging

# Déploiement production
./scripts/deploy-aws.sh production
```

## 🔍 Monitoring

### Logs GitHub Actions

- GitHub → Actions → Voir les runs
- Cliquer sur un run pour voir les logs détaillés

### Vérification Déploiement

```bash
# Vérifier le service ECS
aws ecs describe-services \
  --cluster odoo-saas-cluster \
  --services odoo-saas-service \
  --region us-east-1

# Vérifier l'application
curl https://your-domain.com/web/health
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

```bash
# Créer le repository
aws ecr create-repository \
  --repository-name odoo-saas-tools-production \
  --region us-east-1
```

### Erreur: ECS service non trouvé

```bash
# Vérifier le cluster
aws ecs list-clusters --region us-east-1

# Créer le service si nécessaire
# Via Terraform ou manuellement
```

### Erreur: Tests échouent

```bash
# Exécuter les tests localement
python3 -m pytest tests/ -v

# Vérifier PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=odoo postgres:15
```

## 📊 Dashboard

### GitHub Actions

- **URL:** `https://github.com/VOTRE_ORG/odoo-saas-tools/actions`
- **Badge:** `[![CI](https://github.com/VOTRE_ORG/odoo-saas-tools/workflows/CI/badge.svg)](https://github.com/VOTRE_ORG/odoo-saas-tools/actions)`

### AWS Console

- **ECS:** `https://console.aws.amazon.com/ecs/`
- **ECR:** `https://console.aws.amazon.com/ecr/`
- **CloudWatch:** `https://console.aws.amazon.com/cloudwatch/`

## 🎯 Bonnes Pratiques

### 1. Branches

- `main`: Production
- `develop`: Staging
- `feature/*`: Développement

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
- ✅ Scan de sécurité (bandit, safety)
- ✅ Secrets rotation régulière

## 📚 Documentation Complémentaire

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

**Dernière mise à jour:** 4 Novembre 2025

