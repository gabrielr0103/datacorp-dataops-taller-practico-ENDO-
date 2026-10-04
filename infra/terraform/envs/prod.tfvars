# PROD: base Multi-AZ con protección contra borrado y respaldos de dos semanas.
entorno                = "prod"
crear_rds              = true
clase_rds              = "db.r6g.large"
almacenamiento_rds_gb  = 500
rds_multi_az           = true
dias_retencion_backups = 14
proteccion_borrado     = true
