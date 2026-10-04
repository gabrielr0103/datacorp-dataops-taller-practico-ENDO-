"""Construye las variables del modelo de predicción de ventas."""

import argparse

import pandas as pd


def construir_features(ventas: pd.DataFrame, calendario: pd.DataFrame) -> pd.DataFrame:
    """Une las ventas con el calendario comercial del hub MDM y calcula las variables.

    ventas: fecha, tienda_mdm_id, pais, ventas, clientes_activos (entre otras).
    calendario: fecha, pais, es_festivo.
    """
    datos = ventas.copy()
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos = datos.sort_values(["tienda_mdm_id", "fecha"])

    datos["dia_semana"] = datos["fecha"].dt.dayofweek
    datos["mes"] = datos["fecha"].dt.month

    ventas_por_tienda = datos.groupby("tienda_mdm_id")["ventas"]
    datos["ventas_lag_7"] = ventas_por_tienda.shift(7)
    datos["ventas_media_28"] = ventas_por_tienda.transform(
        lambda serie: serie.shift(1).rolling(28, min_periods=7).mean()
    )

    cal = calendario[["fecha", "pais", "es_festivo"]].copy()
    cal["fecha"] = pd.to_datetime(cal["fecha"])
    datos = datos.merge(cal, on=["fecha", "pais"], how="left")

    # Regla de cobertura del calendario (Actividad 2.1): si falta algún país o fecha,
    # se detiene aquí en vez de entrenar con festivos incompletos (Actividad 1.3).
    sin_calendario = datos["es_festivo"].isna()
    if sin_calendario.any():
        paises = sorted(datos.loc[sin_calendario, "pais"].unique())
        raise ValueError(f"El calendario comercial no cubre todas las fechas de: {paises}")

    datos["es_festivo"] = datos["es_festivo"].astype(int)
    return datos


def main() -> None:
    parser = argparse.ArgumentParser(description="Construye las variables del modelo de ventas")
    parser.add_argument("--ventas", required=True)
    parser.add_argument("--calendario", required=True)
    parser.add_argument("--salida", required=True)
    args = parser.parse_args()

    ventas = pd.read_csv(args.ventas)
    calendario = pd.read_csv(args.calendario)
    features = construir_features(ventas, calendario)
    features.to_csv(args.salida, index=False)
    print(f"{len(features)} filas con variables guardadas en {args.salida}")


if __name__ == "__main__":
    main()
