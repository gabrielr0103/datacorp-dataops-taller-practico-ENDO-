# Recursos de AWS de DataCorp Analytics (Actividad 4.1).
#
# El mismo código crea los tres entornos. Lo que cambia entre DEV, QA y PROD
# está en envs/<entorno>.tfvars, y cada entorno tiene su propio workspace
# y su propio estado en S3 (ver versions.tf).

locals {
  prefijo = "datacorp-${var.entorno}"

  # Nombres de bucket de la Actividad 1. El de QA es el bucket de staging.
  nombres_bucket = {
    dev  = "datacorp-dev"
    qa   = "datacorp-staging"
    prod = "datacorp-prod"
  }
}

# ------------------------------------------------------------------
# Red: se usa la VPC por defecto de la cuenta para simplificar el taller.
# ------------------------------------------------------------------

data "aws_vpc" "principal" {
  default = true
}

data "aws_subnets" "principal" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.principal.id]
  }
}

# ------------------------------------------------------------------
# S3: bucket de datos del entorno (en QA es datacorp-staging)
# ------------------------------------------------------------------

resource "aws_s3_bucket" "datos" {
  bucket = local.nombres_bucket[var.entorno]
}

resource "aws_s3_bucket_versioning" "datos" {
  bucket = aws_s3_bucket.datos.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "datos" {
  bucket = aws_s3_bucket.datos.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "datos" {
  bucket = aws_s3_bucket.datos.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ------------------------------------------------------------------
# IAM: rol del pipeline con acceso solo al bucket de su entorno
# ------------------------------------------------------------------

data "aws_iam_policy_document" "confianza_ec2" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "pipeline" {
  name               = "${local.prefijo}-pipeline"
  description        = "Rol del pipeline de datos en ${var.entorno}. Solo accede al bucket de su entorno."
  assume_role_policy = data.aws_iam_policy_document.confianza_ec2.json
}

data "aws_iam_policy_document" "acceso_bucket" {
  statement {
    sid       = "ListarSoloSuBucket"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.datos.arn]
  }

  statement {
    sid       = "LeerYEscribirObjetos"
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.datos.arn}/*"]
  }

  # Aunque otra política llegara a permitirlo, el pipeline nunca puede borrar datos.
  statement {
    sid       = "SinBorradoDeDatos"
    effect    = "Deny"
    actions   = ["s3:DeleteObject", "s3:DeleteObjectVersion", "s3:DeleteBucket"]
    resources = [aws_s3_bucket.datos.arn, "${aws_s3_bucket.datos.arn}/*"]
  }
}

resource "aws_iam_role_policy" "acceso_bucket" {
  name   = "acceso-bucket-${var.entorno}"
  role   = aws_iam_role.pipeline.id
  policy = data.aws_iam_policy_document.acceso_bucket.json
}

resource "aws_iam_instance_profile" "pipeline" {
  name = "${local.prefijo}-pipeline"
  role = aws_iam_role.pipeline.name
}

# ------------------------------------------------------------------
# EC2: estaciones de trabajo de DEV (cantidad = 0 en QA y PROD)
# ------------------------------------------------------------------

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_instance" "desarrollo" {
  count = var.cantidad_instancias_dev

  ami                  = data.aws_ami.amazon_linux.id
  instance_type        = var.tipo_instancia_dev
  subnet_id            = data.aws_subnets.principal.ids[0]
  iam_instance_profile = aws_iam_instance_profile.pipeline.name

  metadata_options {
    http_tokens = "required"
  }

  root_block_device {
    volume_size = 30
    encrypted   = true
  }

  tags = {
    Name           = "${local.prefijo}-estacion-${count.index + 1}"
    apagado_diario = "true" # lo usa el programador de apagado fuera del horario laboral
  }
}

# ------------------------------------------------------------------
# RDS: base PostgreSQL de QA y PROD (en PROD es Multi-AZ)
# ------------------------------------------------------------------

resource "aws_db_subnet_group" "principal" {
  count = var.crear_rds ? 1 : 0

  name       = "${local.prefijo}-db"
  subnet_ids = data.aws_subnets.principal.ids
}

resource "aws_security_group" "base_datos" {
  count = var.crear_rds ? 1 : 0

  name        = "${local.prefijo}-db"
  description = "PostgreSQL accesible solo desde la VPC"
  vpc_id      = data.aws_vpc.principal.id

  ingress {
    description = "PostgreSQL desde la VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.principal.cidr_block]
  }
}

resource "aws_db_instance" "principal" {
  count = var.crear_rds ? 1 : 0

  identifier     = "${local.prefijo}-ventas"
  engine         = "postgres"
  engine_version = "16"
  instance_class = var.clase_rds
  db_name        = "ventas"
  username       = "datacorp_admin"

  # AWS genera la contraseña y la guarda en Secrets Manager. No aparece en el código.
  manage_master_user_password = true

  allocated_storage      = var.almacenamiento_rds_gb
  storage_type           = "gp3"
  storage_encrypted      = true
  multi_az               = var.rds_multi_az
  db_subnet_group_name   = aws_db_subnet_group.principal[0].name
  vpc_security_group_ids = [aws_security_group.base_datos[0].id]
  publicly_accessible    = false

  backup_retention_period   = var.dias_retencion_backups
  deletion_protection       = var.proteccion_borrado
  skip_final_snapshot       = !var.proteccion_borrado
  final_snapshot_identifier = var.proteccion_borrado ? "${local.prefijo}-ventas-final" : null
}
