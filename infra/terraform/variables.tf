variable "region" {
  description = "Región de AWS donde se crean los recursos"
  type        = string
  default     = "us-east-1"
}

variable "entorno" {
  description = "Entorno a desplegar: dev, qa o prod"
  type        = string

  validation {
    condition     = contains(["dev", "qa", "prod"], var.entorno)
    error_message = "El entorno debe ser dev, qa o prod."
  }
}

# ------------------------------------------------------------------ EC2

variable "cantidad_instancias_dev" {
  description = "Número de estaciones EC2 de desarrollo, una por científico de datos"
  type        = number
  default     = 0

  validation {
    condition     = var.entorno == "dev" || var.cantidad_instancias_dev == 0
    error_message = "Las instancias de desarrollo solo se crean en el entorno dev."
  }
}

variable "tipo_instancia_dev" {
  description = "Tipo de instancia EC2 de las estaciones de desarrollo"
  type        = string
  default     = "t3.medium"
}

# ------------------------------------------------------------------ RDS

variable "crear_rds" {
  description = "Si el entorno tiene base de datos RDS (QA y PROD)"
  type        = bool
  default     = false
}

variable "clase_rds" {
  description = "Clase de la instancia RDS"
  type        = string
  default     = "db.t4g.medium"
}

variable "almacenamiento_rds_gb" {
  description = "Almacenamiento de la base de datos en GB"
  type        = number
  default     = 50
}

variable "rds_multi_az" {
  description = "Si la base tiene una réplica en otra zona de disponibilidad"
  type        = bool
  default     = false

  validation {
    condition     = var.entorno != "prod" || var.rds_multi_az
    error_message = "En prod la base de datos tiene que ser Multi-AZ."
  }
}

variable "dias_retencion_backups" {
  description = "Días que se guardan los respaldos automáticos de RDS"
  type        = number
  default     = 1

  validation {
    condition     = var.dias_retencion_backups >= 1 && var.dias_retencion_backups <= 35
    error_message = "La retención de respaldos debe estar entre 1 y 35 días."
  }
}

variable "proteccion_borrado" {
  description = "Si la base de datos queda protegida contra borrado"
  type        = bool
  default     = false

  validation {
    condition     = var.entorno != "prod" || var.proteccion_borrado
    error_message = "En prod la base de datos tiene que tener protección contra borrado."
  }
}
