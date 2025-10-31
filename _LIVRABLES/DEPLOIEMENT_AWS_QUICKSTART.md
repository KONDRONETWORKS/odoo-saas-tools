# 🚀 Quick Start: Déploiement AWS

## Déploiement Rapide en 3 Étapes

### Étape 1: Préparation Locale

```bash
# Installer AWS CLI
brew install awscli  # macOS
# ou
pip install awscli   # Linux/macOS

# Configurer vos credentials
aws configure
# AWS Access Key ID: [Votre clé]
# AWS Secret Access Key: [Votre secret]
# Default region: eu-west-1
# Default output: json

# Vérifier la connexion
aws sts get-caller-identity
```

### Étape 2: Créer une Instance EC2

**Option A: Via Script Automatique**
```bash
./deploy-aws.sh \
    --region eu-west-1 \
    --instance-type t3.xlarge \
    --key-name votre-cle-ssh \
    --domain votre-domaine.com \
    --email votre-email@example.com
```

**Option B: Via Console AWS**
1. EC2 Dashboard → Launch Instance
2. AMI: Ubuntu Server 22.04 LTS
3. Instance: t3.xlarge (ou t3.medium pour test)
4. Security Group: Autoriser SSH (22), HTTP (80), HTTPS (443)
5. Storage: 100 GB gp3
6. Lancer

### Étape 3: Configuration du Serveur

```bash
# Se connecter au serveur
ssh -i ~/.ssh/votre-cle.pem ubuntu@<IP_PUBLIQUE>

# Télécharger et exécuter le script de configuration
curl -o setup-server.sh https://raw.githubusercontent.com/KONDRONETWORKS/odoo-saas-tools/main/setup-aws-server.sh
chmod +x setup-server.sh
sudo ./setup-server.sh
```

## Configuration Minimale

### Variables à Configurer

Dans le script `setup-aws.sh`, modifiez :
- `DOMAIN_NAME`: votre domaine (ex: saas.exemple.com)
- `EMAIL`: votre email pour Let's Encrypt
- `POSTGRES_PASSWORD`: générer avec `openssl rand -hex 32`

### Modules Odoo à Installer

Une fois Odoo démarré, installez dans l'ordre :

1. **Base (OBLIGATOIRE)**
   - auth_oauth
   - auth_oauth_ip
   - auth_oauth_check_client_id
   - oauth_provider
   - saas_base

2. **Core (OBLIGATOIRE)**
   - saas_portal
   - saas_server
   - saas_client

3. **Interface (RECOMMANDÉ)**
   - saas_portal_portal
   - saas_portal_signup
   - saas_portal_start

4. **AWS (OPTIONNEL mais recommandé pour AWS)**
   - saas_sysadmin_aws
   - saas_sysadmin_aws_route53
   - saas_server_backup_s3

## Configuration AWS dans Odoo

1. Aller dans **Système > SaaS > Configuration AWS**
2. Entrer :
   - AWS Access Key ID
   - AWS Secret Access Key
3. Sauvegarder

### Créer un Utilisateur IAM pour Odoo

```bash
# Créer un utilisateur IAM
aws iam create-user --user-name odoo-saas

# Attacher la politique AmazonS3FullAccess (ou créer une politique custom)
aws iam attach-user-policy \
    --user-name odoo-saas \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Ajouter la politique Route53
aws iam attach-user-policy \
    --user-name odoo-saas \
    --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess

# Créer les credentials
aws iam create-access-key --user-name odoo-saas
```

## Checklist Post-Déploiement

- [ ] Instance EC2 démarrée et accessible
- [ ] Odoo accessible via navigateur
- [ ] SSL/HTTPS configuré (Let's Encrypt)
- [ ] Route53 configuré (si domaine fourni)
- [ ] S3 bucket créé pour backups
- [ ] Credentials AWS configurés dans Odoo
- [ ] Modules de base installés
- [ ] Test de création d'instance SaaS réussi
- [ ] Backups automatiques testés

## Commandes Utiles

```bash
# Voir les logs Odoo
sudo journalctl -u odoo-saas -f

# Redémarrer Odoo
sudo systemctl restart odoo-saas

# Vérifier le statut
sudo systemctl status odoo-saas

# Voir les instances EC2
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,PublicIpAddress,State.Name]" --output table

# Voir les logs CloudWatch (si configuré)
aws logs tail /aws/ec2/odoo --follow
```

## Support

Pour plus de détails, consultez:
- `_LIVRABLES/GUIDE_DEPLOIEMENT_AWS.md` - Guide complet
- Documentation AWS: https://docs.aws.amazon.com/
- Documentation Odoo: https://www.odoo.com/documentation/

