"""Operaciones del pipeline de CD sobre el registro de modelos de MLflow.

Subcomandos:
    campeon    imprime el MAPE del modelo con alias "produccion" (nada si todavía no hay)
    registrar  registra un modelo como nueva versión y le asigna un alias
    promover   pasa un alias a la versión que tiene otro alias
    verificar  carga el modelo de un alias y hace una predicción de prueba

La URI de MLflow sale de la variable de entorno MLFLOW_TRACKING_URI.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

NOMBRE_MODELO = "modelo_ventas"
RAIZ = Path(__file__).resolve().parents[2]


def campeon() -> None:
    from mlflow import MlflowClient
    from mlflow.exceptions import MlflowException

    cliente = MlflowClient()
    try:
        version = cliente.get_model_version_by_alias(NOMBRE_MODELO, "produccion")
    except MlflowException:
        return  # todavía no hay un modelo en producción contra el cual comparar
    print(cliente.get_run(version.run_id).data.metrics["mape"])


def registrar(modelo_uri: str, alias: str) -> None:
    import mlflow
    from mlflow import MlflowClient

    version = mlflow.register_model(modelo_uri, NOMBRE_MODELO)
    MlflowClient().set_registered_model_alias(NOMBRE_MODELO, alias, version.version)
    print(f"{NOMBRE_MODELO} versión {version.version} registrada con el alias '{alias}'")


def promover(desde: str, hacia: str) -> None:
    from mlflow import MlflowClient
    from mlflow.exceptions import MlflowException

    cliente = MlflowClient()
    nueva = cliente.get_model_version_by_alias(NOMBRE_MODELO, desde)

    if hacia == "produccion":
        # La versión que sale de producción queda con el alias "anterior" para el rollback.
        try:
            actual = cliente.get_model_version_by_alias(NOMBRE_MODELO, "produccion")
            cliente.set_registered_model_alias(NOMBRE_MODELO, "anterior", actual.version)
        except MlflowException:
            pass

    cliente.set_registered_model_alias(NOMBRE_MODELO, hacia, nueva.version)
    print(f"Alias '{hacia}' -> {NOMBRE_MODELO} versión {nueva.version} (la que tenía '{desde}')")


def verificar(alias: str, features: str) -> None:
    import mlflow

    config_modelo = json.loads((RAIZ / "config" / "modelo_ventas.json").read_text(encoding="utf-8"))
    variables = config_modelo["variables"]

    modelo = mlflow.pyfunc.load_model(f"models:/{NOMBRE_MODELO}@{alias}")
    datos = pd.read_csv(features).dropna(subset=variables).tail(500)
    prediccion = np.asarray(modelo.predict(datos[variables]), dtype=float)

    if len(prediccion) == 0 or np.isnan(prediccion).any() or (prediccion < 0).any():
        print(f"Prueba de humo fallida con el modelo '{alias}'")
        sys.exit(1)

    print(f"Prueba de humo correcta: {len(prediccion)} predicciones con el modelo '{alias}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Registro de modelos del pipeline de CD")
    sub = parser.add_subparsers(dest="comando", required=True)

    sub.add_parser("campeon")

    p_registrar = sub.add_parser("registrar")
    p_registrar.add_argument("--modelo-uri", required=True)
    p_registrar.add_argument("--alias", required=True)

    p_promover = sub.add_parser("promover")
    p_promover.add_argument("--desde", required=True)
    p_promover.add_argument("--hacia", required=True)

    p_verificar = sub.add_parser("verificar")
    p_verificar.add_argument("--alias", required=True)
    p_verificar.add_argument("--features", required=True)

    args = parser.parse_args()
    if args.comando == "campeon":
        campeon()
    elif args.comando == "registrar":
        registrar(args.modelo_uri, args.alias)
    elif args.comando == "promover":
        promover(args.desde, args.hacia)
    else:
        verificar(args.alias, args.features)


if __name__ == "__main__":
    main()
