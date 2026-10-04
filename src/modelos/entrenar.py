"""Entrena el modelo de predicción de ventas y lo registra en MLflow.

Termina con código 1 si las métricas no cumplen los umbrales del entorno,
para que el pipeline no empaquete ni despliegue el modelo.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]


def mape(real, prediccion) -> float:
    real = np.asarray(real, dtype=float)
    prediccion = np.asarray(prediccion, dtype=float)
    distintos_de_cero = real != 0
    errores = np.abs((real[distintos_de_cero] - prediccion[distintos_de_cero]) / real[distintos_de_cero])
    return float(np.mean(errores) * 100)


def cumple_umbrales(mape_candidato: float, mape_produccion: float | None, umbrales: dict) -> bool:
    if mape_candidato > umbrales["mape_max"]:
        return False
    if mape_produccion is not None:
        return mape_candidato <= mape_produccion + umbrales["tolerancia_vs_produccion"]
    return True


def mape_por_segmento(datos: pd.DataFrame, prediccion, objetivo: str, segmento: str = "pais") -> dict:
    tabla = datos[[segmento, objetivo]].assign(prediccion=np.asarray(prediccion, dtype=float))
    return {
        str(clave): mape(grupo[objetivo], grupo["prediccion"]) for clave, grupo in tabla.groupby(segmento)
    }


def segmentos_fuera_de_umbral(mapes: dict, maximo: float) -> list[str]:
    # Un buen promedio puede esconder un segmento que empeora (Actividad 1.3).
    return sorted(segmento for segmento, valor in mapes.items() if valor > maximo)


def version_codigo() -> str:
    resultado = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=False
    )
    return resultado.stdout.strip()


def version_datos() -> str:
    # El md5 del puntero de DVC identifica la versión exacta de los datos de entrenamiento.
    with open(RAIZ / "data" / "raw" / "ventas.csv.dvc", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)["outs"][0]["md5"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena el modelo de predicción de ventas")
    parser.add_argument("--entorno", choices=["dev", "qa", "prod"], required=True)
    parser.add_argument("--features", required=True)
    parser.add_argument("--mape-produccion", type=float, default=None)
    args = parser.parse_args()

    with open(RAIZ / "config" / f"{args.entorno}.yaml", encoding="utf-8") as archivo:
        config = yaml.safe_load(archivo)
    with open(RAIZ / "config" / "modelo_ventas.json", encoding="utf-8") as archivo:
        config_modelo = json.load(archivo)

    variables = config_modelo["variables"]
    objetivo = config_modelo["objetivo"]
    umbrales = config["umbrales"]

    datos = pd.read_csv(args.features, parse_dates=["fecha"]).dropna(subset=variables)
    corte = datos["fecha"].max() - pd.Timedelta(days=config_modelo["dias_validacion"])
    entrenamiento = datos[datos["fecha"] <= corte]
    validacion = datos[datos["fecha"] > corte]

    import mlflow
    from xgboost import XGBRegressor

    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    mlflow.set_experiment("modelo_ventas")

    with mlflow.start_run():
        modelo = XGBRegressor(**config_modelo["hiperparametros"])
        modelo.fit(entrenamiento[variables], entrenamiento[objetivo])
        prediccion = modelo.predict(validacion[variables])

        mape_candidato = mape(validacion[objetivo], prediccion)
        rmse = float(np.sqrt(np.mean((validacion[objetivo] - prediccion) ** 2)))
        mapes_pais = mape_por_segmento(validacion, prediccion, objetivo)

        mlflow.log_params(config_modelo["hiperparametros"])
        mlflow.log_metrics({"mape": mape_candidato, "rmse": rmse})
        mlflow.log_metrics({f"mape_{pais}": valor for pais, valor in mapes_pais.items()})
        mlflow.set_tags(
            {
                "entorno": args.entorno,
                "commit": version_codigo(),
                "version_datos_dvc": version_datos(),
                "definicion_cliente_activo": config["mdm"]["definicion_cliente_activo"],
            }
        )
        info_modelo = mlflow.xgboost.log_model(
            modelo, name="modelo", input_example=validacion[variables].head(5)
        )

    # El URI del modelo lo usa la etapa de Empaquetado para registrarlo.
    Path("reportes").mkdir(exist_ok=True)
    Path("reportes/modelo_uri.txt").write_text(info_modelo.model_uri, encoding="utf-8")
    metricas = {"mape": round(mape_candidato, 2), "rmse": round(rmse, 2)}
    metricas.update({f"mape_{pais}": round(valor, 2) for pais, valor in mapes_pais.items()})
    Path("reportes/metricas.json").write_text(json.dumps(metricas, indent=2), encoding="utf-8")

    fuera = segmentos_fuera_de_umbral(mapes_pais, umbrales["mape_max_segmento"])
    if not cumple_umbrales(mape_candidato, args.mape_produccion, umbrales) or fuera:
        print(
            f"Modelo rechazado en {args.entorno}: MAPE {mape_candidato:.1f} %, países fuera de umbral: {fuera}"
        )
        sys.exit(1)

    print(f"Modelo aceptado: MAPE {mape_candidato:.1f} %, RMSE {rmse:.1f}")


if __name__ == "__main__":
    main()
