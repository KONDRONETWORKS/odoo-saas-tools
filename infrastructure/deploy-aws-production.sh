#!/bin/bash
# Script de déploiement complet pour AWS avec Terraform
# Usage: ./deploy-aws-production.sh

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variables
TERRAFORM_DIR="infrastructure/terraform"
TFVARS_FILE="$TERRAFORM_DIR/terraform.tfvars"

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 Déploiement Odoo SaaS Tools sur AWS${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Vérifications préalables
echo -e "${YELLOW}📋 Vérifications préalables...${NC}"

# Vérifier AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI n'est pas installé${NC}"
    echo "Installez-le avec: brew install awscli (macOS) ou pip install awscli"
    exit 1
fi

# Vérifier Terraform
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform n'est pas installé${NC}"
    echo "Installez-le avec: brew install terraform (macOS) ou téléchargez depuis https://terraform.io"
    exit 1
fi

# Vérifier les credentials AWS
echo "🔐 Vérification des credentials AWS..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials non configurés${NC}"
    echo "Configurez avec: aws configure"
    exit 1
fi

AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "eu-west-1")
echo -e "${GREEN}✅ AWS Account: $AWS_ACCOUNT${NC}"
echo -e "${GREEN}✅ Région: $AWS_REGION${NC}"

# Vérifier le fichier terraform.tfvars
if [ ! -f "$TFVARS_FILE" ]; then
    echo -e "${YELLOW}⚠️ Fichier terraform.tfvars non trouvé${NC}"
    echo "Création depuis terraform.tfvars.example..."
    if [ -f "$TERRAFORM_DIR/terraform.tfvars.example" ]; then
        cp "$TERRAFORM_DIR/terraform.tfvars.example" "$TFVARS_FILE"
        echo -e "${YELLOW}⚠️ Veuillez éditer $TFVARS_FILE avec vos valeurs avant de continuer${NC}"
        exit 1
    else
        echo -e "${RED}❌ Fichier terraform.tfvars.example non trouvé${NC}"
        exit 1
    fi
fi

# Vérifier les variables requises
echo "🔍 Vérification des variables..."
DOMAIN_NAME=$(grep -E "^domain_name" "$TFVARS_FILE" | cut -d'"' -f2 || echo "")
KEY_PAIR_NAME=$(grep -E "^key_pair_name" "$TFVARS_FILE" | cut -d'"' -f2 || echo "")

if [ -z "$DOMAIN_NAME" ] || [ "$DOMAIN_NAME" = "saas.votre-domaine.com" ]; then
    echo -e "${RED}❌ Veuillez configurer domain_name dans $TFVARS_FILE${NC}"
    exit 1
fi

if [ -z "$KEY_PAIR_NAME" ] || [ "$KEY_PAIR_NAME" = "votre-cle-ssh" ]; then
    echo -e "${RED}❌ Veuillez configurer key_pair_name dans $TFVARS_FILE${NC}"
    exit 1
fi

# Vérifier que la clé SSH existe
echo "🔑 Vérification de la clé SSH AWS..."
if ! aws ec2 describe-key-pairs --key-names "$KEY_PAIR_NAME" &> /dev/null; then
    echo -e "${YELLOW}⚠️ Clé SSH '$KEY_PAIR_NAME' non trouvée dans AWS${NC}"
    echo "Souhaitez-vous créer une nouvelle clé? (y/n)"
    read -r CREATE_KEY
    if [ "$CREATE_KEY" = "y" ]; then
        echo "Génération d'une nouvelle clé SSH..."
        aws ec2 create-key-pair --key-name "$KEY_PAIR_NAME" --query 'KeyMaterial' --output text > "$HOME/.ssh/$KEY_PAIR_NAME.pem"
        chmod 400 "$HOME/.ssh/$KEY_PAIR_NAME.pem"
        echo -e "${GREEN}✅ Clé créée: $HOME/.ssh/$KEY_PAIR_NAME.pem${NC}"
    else
        exit 1
    fi
fi

# Créer le bucket S3 pour Terraform state (si nécessaire)
echo "📦 Vérification du bucket S3 pour Terraform state..."
BUCKET_NAME="odoo-saas-terraform-state"
if ! aws s3 ls "s3://$BUCKET_NAME" &> /dev/null; then
    echo "Création du bucket S3..."
    aws s3 mb "s3://$BUCKET_NAME" --region "$AWS_REGION"
    aws s3api put-bucket-versioning \
        --bucket "$BUCKET_NAME" \
        --versioning-configuration Status=Enabled
    aws s3api put-bucket-encryption \
        --bucket "$BUCKET_NAME" \
        --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
    
    # Créer la table DynamoDB pour le locking
    echo "Création de la table DynamoDB pour Terraform locking..."
    aws dynamodb create-table \
        --table-name terraform-state-lock \
        --attribute-definitions AttributeName=LockID,AttributeType=S \
        --key-schema AttributeName=LockID,KeyType=HASH \
        --billing-mode PAY_PER_REQUEST \
        --region "$AWS_REGION" \
        2>/dev/null || echo "Table déjà existante"
    
    echo -e "${GREEN}✅ Bucket S3 créé${NC}"
else
    echo -e "${GREEN}✅ Bucket S3 existe déjà${NC}"
fi

# Initialiser Terraform
echo ""
echo -e "${BLUE}🔧 Initialisation de Terraform...${NC}"
cd "$TERRAFORM_DIR"
terraform init

# Planification
echo ""
echo -e "${BLUE}📋 Planification des changements...${NC}"
terraform plan -out=tfplan

# Confirmation
echo ""
echo -e "${YELLOW}⚠️ Êtes-vous sûr de vouloir créer/modifier l'infrastructure? (yes/no)${NC}"
read -r CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Annulation..."
    exit 0
fi

# Application
echo ""
echo -e "${BLUE}🚀 Déploiement de l'infrastructure...${NC}"
terraform apply tfplan

# Récupération des outputs
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Déploiement terminé!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""

terraform output -json > ../terraform-outputs.json

echo "📋 Informations importantes:"
terraform output configuration_summary

echo ""
echo -e "${YELLOW}📝 Prochaines étapes:${NC}"
echo "1. Configurez vos DNS pour pointer vers les name servers Route53 affichés ci-dessus"
echo "2. Validez le certificat SSL dans la console AWS ACM"
echo "3. Attendez que les instances EC2 soient prêtes (quelques minutes)"
echo "4. Configurez les credentials AWS dans Odoo:"
echo "   - AWS Access Key ID"
echo "   - AWS Secret Access Key"
echo "5. Installez les modules SaaS dans Odoo"
echo ""
echo -e "${BLUE}Pour voir les outputs complets:${NC}"
echo "cd $TERRAFORM_DIR && terraform output"
echo ""
echo -e "${BLUE}Pour détruire l'infrastructure:${NC}"
echo "cd $TERRAFORM_DIR && terraform destroy"

