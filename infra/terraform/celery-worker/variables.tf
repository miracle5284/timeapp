variable "resource_group_name" {
  description = "Azure Resource Group where Chrona services will be deployed"
  type        = string
}

variable "location" {
  description = "Azure region (e.g., eastus)"
  type        = string
}

variable "container_app_env_name" {
  description = "Azure Container App Environment name"
  type        = string
}

variable "worker_name" {
  description = "Name for the Celery worker container app"
  type        = string
}

variable "app_image" {
  description = "Docker image URL shared between backend and Celery worker"
  type        = string
}

variable "registry_password" {
  description = "GitHub PAT for GHCR (read packages)"
  type        = string
  sensitive   = true
}

variable "registry_username" {
  description = "GitHub Username for GHCR"
  type        = string
}

variable "redis_url" {
  description = "Connection string for Redis (used by Celery broker)"
  type        = string
}

variable "list_name" {
  description = "Redis list name Celery uses (default: 'celery')"
  type        = string
  default     = "celery"
}

variable "list_length" {
  description = "Threshold Redis queue length to trigger scale-up"
  type        = number
  default     = 1
}

variable "min_replicas" {
  description = "Minimum number of replicas for the container app"
  type        = number
  default     = 0
}

variable "max_replicas" {
  description = "Maximum number of replicas for the container app"
  type        = number
  default     = 1
}

variable "environment" {
  description = "Deployment environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}
