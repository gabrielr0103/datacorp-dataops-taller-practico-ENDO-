-- Ventas diarias por tienda para el modelo de predicción de ventas.
-- Usa los identificadores del hub MDM (tienda_mdm_id), no los códigos de cada cadena,
-- y toma los clientes activos según la versión de la definición indicada en config/.
SELECT
    v.fecha,
    t.tienda_mdm_id,
    t.cuenta_mdm_id,
    t.pais,
    SUM(v.valor_total)          AS ventas,
    COUNT(DISTINCT v.ticket_id) AS transacciones,
    MAX(ca.clientes_activos)    AS clientes_activos
FROM ventas.transacciones AS v
JOIN mdm.tienda_xref AS x
  ON x.fuente = v.fuente
 AND x.codigo_origen = v.codigo_tienda
JOIN mdm.tienda AS t
  ON t.tienda_mdm_id = x.tienda_mdm_id
LEFT JOIN mdm.clientes_activos_por_tienda AS ca
  ON ca.tienda_mdm_id = t.tienda_mdm_id
 AND ca.fecha = v.fecha
 AND ca.version_definicion = %(version_cliente_activo)s
WHERE v.fecha BETWEEN %(inicio)s AND %(fin)s
  AND v.estado = 'valida'
GROUP BY v.fecha, t.tienda_mdm_id, t.cuenta_mdm_id, t.pais
ORDER BY v.fecha, t.tienda_mdm_id;
