output "ecs_cluster_name" {
  description = "Nom du cluster ECS"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Nom du service ECS"
  value       = aws_ecs_service.main.name
}

output "app_url" {
  description = "URL de l'application"
  value       = "https://${aws_lb.main.dns_name}"
}

output "rds_endpoint" {
  description = "Endpoint RDS PostgreSQL"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "ecr_repository_url" {
  description = "URL du repository ECR"
  value       = aws_ecr_repository.main.repository_url
}

output "s3_bucket_name" {
  description = "Nom du bucket S3 pour les backups"
  value       = aws_s3_bucket.backups.id
}
