resource "azurerm_container_app_environment" "chrona_env" {
  name                = var.container_app_env_name
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_app" "chrona_backend" {
  name                         = var.app_name
  container_app_environment_id = azurerm_container_app_environment.chrona_env.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = var.app_name
      image  = var.backend_image
      cpu    = 0.5
      memory = "1Gi"

    }

    max_replicas = 3
    min_replicas = var.min_replicas

  }

  secret {
    name  = "ghcr-password"
    value = var.registry_password
  }

  registry {
    server               = "ghcr.io"
    username             = var.registry_username
    password_secret_name = "ghcr-password"
  }

  ingress {
    external_enabled           = true
    target_port                = 8000
    allow_insecure_connections = false

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
}