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
  description = "Backend App name (Django)"
  type        = string
}

variable "backend_image" {
  description = "Docker image URL for the backend app"
  type        = string
}