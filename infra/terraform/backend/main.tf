resource "azurerm_container_app_environment" "chrona_env" {
  name                = var.container_app_env_name
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_app" "chrona_backend" {
  name                         = var.app_name
  container_app_environment_id = azurerm_container_app_environment.chrona_env
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = var.app_name
      image  = var.backend_image
      cpu    = 0.5
      memory = "1Gi"
      ports {
        external    = true
        target_port = 8000
      }

    }

    scale {
      max_replicas = 3
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
  }
}