output "bucket_datos" {
  description = "Bucket S3 de datos del entorno"
  value       = aws_s3_bucket.datos.bucket
}

output "rol_pipeline_arn" {
  description = "ARN del rol IAM del pipeline"
  value       = aws_iam_role.pipeline.arn
}

output "instancias_desarrollo" {
  description = "IDs de las estaciones EC2 de desarrollo (lista vacía fuera de dev)"
  value       = aws_instance.desarrollo[*].id
}

output "endpoint_base_datos" {
  description = "Endpoint de la base RDS (null en dev)"
  value       = var.crear_rds ? aws_db_instance.principal[0].endpoint : null
}
