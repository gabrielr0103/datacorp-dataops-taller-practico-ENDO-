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
