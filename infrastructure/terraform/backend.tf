# Backend S3 pour Terraform State
# À créer avant d'exécuter terraform init

# Pour créer le bucket et la table DynamoDB:
# aws s3 mb s3://odoo-saas-terraform-state --region eu-west-1
# aws s3api put-bucket-versioning --bucket odoo-saas-terraform-state --versioning-configuration Status=Enabled
# aws s3api put-bucket-encryption --bucket odoo-saas-terraform-state --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
# aws dynamodb create-table --table-name terraform-state-lock --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region eu-west-1

# Note: Le backend est configuré dans providers.tf pour éviter la duplication

