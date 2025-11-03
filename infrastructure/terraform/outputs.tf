# Outputs Terraform pour Odoo SaaS Tools

output "vpc_id" {
  description = "ID du VPC créé"
  value       = aws_vpc.main.id
}

output "alb_dns_name" {
  description = "DNS name de l'Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_arn" {
  description = "ARN de l'Application Load Balancer"
  value       = aws_lb.main.arn
}

output "rds_endpoint" {
  description = "Endpoint RDS PostgreSQL"
  value       = aws_db_instance.main.address
  sensitive   = true
}

output "rds_port" {
  description = "Port RDS PostgreSQL"
  value       = aws_db_instance.main.port
}

output "rds_database_name" {
  description = "Nom de la base de données RDS"
  value       = aws_db_instance.main.db_name
}

output "rds_username" {
  description = "Nom d'utilisateur RDS"
  value       = aws_db_instance.main.username
  sensitive   = true
}

output "db_password" {
  description = "Mot de passe RDS (généré aléatoirement)"
  value       = random_password.db_password.result
  sensitive   = true
}

output "s3_backups_bucket" {
  description = "Nom du bucket S3 pour les backups"
  value       = aws_s3_bucket.backups.id
}

output "s3_backups_bucket_arn" {
  description = "ARN du bucket S3 pour les backups"
  value       = aws_s3_bucket.backups.arn
}

output "s3_filestore_bucket" {
  description = "Nom du bucket S3 pour le filestore"
  value       = aws_s3_bucket.filestore.id
}

output "s3_filestore_bucket_arn" {
  description = "ARN du bucket S3 pour le filestore"
  value       = aws_s3_bucket.filestore.arn
}

output "route53_zone_id" {
  description = "ID de la zone Route53"
  value       = aws_route53_zone.main.zone_id
}

output "route53_name_servers" {
  description = "Name servers Route53 pour configuration DNS"
  value       = aws_route53_zone.main.name_servers
}

output "certificate_arn" {
  description = "ARN du certificat SSL ACM"
  value       = aws_acm_certificate.main.arn
}

output "security_group_alb_id" {
  description = "ID du Security Group pour l'ALB"
  value       = aws_security_group.alb.id
}

output "security_group_ec2_id" {
  description = "ID du Security Group pour les instances EC2"
  value       = aws_security_group.ec2.id
}

output "security_group_rds_id" {
  description = "ID du Security Group pour RDS"
  value       = aws_security_group.rds.id
}

output "autoscaling_group_name" {
  description = "Nom du groupe Auto Scaling"
  value       = aws_autoscaling_group.odoo.name
}

output "target_group_arn" {
  description = "ARN du Target Group"
  value       = aws_lb_target_group.odoo.arn
}

output "iam_role_ec2_arn" {
  description = "ARN du rôle IAM pour EC2"
  value       = aws_iam_role.ec2.arn
}

output "cloudwatch_log_group" {
  description = "Nom du groupe de logs CloudWatch"
  value       = aws_cloudwatch_log_group.odoo.name
}

# Informations de connexion
output "ssh_connection_command" {
  description = "Commande SSH pour se connecter à une instance"
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ubuntu@<INSTANCE_IP>"
}

output "application_url" {
  description = "URL de l'application"
  value       = "https://${var.domain_name}"
}

output "configuration_summary" {
  description = "Résumé de la configuration"
  value = <<-EOT
    ============================================
    Infrastructure Odoo SaaS Tools déployée
    ============================================
    
    Application URL: https://${var.domain_name}
    ALB DNS: ${aws_lb.main.dns_name}
    
    RDS Endpoint: ${aws_db_instance.main.address}
    Database: ${aws_db_instance.main.db_name}
    Username: ${aws_db_instance.main.username}
    
    S3 Backups: ${aws_s3_bucket.backups.id}
    S3 Filestore: ${aws_s3_bucket.filestore.id}
    
    Route53 Zone ID: ${aws_route53_zone.main.zone_id}
    Name Servers: ${join(", ", aws_route53_zone.main.name_servers)}
    
    ⚠️ IMPORTANT: Sauvegardez le mot de passe RDS de manière sécurisée!
    Le mot de passe est disponible dans les outputs Terraform (sensitive).
    
    Prochaines étapes:
    1. Configurez vos DNS pour pointer vers les name servers Route53
    2. Validez le certificat SSL dans ACM
    3. Configurez les credentials AWS dans Odoo
    4. Installez les modules SaaS dans Odoo
    ============================================
  EOT
}

