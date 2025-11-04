# 🚀 GitHub Actions - CI/CD Workflows

## 📋 Workflows Disponibles

### 1. `ci.yml` - Continuous Integration
**Déclenchement:** Push/PR sur `main` ou `develop`

**Actions:**
- ✅ Tests unitaires avec PostgreSQL
- ✅ Lint et formatage (black, flake8, isort)
- ✅ Analyse de sécurité (bandit, safety)
- ✅ Build Docker images

### 2. `cd-aws.yml` - Continuous Deployment AWS ECS
**Déclenchement:** Push sur `main`, tags `v*`, ou manuel

**Actions:**
- ✅ Build et push Docker vers ECR
- ✅ Déploiement sur ECS
- ✅ Déploiement infrastructure Terraform
- ✅ Notifications

### 3. `deploy-aws-ec2.yml` - Déploiement AWS EC2
**Déclenchement:** Push sur `main` ou manuel

**Actions:**
- ✅ Déploiement via SSH sur EC2
- ✅ Backup automatique
- ✅ Migration base de données
- ✅ Health check

### 4. `terraform.yml` - Infrastructure as Code
**Déclenchement:** Changements Terraform, PR

**Actions:**
- ✅ Validation Terraform
- ✅ Format check
- ✅ Plan et Apply (production)

## 🔧 Configuration Requise

### Secrets GitHub

Ajoutez dans: `Settings → Secrets and variables → Actions`

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_EC2_INSTANCE_ID (pour EC2)
AWS_EC2_HOST (pour EC2)
AWS_EC2_USER (pour EC2)
AWS_SSH_PRIVATE_KEY (pour EC2)
AWS_APP_URL
```

### Environments

Créez dans: `Settings → Environments`

- `staging`
- `production`

## 📚 Documentation

Voir `docs/CI_CD_GUIDE.md` pour le guide complet.

