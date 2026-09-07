terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "db_username" {
  description = "Administrator username for the Postgres server (never hardcode this)"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Administrator password for the Postgres server (never hardcode this)"
  type        = string
  sensitive   = true
}

variable "my_ip" {
  description = "Your current public IP address, to allow the firewall to let you connect"
  type        = string
}

resource "azurerm_resource_group" "chrysoptera" {
  name     = "chrysoptera-rg"
  location = "Switzerland North"
}

resource "azurerm_postgresql_flexible_server" "chrysoptera_postgres" {
  name                   = "chrysoptera-db-server"
  resource_group_name    = azurerm_resource_group.chrysoptera.name
  location               = azurerm_resource_group.chrysoptera.location
  version                = "15"
  administrator_login    = var.db_username
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  backup_retention_days  = 7

  tags = {
    Project     = "Chrysoptera"
    Environment = "staging"
  }
}

resource "azurerm_postgresql_flexible_server_database" "chrysoptera_db" {
  name      = "chrysoptera"
  server_id = azurerm_postgresql_flexible_server.chrysoptera_postgres.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_my_ip" {
  name             = "allow-my-ip"
  server_id        = azurerm_postgresql_flexible_server.chrysoptera_postgres.id
  start_ip_address = var.my_ip
  end_ip_address   = var.my_ip
}

output "db_host" {
  description = "Connection hostname for the Postgres server"
  value       = azurerm_postgresql_flexible_server.chrysoptera_postgres.fqdn
}
