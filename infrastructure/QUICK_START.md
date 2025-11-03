# 🚀 Guide de Déploiement Production - Vue d'Ensemble

Ce dossier contient toute l'infrastructure nécessaire pour déployer Odoo SaaS Tools sur AWS en production.

## 📁 Structure des Fichiers

```
infrastructure/
├── README.md                    # Guide complet de déploiement
├── ARCHITECTURE.md              # Vue d'ensemble de l'architecture
├── deploy-aws-production.sh      # Script de déploiement automatisé
├── configure-odoo-aws.sh        # Script de configuration Odoo
├── .gitignore                   # Exclusions Git
├── config/
│   ├── odoo.conf.prod           # Configuration Odoo production
│   └── nginx.conf.prod          # Configuration Nginx production
└── terraform/
    ├── main.tf                  # Infrastructure principale
    ├── variables.tf             # Variables Terraform
    ├── outputs.tf               # Outputs Terraform
    ├── providers.tf             # Providers Terraform
    ├── backend.tf               # Backend S3 pour state
    ├── user-data.sh             # Script de configuration EC2
    └── terraform.tfvars.example # Exemple de variables
```

## 🚀 Démarrage Rapide

### 1. Préparer l'Environnement

```bash
# Installer les outils
brew install awscli terraform  # macOS
# ou
sudo apt install awscli terraform  # Linux

# Configurer AWS
aws configure
```

### 2. Configurer les Variables

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Éditer terraform.tfvars avec vos valeurs
```

### 3. Déployer

```bash
# Depuis la racine du projet
./infrastructure/deploy-aws-production.sh
```

### 4. Configurer Odoo

```bash
# Après le déploiement
./infrastructure/configure-odoo-aws.sh
```

## 📚 Documentation

- **[README.md](README.md)** : Guide complet pas à pas
- **[ARCHITECTURE.md](ARCHITECTURE.md)** : Vue d'ensemble de l'architecture AWS

## 🔧 Maintenance

### Mise à jour de l'Infrastructure

```bash
cd infrastructure/terraform
terraform plan
terraform apply
```

### Voir les Outputs

```bash
cd infrastructure/terraform
terraform output
```

### Détruire l'Infrastructure

```bash
cd infrastructure/terraform
terraform destroy
```

## ⚠️ Important

- Ne commitez jamais `terraform.tfvars` avec des credentials
- Sauvegardez le mot de passe RDS de manière sécurisée
- Restreignez l'accès SSH (`allowed_ssh_cidr`)
- Utilisez un utilisateur IAM dédié pour Odoo, pas vos credentials root

## 📞 Support

Pour plus d'informations, consultez la documentation dans `_LIVRABLES/GUIDE_DEPLOIEMENT_AWS.md`

