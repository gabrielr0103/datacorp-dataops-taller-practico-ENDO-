"""Reglas de calidad de los datos de ventas, antes de construir variables y entrenar.

Si alguna regla falla, el proceso termina con código 1 y el pipeline se detiene.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
COLUMNAS_ESPERADAS = [
    "fecha",
    "tienda_mdm_id",
    "cuenta_mdm_id",
    "pais",
    "ventas",
    "transacciones",
    "clientes_activos",
]


def validar(ventas: pd.DataFrame, max_nulos_pct: float) -> list[str]:
    errores = []

    faltantes = [columna for columna in COLUMNAS_ESPERADAS if columna not in ventas.columns]
    if faltantes:
        errores.append(f"Faltan columnas: {faltantes}")
        return errores

    for columna in COLUMNAS_ESPERADAS:
        pct_nulos = ventas[columna].isna().mean() * 100
        if pct_nulos > max_nulos_pct:
            errores.append(f"{columna}: {pct_nulos:.1f} % de nulos (máximo permitido {max_nulos_pct} %)")

    if (ventas["ventas"] < 0).any():
        errores.append("Hay ventas negativas")

    duplicados = int(ventas.duplicated(subset=["fecha", "tienda_mdm_id"]).sum())
    if duplicados:
        errores.append(f"{duplicados} filas duplicadas por fecha y tienda")

    return errores


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida la calidad del archivo de ventas")
    parser.add_argument("--entorno", choices=["dev", "qa", "prod"], required=True)
    parser.add_argument("--archivo", required=True)
    args = parser.parse_args()

    with open(RAIZ / "config" / f"{args.entorno}.yaml", encoding="utf-8") as archivo:
        config = yaml.safe_load(archivo)

    ventas = pd.read_csv(args.archivo, parse_dates=["fecha"])
    errores = validar(ventas, config["calidad"]["max_nulos_pct"])

    if errores:
        print("Validación fallida:")
        for error in errores:
            print(f"  - {error}")
        sys.exit(1)

    print(f"Validación correcta: {len(ventas)} filas")


if __name__ == "__main__":
    main()
