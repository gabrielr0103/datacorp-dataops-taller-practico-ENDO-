import pandas as pd

from src.modelos.entrenar import cumple_umbrales, mape, mape_por_segmento, segmentos_fuera_de_umbral

UMBRALES_QA = {"mape_max": 15, "tolerancia_vs_produccion": 1, "mape_max_segmento": 20}


def test_mape_calcula_error_porcentual():
    assert round(mape([100, 200], [110, 180]), 2) == 10.0


def test_rechaza_el_candidato_del_escenario_de_la_actividad_1():
    # v1.5.0 con MAPE de 18,7 % frente a v1.4.0 en producción con 12,9 %.
    assert not cumple_umbrales(18.7, 12.9, UMBRALES_QA)


def test_rechaza_si_empeora_mas_de_un_punto_frente_a_produccion():
    assert not cumple_umbrales(14.5, 13.0, UMBRALES_QA)


def test_acepta_un_candidato_dentro_de_los_umbrales():
    assert cumple_umbrales(12.5, 12.9, UMBRALES_QA)


def test_detecta_un_pais_fuera_de_umbral_aunque_el_promedio_sea_bueno():
    validacion = pd.DataFrame({"pais": ["CO", "CO", "PE", "PE"], "ventas": [100.0, 100.0, 100.0, 100.0]})
    prediccion = [101.0, 99.0, 130.0, 70.0]
    mapes = mape_por_segmento(validacion, prediccion, "ventas")
    assert mapes == {"CO": 1.0, "PE": 30.0}
    assert segmentos_fuera_de_umbral(mapes, UMBRALES_QA["mape_max_segmento"]) == ["PE"]
