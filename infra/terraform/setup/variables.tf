variable "resource_group_name" {
  description = "Name of the existing Azure resource group"
  type        = string
}

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "eastus"
}

variable "storage_account_name" {
  description = "Name of the Azure Storage account"
  type        = string
}

variable "container_name" {
  description = "Name of the storage container"
  type        = string
}

variable "github_owner" {
  description = "GitHub account/org that owns the repo"
  type        = string
}

variable "subscription_id" {
  type        = string
  description = "Subscription that is subscription will be created"
}
variable "client_id" {
  type        = string
  description = "Client ID for Service Principal"
}
variable "client_secret" {
  type        = string
  description = "Client Secret for Service Principal"
}
variable "tenant_id" {
  type        = string
  description = "Tenant ID for Service Principal"
}