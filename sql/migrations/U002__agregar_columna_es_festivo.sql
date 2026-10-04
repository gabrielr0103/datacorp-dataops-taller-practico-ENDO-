-- Reversa de V002. Se usa si hay que hacer rollback de la versión que agregó los festivos.
ALTER TABLE analitica.features_ventas
    DROP COLUMN IF EXISTS es_festivo;
