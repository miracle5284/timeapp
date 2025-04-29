terraform {
    required_version = ">= 1.11.4"

    required_providers {
        azurerm ={
            source = "hashicorp/azurerm"
            version = "~> 3.90"
        }
    }
}

provider "azurerm" {
    features {}
}