from src.modelos.entrenar import cumple_umbrales, mape

UMBRALES_QA = {"mape_max": 15, "tolerancia_vs_produccion": 1}


def test_mape_calcula_error_porcentual():
    assert round(mape([100, 200], [110, 180]), 2) == 10.0


def test_rechaza_el_candidato_del_escenario_de_la_actividad_1():
    # v1.5.0 con MAPE de 18,7 % frente a v1.4.0 en producción con 12,9 %.
    assert not cumple_umbrales(18.7, 12.9, UMBRALES_QA)


def test_rechaza_si_empeora_mas_de_un_punto_frente_a_produccion():
    assert not cumple_umbrales(14.5, 13.0, UMBRALES_QA)


def test_acepta_un_candidato_dentro_de_los_umbrales():
    assert cumple_umbrales(12.5, 12.9, UMBRALES_QA)
