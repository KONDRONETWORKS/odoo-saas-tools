#!/bin/bash
# Script de déploiement AWS pour Odoo SaaS Tools
# Usage: ./scripts/deploy-aws.sh [staging|production]

set -e

ENVIRONMENT=${1:-staging}
AWS_REGION=${AWS_REGION:-us-east-1}
PROJECT_NAME="odoo-saas-tools"

echo "🚀 Déploiement Odoo SaaS Tools sur AWS - Environnement: $ENVIRONMENT"
echo "================================================================"

# Vérifier les prérequis
command -v aws >/dev/null 2>&1 || { echo "❌ AWS CLI non installé. Installez-le: brew install awscli"; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "❌ Terraform non installé. Installez-le: brew install terraform"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker non installé"; exit 1; }

# Vérifier les credentials AWS
aws sts get-caller-identity >/dev/null 2>&1 || { echo "❌ AWS credentials non configurés. Exécutez: aws configure"; exit 1; }

echo ""
echo "✅ Prérequis validés"
echo ""

# Variables d'environnement
export TF_VAR_environment=$ENVIRONMENT
export TF_VAR_project_name=$PROJECT_NAME
export TF_VAR_aws_region=$AWS_REGION

# Étape 1: Build et Push Docker Image vers ECR
echo "📦 Étape 1: Build et Push Docker Image"
echo "--------------------------------------"

ECR_REPOSITORY="${PROJECT_NAME}-${ENVIRONMENT}"
ECR_REGISTRY=$(aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text 2>/dev/null || echo "")

if [ -z "$ECR_REGISTRY" ]; then
    echo "📝 Création du repository ECR..."
    aws ecr create-repository \
        --repository-name $ECR_REPOSITORY \
        --region $AWS_REGION \
        --image-scanning-configuration scanOnPush=true \
        --encryption-configuration encryptionType=AES256
    
    ECR_REGISTRY=$(aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text)
fi

echo "🔐 Login ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

echo "🏗️  Build Docker image..."
docker build -f config/Dockerfile -t $ECR_REPOSITORY:latest .

echo "📤 Push vers ECR..."
docker tag $ECR_REPOSITORY:latest $ECR_REGISTRY:latest
docker push $ECR_REGISTRY:latest

IMAGE_URI="$ECR_REGISTRY:latest"
echo "✅ Image disponible: $IMAGE_URI"
echo ""

# Étape 2: Déploiement Infrastructure avec Terraform
echo "🏗️  Étape 2: Déploiement Infrastructure Terraform"
echo "---------------------------------------------------"

cd infrastructure/terraform

echo "🔧 Initialisation Terraform..."
terraform init

echo "📋 Plan Terraform..."
terraform plan \
    -var="environment=$ENVIRONMENT" \
    -var="project_name=$PROJECT_NAME" \
    -var="aws_region=$AWS_REGION" \
    -var="docker_image=$IMAGE_URI" \
    -out=tfplan

echo "🚀 Application Terraform..."
read -p "Continuer avec le déploiement? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    terraform apply tfplan
    echo "✅ Infrastructure déployée"
else
    echo "❌ Déploiement annulé"
    exit 1
fi

# Étape 3: Déploiement Application
echo ""
echo "🚀 Étape 3: Déploiement Application"
echo "----------------------------------"

# Récupérer les outputs Terraform
CLUSTER_NAME=$(terraform output -raw ecs_cluster_name 2>/dev/null || echo "")
SERVICE_NAME=$(terraform output -raw ecs_service_name 2>/dev/null || echo "")

if [ ! -z "$CLUSTER_NAME" ] && [ ! -z "$SERVICE_NAME" ]; then
    echo "🔄 Mise à jour du service ECS..."
    aws ecs update-service \
        --cluster $CLUSTER_NAME \
        --service $SERVICE_NAME \
        --force-new-deployment \
        --region $AWS_REGION
    
    echo "⏳ Attente de la stabilisation du service..."
    aws ecs wait services-stable \
        --cluster $CLUSTER_NAME \
        --services $SERVICE_NAME \
        --region $AWS_REGION
    
    echo "✅ Service déployé"
else
    echo "⚠️  Service ECS non trouvé. Déploiement manuel requis."
fi

# Étape 4: Health Check
echo ""
echo "🏥 Étape 4: Health Check"
echo "------------------------"

APP_URL=$(terraform output -raw app_url 2>/dev/null || echo "")

if [ ! -z "$APP_URL" ]; then
    echo "🔍 Vérification de santé: $APP_URL"
    sleep 30
    
    for i in {1..10}; do
        if curl -f "$APP_URL/web/health" >/dev/null 2>&1; then
            echo "✅ Application accessible et fonctionnelle"
            break
        else
            echo "⏳ Tentative $i/10..."
            sleep 10
        fi
    done
else
    echo "⚠️  URL de l'application non disponible"
fi

echo ""
echo "🎉 Déploiement terminé!"
echo "================================================================"
echo "Environnement: $ENVIRONMENT"
echo "Région: $AWS_REGION"
echo "Image: $IMAGE_URI"
if [ ! -z "$APP_URL" ]; then
    echo "URL: $APP_URL"
fi
echo ""

cd ../..

