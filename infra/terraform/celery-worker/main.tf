data "azurerm_container_app_environment" "chrona_env" {
  name                = var.container_app_env_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_app" "chrona_celery_worker" {
  name                         = var.worker_name
  container_app_environment_id = data.azurerm_container_app_environment.chrona_env.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = var.worker_name
      image  = var.app_image
      cpu    = 0.25
      memory = "0.5Gi"
      command = ["poetry", "run", "celery", "-A", "config", "worker", "--loglevel=info"]
    }

    scale {
      max_replicas = var.max_replicas
      min_replicas = var.min_replicas

      rule {
        name = "celery-scale"
        type = "redis"

        metadata = {
          address       = var.redis_url
          listName      = var.list_name
          listLength    = var.list_length
          databaseIndex = "0"
        }

        auth {
          secretRef        = "redis-password"
          triggerParameter = "password"
        }
      }
    }
  }

  ingress {
    external_enabled = false
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

  tags = {
    service     = "celery"
    environment = var.environment
    project     = "chrona"
    prod        = "yes"
  }
}
