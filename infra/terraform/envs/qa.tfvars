# QA / staging: misma arquitectura que PROD en tamaño reducido y bucket datacorp-staging.
entorno                = "qa"
crear_rds              = true
clase_rds              = "db.t4g.medium"
almacenamiento_rds_gb  = 100
rds_multi_az           = false
dias_retencion_backups = 3
proteccion_borrado     = false
