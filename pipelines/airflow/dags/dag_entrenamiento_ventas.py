"""DAG semanal de entrenamiento del modelo de predicción de ventas.

Escrito para Airflow 2.10. El entorno (dev, qa o prod) sale de la variable de Airflow
"entorno", que tiene un valor distinto en cada despliegue.
"""

from datetime import UTC, datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

REPO = "/opt/airflow/repos/datacorp-dataops"
ENTORNO = "{{ var.value.entorno }}"

argumentos = {
    "owner": "ciencia-de-datos",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="entrenamiento_modelo_ventas",
    description="Extrae ventas, valida calidad, construye variables y entrena el modelo",
    schedule="0 3 * * 1",  # lunes a las 3:00
    start_date=datetime(2026, 10, 5, tzinfo=UTC),
    catchup=False,
    default_args=argumentos,
    tags=["ventas", "dataops"],
) as dag:
    extraer_ventas = BashOperator(
        task_id="extraer_ventas",
        bash_command=(
            f"cd {REPO} && python -m src.ingesta.extraer_ventas --entorno {ENTORNO} "
            "--inicio {{ macros.ds_add(ds, -730) }} --fin {{ ds }} --salida data/raw/ventas.csv"
        ),
    )

    obtener_calendario = BashOperator(
        task_id="obtener_calendario",
        bash_command=f"cd {REPO} && dvc pull data/raw/calendario_comercial.csv",
    )

    validar_calidad = BashOperator(
        task_id="validar_calidad",
        bash_command=(
            f"cd {REPO} && python -m src.calidad.validar_datos --entorno {ENTORNO} "
            "--archivo data/raw/ventas.csv"
        ),
    )

    construir_features = BashOperator(
        task_id="construir_features",
        bash_command=(
            f"cd {REPO} && python -m src.features.construir_features "
            "--ventas data/raw/ventas.csv --calendario data/raw/calendario_comercial.csv "
            "--salida data/processed/features.csv"
        ),
    )

    entrenar_modelo = BashOperator(
        task_id="entrenar_modelo",
        bash_command=(
            f"cd {REPO} && python -m src.modelos.entrenar --entorno {ENTORNO} "
            "--features data/processed/features.csv"
        ),
    )

    extraer_ventas >> validar_calidad
    [validar_calidad, obtener_calendario] >> construir_features >> entrenar_modelo
