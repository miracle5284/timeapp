output "logging_service_url" {
  description = "Public URL of the Logging Service"
  value       = azurerm_container_app.logging_service.latest_revision_fqdn
}