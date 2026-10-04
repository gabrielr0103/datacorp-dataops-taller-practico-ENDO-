-- Tabla donde el pipeline guarda las variables del modelo de ventas.
CREATE SCHEMA IF NOT EXISTS analitica;

CREATE TABLE IF NOT EXISTS analitica.features_ventas (
    fecha            DATE        NOT NULL,
    tienda_mdm_id    VARCHAR(36) NOT NULL,
    ventas           NUMERIC(14, 2),
    ventas_lag_7     NUMERIC(14, 2),
    ventas_media_28  NUMERIC(14, 2),
    clientes_activos INTEGER,
    dia_semana       SMALLINT,
    mes              SMALLINT,
    actualizado_en   TIMESTAMP   NOT NULL DEFAULT now(),
    PRIMARY KEY (fecha, tienda_mdm_id)
);
