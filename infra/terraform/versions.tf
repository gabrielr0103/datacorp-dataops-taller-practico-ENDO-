# Versiones de Terraform y del proveedor de AWS, y dónde se guarda el estado.
# Los recursos (S3, EC2, RDS e IAM) se definen en la Actividad 4.

terraform {
  required_version = ">= 1.11.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # El estado se guarda en S3, nunca en el repositorio.
  # Cada entorno usa su propio workspace (dev, qa, prod).
  backend "s3" {
    bucket       = "datacorp-terraform-state"
    key          = "dataops/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      proyecto       = "datacorp-dataops"
      entorno        = var.entorno
      gestionado_por = "terraform"
    }
  }
}
