"""Pruebas con los archivos de tests/datos, los mismos que usa la simulación del pipeline de CD."""

from pathlib import Path

import pandas as pd

from src.calidad.validar_datos import validar

DATOS = Path(__file__).parent / "datos"


def test_archivo_valido_pasa_el_test_de_datos():
    ventas = pd.read_csv(DATOS / "ventas_validas.csv", parse_dates=["fecha"])
    assert validar(ventas, max_nulos_pct=10) == []


def test_archivo_con_nulos_no_pasa_el_test_de_datos():
    # 3 de 20 filas sin clientes_activos: 15 % de nulos, por encima del 10 % permitido (Actividad 5.3).
    ventas = pd.read_csv(DATOS / "ventas_con_nulos.csv", parse_dates=["fecha"])
    errores = validar(ventas, max_nulos_pct=10)
    assert errores == ["clientes_activos: 15.0 % de nulos (máximo permitido 10 %)"]
