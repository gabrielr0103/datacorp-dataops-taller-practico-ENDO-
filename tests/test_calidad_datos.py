import pandas as pd

from src.calidad.validar_datos import validar


def datos_validos() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03"]),
            "tienda_mdm_id": ["T1", "T1", "T1"],
            "cuenta_mdm_id": ["C1", "C1", "C1"],
            "pais": ["CO", "CO", "CO"],
            "ventas": [100.0, 120.0, 90.0],
            "transacciones": [10, 12, 9],
            "clientes_activos": [50, 51, 51],
        }
    )


def test_datos_validos_no_tienen_errores():
    assert validar(datos_validos(), max_nulos_pct=10) == []


def test_detecta_exceso_de_nulos():
    datos = datos_validos()
    datos.loc[0, "ventas"] = None
    errores = validar(datos, max_nulos_pct=10)
    assert any(error.startswith("ventas:") for error in errores)


def test_detecta_ventas_negativas():
    datos = datos_validos()
    datos.loc[1, "ventas"] = -5.0
    assert "Hay ventas negativas" in validar(datos, max_nulos_pct=10)


def test_detecta_duplicados_por_fecha_y_tienda():
    datos = pd.concat([datos_validos(), datos_validos().head(1)], ignore_index=True)
    errores = validar(datos, max_nulos_pct=10)
    assert any("duplicadas" in error for error in errores)


def test_detecta_columnas_faltantes():
    datos = datos_validos().drop(columns=["clientes_activos"])
    errores = validar(datos, max_nulos_pct=10)
    assert errores and errores[0].startswith("Faltan columnas")
