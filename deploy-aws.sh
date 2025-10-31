#!/bin/bash
# Script de déploiement automatisé pour AWS
# Usage: ./deploy-aws.sh --region eu-west-1 --instance-type t3.xlarge

set -e

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables par défaut
REGION="eu-west-1"
INSTANCE_TYPE="t3.xlarge"
KEY_NAME=""
DOMAIN_NAME=""
EMAIL=""
AMI_ID=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --region)
            REGION="$2"
            shift 2
            ;;
        --instance-type)
            INSTANCE_TYPE="$2"
            shift 2
            ;;
        --key-name)
            KEY_NAME="$2"
            shift 2
            ;;
        --domain)
            DOMAIN_NAME="$2"
            shift 2
            ;;
        --email)
            EMAIL="$2"
            shift 2
            ;;
        --ami)
            AMI_ID="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Option inconnue: $1${NC}"
            exit 1
            ;;
    esac
done

# Vérifications
if [ -z "$KEY_NAME" ]; then
    echo -e "${RED}Erreur: --key-name est requis${NC}"
    exit 1
fi

if [ -z "$DOMAIN_NAME" ]; then
    echo -e "${YELLOW}Avertissement: --domain non fourni, vous devrez le configurer manuellement${NC}"
fi

# Obtenir AMI Ubuntu 22.04 si non fourni
if [ -z "$AMI_ID" ]; then
    echo "🔍 Recherche de l'AMI Ubuntu 22.04..."
    AMI_ID=$(aws ec2 describe-images \
        --region $REGION \
        --owners 099720109477 \
        --filters \
            "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
            "Name=state,Values=available" \
        --query "Images | sort_by(@, &CreationDate) | [-1].ImageId" \
        --output text)
    echo "✅ AMI trouvé: $AMI_ID"
fi

# Créer VPC et subnets (si nécessaire)
echo "🌐 Vérification de la configuration réseau..."
VPC_ID=$(aws ec2 describe-vpcs --region $REGION --query "Vpcs[0].VpcId" --output text)
echo "✅ VPC: $VPC_ID"

# Créer Security Group
echo "🔒 Création du Security Group..."
SG_ID=$(aws ec2 create-security-group \
    --region $REGION \
    --group-name odoo-saas-sg-$(date +%s) \
    --description "Security group for Odoo SaaS Tools" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

echo "✅ Security Group créé: $SG_ID"

# Ajouter règles au Security Group
echo "🔧 Configuration des règles du Security Group..."
aws ec2 authorize-security-group-ingress \
    --region $REGION \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --region $REGION \
    --group-id $SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --region $REGION \
    --group-id $SG_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Obtenir un subnet
SUBNET_ID=$(aws ec2 describe-subnets \
    --region $REGION \
    --filters "Name=vpc-id,Values=$VPC_ID" \
    --query "Subnets[0].SubnetId" \
    --output text)

echo "✅ Subnet: $SUBNET_ID"

# Créer l'instance EC2
echo "🚀 Création de l'instance EC2..."
INSTANCE_ID=$(aws ec2 run-instances \
    --region $REGION \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --subnet-id $SUBNET_ID \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100,"VolumeType":"gp3"}}]' \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=odoo-saas-production},{Key=Project,Value=OdooSaaS}]" \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ Instance créée: $INSTANCE_ID"

# Attendre que l'instance soit running
echo "⏳ Attente du démarrage de l'instance..."
aws ec2 wait instance-running \
    --region $REGION \
    --instance-ids $INSTANCE_ID

# Obtenir l'IP publique
PUBLIC_IP=$(aws ec2 describe-instances \
    --region $REGION \
    --instance-ids $INSTANCE_ID \
    --query "Reservations[0].Instances[0].PublicIpAddress" \
    --output text)

echo "✅ Instance démarrée. IP Publique: $PUBLIC_IP"

# Préparer le script de configuration
echo "📝 Préparation du script de configuration..."
cat > /tmp/setup-server.sh << 'SETUP_EOF'
#!/bin/bash
set -e

# Ce script sera exécuté sur le serveur
PROJECT_DIR="/opt/odoo-saas-tools"
# ... (reste du script de configuration)
SETUP_EOF

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Déploiement AWS terminé!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "📋 Informations importantes:"
echo "   Instance ID: $INSTANCE_ID"
echo "   IP Publique: $PUBLIC_IP"
echo "   Security Group: $SG_ID"
echo ""
echo "🔗 Connexion SSH:"
echo "   ssh -i ~/.ssh/${KEY_NAME}.pem ubuntu@${PUBLIC_IP}"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Connectez-vous au serveur via SSH"
echo "   2. Exécutez le script de configuration:"
echo "      wget https://raw.githubusercontent.com/KONDRONETWORKS/odoo-saas-tools/main/deploy.sh"
echo "      chmod +x deploy.sh"
echo "      sudo ./deploy.sh"
echo ""
echo "   3. Configurez Route53 pour le DNS (si domaine fourni)"
if [ ! -z "$DOMAIN_NAME" ]; then
    echo "   4. Configurez votre domaine: $DOMAIN_NAME -> $PUBLIC_IP"
fi
echo ""

