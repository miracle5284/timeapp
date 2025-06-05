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

variable "app_name" {
  description = "App name"
  type        = string
}

variable "backend_image" {
  description = "Docker image URL for the backend app"
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

variable "min_replicas" {
    description = "Minimum number of replicas for the container app"
    type        = number
    default     = 0
}
#
# variable "subscription_id" {
#   description = "AZURE Subscription ID"
#   type        = string
# }
#
# variable "tenant_id" {
#   description = "Azure Tenant ID"
#   type        = string
# }
#
# variable "client_id" {
#   description = "Azure Client ID"
#   type        = string
# }
#
# variable "client_secret" {
#   description = "Azure client Secret"
#   type        = string
#   sensitive   = true
# }