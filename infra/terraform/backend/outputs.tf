output "backend_url" {
  description = "Public URL of the Chrona backend API"
  value       = azurerm_container_app.chrona_backend.latest_revision_fqdn
}