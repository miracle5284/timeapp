data "azurerm_container_app_environment" "chrona_env" {
  name                = var.container_app_env_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_app" "logging_service" {
  name                         = var.app_name
  container_app_environment_id = data.azurerm_container_app_environment.chrona_env.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      cpu    = 0.25
      image  = var.logging_service_image
      memory = "0.5Gi"
      name   = var.app_name
    }

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
    target_port                = 7000
    transport                  = "auto"
    allow_insecure_connections = false

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
}