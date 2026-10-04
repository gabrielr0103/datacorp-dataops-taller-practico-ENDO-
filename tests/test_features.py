import pandas as pd
import pytest

from src.features.construir_features import construir_features


def ventas_de_prueba(pais: str) -> pd.DataFrame:
    fechas = pd.date_range("2026-01-01", periods=10, freq="D")
    return pd.DataFrame(
        {
            "fecha": fechas,
            "tienda_mdm_id": ["T1"] * 10,
            "pais": [pais] * 10,
            "ventas": [float(100 + i) for i in range(10)],
            "clientes_activos": [50] * 10,
        }
    )


def calendario_colombia() -> pd.DataFrame:
    fechas = pd.date_range("2026-01-01", periods=10, freq="D")
    return pd.DataFrame(
        {
            "fecha": fechas,
            "pais": ["CO"] * 10,
            "es_festivo": [1 if fecha.day in (1, 6) else 0 for fecha in fechas],
        }
    )


def test_construye_variables_de_fecha_y_festivo():
    features = construir_features(ventas_de_prueba("CO"), calendario_colombia())
    assert {"dia_semana", "mes", "ventas_lag_7", "ventas_media_28", "es_festivo"} <= set(features.columns)
    assert features["es_festivo"].sum() == 2
    assert features["ventas_lag_7"].iloc[7] == 100.0


def test_falla_si_el_calendario_no_cubre_un_pais():
    # Caso de la Actividad 1.3: tiendas de Perú sin festivos en el calendario.
    with pytest.raises(ValueError, match="PE"):
        construir_features(ventas_de_prueba("PE"), calendario_colombia())
