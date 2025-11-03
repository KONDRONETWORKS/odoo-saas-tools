#!/bin/bash
# Script pour configurer les credentials AWS dans Odoo après déploiement
# Usage: ./configure-odoo-aws.sh

set -e

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}⚙️ Configuration AWS dans Odoo${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Vérifier Terraform outputs
if [ ! -f "infrastructure/terraform-outputs.json" ]; then
    echo -e "${YELLOW}⚠️ Fichier terraform-outputs.json non trouvé${NC}"
    echo "Récupération des outputs Terraform..."
    cd infrastructure/terraform
    terraform output -json > ../terraform-outputs.json
    cd ../..
fi

# Lire les outputs
BACKUPS_BUCKET=$(jq -r '.s3_backups_bucket.value' infrastructure/terraform-outputs.json)
FILESTORE_BUCKET=$(jq -r '.s3_filestore_bucket.value' infrastructure/terraform-outputs.json)
ROUTE53_ZONE_ID=$(jq -r '.route53_zone_id.value' infrastructure/terraform-outputs.json)

echo -e "${GREEN}✅ Informations récupérées depuis Terraform${NC}"
echo "  - Backups Bucket: $BACKUPS_BUCKET"
echo "  - Filestore Bucket: $FILESTORE_BUCKET"
echo "  - Route53 Zone ID: $ROUTE53_ZONE_ID"
echo ""

# Demander les credentials AWS
echo -e "${YELLOW}📝 Entrez les credentials AWS pour Odoo:${NC}"
echo "  (Créez un utilisateur IAM avec permissions S3 et Route53)"
read -p "AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -sp "AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo ""

# Générer un script Python pour configurer Odoo
cat > /tmp/configure_odoo_aws.py << PYTHON_EOF
import xmlrpc.client
import sys

# Configuration
ODOO_URL = "http://localhost:8069"  # Modifiez si nécessaire
ODOO_DB = "odoo"  # Modifiez si nécessaire
ODOO_USER = "admin"  # Modifiez si nécessaire
ODOO_PASSWORD = "admin"  # ⚠️ Changez en production

AWS_ACCESS_KEY_ID = "$AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "$AWS_SECRET_ACCESS_KEY"
BACKUPS_BUCKET = "$BACKUPS_BUCKET"
FILESTORE_BUCKET = "$FILESTORE_BUCKET"
ROUTE53_ZONE_ID = "$ROUTE53_ZONE_ID"

# Connexion
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})

if not uid:
    print("❌ Erreur d'authentification")
    sys.exit(1)

models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

# Configurer AWS
print("🔧 Configuration AWS...")

# Chercher ou créer la configuration AWS
config_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'saas.sysadmin.aws.config',
    'search',
    [[('name', '=', 'default')]]
)

if config_ids:
    config_id = config_ids[0]
    models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'saas.sysadmin.aws.config',
        'write',
        [[config_id], {
            'aws_access_key_id': AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
            'aws_region': 'eu-west-1',
        }]
    )
    print(f"✅ Configuration AWS mise à jour (ID: {config_id})")
else:
    config_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'saas.sysadmin.aws.config',
        'create',
        [{
            'name': 'default',
            'aws_access_key_id': AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
            'aws_region': 'eu-west-1',
        }]
    )
    print(f"✅ Configuration AWS créée (ID: {config_id})")

# Configurer S3 Backup
print("📦 Configuration S3 Backup...")
backup_config_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'saas.server.backup.s3.config',
    'search',
    [[('name', '=', 'default')]]
)

if backup_config_ids:
    backup_config_id = backup_config_ids[0]
    models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'saas.server.backup.s3.config',
        'write',
        [[backup_config_id], {
            's3_bucket': BACKUPS_BUCKET,
        }]
    )
    print(f"✅ Configuration S3 Backup mise à jour")
else:
    print("⚠️ Module saas_server_backup_s3 non installé ou non trouvé")

# Configurer Route53
print("🌐 Configuration Route53...")
route53_config_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'saas.sysadmin.route53.config',
    'search',
    [[('name', '=', 'default')]]
)

if route53_config_ids:
    route53_config_id = route53_config_ids[0]
    models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'saas.sysadmin.route53.config',
        'write',
        [[route53_config_id], {
            'route53_zone_id': ROUTE53_ZONE_ID,
        }]
    )
    print(f"✅ Configuration Route53 mise à jour")
else:
    print("⚠️ Module saas_sysadmin_aws_route53 non installé ou non trouvé")

print("✅ Configuration terminée!")
PYTHON_EOF

echo ""
echo -e "${YELLOW}⚠️ Ce script nécessite un accès XML-RPC à Odoo${NC}"
echo "Pour l'exécuter, vous devez être sur le serveur ou avoir configuré l'accès XML-RPC"
echo ""
echo "Pour exécuter manuellement:"
echo "  1. Connectez-vous à Odoo via l'interface web"
echo "  2. Allez dans Système > SaaS > Configuration AWS"
echo "  3. Entrez les credentials et les buckets S3"
echo ""
echo "Informations à utiliser:"
echo "  - AWS Access Key ID: $AWS_ACCESS_KEY_ID"
echo "  - AWS Secret Access Key: [masqué]"
echo "  - Backups Bucket: $BACKUPS_BUCKET"
echo "  - Filestore Bucket: $FILESTORE_BUCKET"
echo "  - Route53 Zone ID: $ROUTE53_ZONE_ID"

