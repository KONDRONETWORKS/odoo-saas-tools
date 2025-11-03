# 🏗️ Infrastructure AWS - Vue d'ensemble

## Architecture Déployée

Cette infrastructure AWS complète permet de déployer Odoo SaaS Tools en production avec haute disponibilité, scalabilité et sécurité.

## Composants Principaux

### 1. Réseau (VPC)
- **VPC** : 10.0.0.0/16 avec DNS activé
- **Subnets Publics** : 2 subnets dans 2 Availability Zones pour ALB et EC2
- **Subnets Privés** : 2 subnets dans 2 Availability Zones pour RDS
- **Internet Gateway** : Connexion Internet
- **Route Tables** : Configuration du routage

### 2. Calcul (EC2)
- **Auto Scaling Group** : 2-10 instances selon la charge
- **Launch Template** : Configuration standardisée des instances
- **Instance Type** : t3.xlarge (4 vCPU, 16 GB RAM) par défaut
- **User Data** : Configuration automatique au démarrage
- **IAM Role** : Permissions pour S3, Route53, CloudWatch

### 3. Base de Données (RDS)
- **Moteur** : PostgreSQL 15.4
- **Instance** : db.t3.medium (Multi-AZ pour HA)
- **Stockage** : 100 GB gp3 chiffré
- **Backups** : 7 jours de rétention, backups automatiques
- **Sécurité** : Accessible uniquement depuis les instances EC2

### 4. Load Balancing (ALB)
- **Type** : Application Load Balancer
- **HTTPS** : Certificat SSL via ACM
- **Health Checks** : Monitoring automatique
- **Sticky Sessions** : Support des sessions utilisateur
- **Multi-AZ** : Distribution sur 2 Availability Zones

### 5. Stockage (S3)
- **Backups Bucket** : Sauvegardes automatiques avec versioning
- **Filestore Bucket** : Stockage des fichiers utilisateurs
- **Chiffrement** : AES-256
- **Lifecycle** : Suppression automatique après 90 jours

### 6. DNS (Route53)
- **Hosted Zone** : Gestion DNS automatique
- **Records** : Configuration A et CNAME
- **Health Checks** : Monitoring DNS

### 7. Monitoring (CloudWatch)
- **Logs** : Centralisation des logs Odoo, Nginx
- **Metrics** : CPU, Memory, Network, RDS
- **Alarms** : Alertes automatiques
- **Rétention** : 30 jours

### 8. Sécurité
- **Security Groups** : Pare-feu pour ALB, EC2, RDS
- **SSL/TLS** : Certificats ACM avec renouvellement automatique
- **IAM** : Permissions minimales requises
- **Encryption** : Chiffrement au repos (RDS, S3) et en transit (HTTPS)

## Coûts Estimés (Région eu-west-1)

### Mensuel (approximatif)

| Service | Configuration | Coût/mois |
|---------|--------------|-----------|
| EC2 (2x t3.xlarge) | 2 instances | ~$300 |
| RDS (db.t3.medium Multi-AZ) | 1 instance | ~$150 |
| ALB | 1 load balancer | ~$20 |
| S3 | 100 GB storage | ~$3 |
| Route53 | 1 hosted zone | ~$0.50 |
| CloudWatch | Logs + metrics | ~$10 |
| Data Transfer | 100 GB | ~$10 |
| **Total** | | **~$493/mois** |

**Note** : Ces coûts sont approximatifs et varient selon l'utilisation réelle.

## Haute Disponibilité

- ✅ **Multi-AZ** : RDS et instances EC2 dans plusieurs zones
- ✅ **Auto Scaling** : Ajout automatique d'instances en cas de charge
- ✅ **Health Checks** : Redirection automatique en cas de panne
- ✅ **Backups** : Sauvegardes quotidiennes avec rétention 7 jours
- ✅ **Monitoring** : Surveillance 24/7 avec alertes

## Scalabilité

- **Horizontal** : Auto Scaling Group (2-10 instances)
- **Vertical** : Modification du type d'instance possible
- **Base de données** : Read replicas disponibles
- **Stockage** : S3 scalable automatiquement

## Sécurité

- ✅ **Isolation réseau** : VPC privé avec subnets isolés
- ✅ **Chiffrement** : Données au repos et en transit
- ✅ **SSL/TLS** : Certificats automatiques via ACM
- ✅ **IAM** : Permissions minimales avec rôles
- ✅ **Firewall** : Security Groups restrictifs
- ✅ **Backups** : Sauvegardes chiffrées et versionnées

## Points d'Attention

1. **SSH Access** : Restreindre `allowed_ssh_cidr` à votre IP
2. **Admin Password** : Changer le mot de passe admin Odoo
3. **IAM Credentials** : Ne pas utiliser les credentials root AWS
4. **Backups** : Tester les restaurations régulièrement
5. **Monitoring** : Configurer les alertes selon vos besoins
6. **Coûts** : Surveiller les coûts AWS avec Cost Explorer

## Prochaines Étapes

1. Déployer l'infrastructure avec `deploy-aws-production.sh`
2. Configurer le DNS Route53
3. Valider le certificat SSL
4. Configurer AWS dans Odoo
5. Installer les modules SaaS
6. Tester la création d'instances SaaS
7. Configurer les backups automatiques
8. Mettre en place le monitoring

## Maintenance

### Mises à jour Régulières
- **Système** : Automatique via user-data
- **Odoo** : Via l'interface ou code déployé
- **Terraform** : Via `terraform apply`

### Backups
- **Base de données** : Automatique quotidien (RDS)
- **Fichiers** : Via module S3 Backup
- **Rétention** : 7 jours (configurable)

### Monitoring
- **CloudWatch** : Logs et métriques automatiques
- **Health Checks** : ALB et Route53
- **Alertes** : Email/SNS configurable

