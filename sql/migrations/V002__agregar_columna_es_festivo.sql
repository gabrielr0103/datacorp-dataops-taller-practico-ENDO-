-- Variable de festivos (cambio de ejemplo de la Actividad 1.2).
ALTER TABLE analitica.features_ventas
    ADD COLUMN IF NOT EXISTS es_festivo SMALLINT NOT NULL DEFAULT 0;
