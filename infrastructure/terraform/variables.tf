# Variables Terraform pour Odoo SaaS Tools

variable "aws_region" {
  description = "Région AWS pour le déploiement"
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Nom du projet (utilisé pour nommer les ressources)"
  type        = string
  default     = "odoo-saas"
}

variable "domain_name" {
  description = "Nom de domaine principal (ex: saas.exemple.com)"
  type        = string
}

variable "environment" {
  description = "Environnement (production, staging, development)"
  type        = string
  default     = "production"
  
  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "L'environnement doit être: production, staging ou development."
  }
}

variable "instance_type" {
  description = "Type d'instance EC2 pour Odoo"
  type        = string
  default     = "t3.xlarge"
}

variable "db_instance_class" {
  description = "Classe d'instance RDS PostgreSQL"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Stockage alloué pour RDS en GB"
  type        = number
  default     = 100
  
  validation {
    condition     = var.db_allocated_storage >= 20 && var.db_allocated_storage <= 65536
    error_message = "Le stockage RDS doit être entre 20 et 65536 GB."
  }
}

variable "key_pair_name" {
  description = "Nom de la clé SSH AWS à utiliser"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR autorisé pour l'accès SSH (0.0.0.0/0 = tous, restreindre en production)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "min_instances" {
  description = "Nombre minimum d'instances dans l'Auto Scaling Group"
  type        = number
  default     = 2
  
  validation {
    condition     = var.min_instances >= 1
    error_message = "Le nombre minimum d'instances doit être au moins 1."
  }
}

variable "max_instances" {
  description = "Nombre maximum d'instances dans l'Auto Scaling Group"
  type        = number
  default     = 10
  
  validation {
    condition     = var.max_instances >= var.min_instances
    error_message = "Le nombre maximum d'instances doit être supérieur ou égal au minimum."
  }
}

variable "desired_capacity" {
  description = "Capacité désirée pour l'Auto Scaling Group"
  type        = number
  default     = 2
  
  validation {
    condition     = var.desired_capacity >= var.min_instances && var.desired_capacity <= var.max_instances
    error_message = "La capacité désirée doit être entre min et max."
  }
}

variable "enable_backup" {
  description = "Activer les backups automatiques RDS"
  type        = bool
  default     = true
}

variable "backup_retention_days" {
  description = "Nombre de jours de rétention pour les backups RDS"
  type        = number
  default     = 7
  
  validation {
    condition     = var.backup_retention_days >= 0 && var.backup_retention_days <= 35
    error_message = "La rétention des backups doit être entre 0 et 35 jours."
  }
}

variable "enable_multi_az" {
  description = "Activer Multi-AZ pour RDS (haute disponibilité)"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Rétention des logs CloudWatch en jours"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags additionnels à appliquer à toutes les ressources"
  type        = map(string)
  default     = {}
}

