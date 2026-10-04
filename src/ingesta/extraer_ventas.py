"""Extrae las ventas diarias por tienda desde la base de datos del entorno indicado.

Uso:
    python -m src.ingesta.extraer_ventas --entorno qa --inicio 2024-10-01 --fin 2026-09-30
"""

import argparse
import os
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
CONSULTA = RAIZ / "sql" / "consultas" / "ventas_diarias_por_tienda.sql"


def cargar_config(entorno: str) -> dict:
    with open(RAIZ / "config" / f"{entorno}.yaml", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def url_conexion(config: dict) -> str:
    # Usuario y contraseña llegan como variables de entorno desde AWS Secrets Manager.
    # Nunca se escriben en el repositorio.
    db = config["base_datos"]
    usuario = os.environ["DB_USUARIO"]
    clave = os.environ["DB_CLAVE"]
    return f"postgresql+psycopg2://{usuario}:{clave}@{db['host']}:{db['puerto']}/{db['nombre']}"


def extraer(entorno: str, inicio: str, fin: str) -> pd.DataFrame:
    from sqlalchemy import create_engine

    config = cargar_config(entorno)
    motor = create_engine(url_conexion(config))
    consulta = CONSULTA.read_text(encoding="utf-8")
    parametros = {
        "inicio": inicio,
        "fin": fin,
        "version_cliente_activo": config["mdm"]["definicion_cliente_activo"],
    }
    return pd.read_sql(consulta, motor, params=parametros)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae las ventas diarias por tienda")
    parser.add_argument("--entorno", choices=["dev", "qa", "prod"], required=True)
    parser.add_argument("--inicio", required=True)
    parser.add_argument("--fin", required=True)
    parser.add_argument("--salida", default="data/raw/ventas.csv")
    args = parser.parse_args()

    ventas = extraer(args.entorno, args.inicio, args.fin)
    ventas.to_csv(args.salida, index=False)
    print(f"{len(ventas)} filas guardadas en {args.salida}")


if __name__ == "__main__":
    main()
