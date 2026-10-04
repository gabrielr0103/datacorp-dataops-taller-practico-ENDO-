#!/usr/bin/env bash
# Simulación local del pipeline de CD del modelo de ventas (Actividad 5.3).
#
# Las etapas 1 y 2 se ejecutan de verdad, con el mismo código del Jenkinsfile.
# Las etapas 3 a 6 solo se describen, porque necesitan MLflow, AWS y Jenkins.
# Igual que en Jenkins, si una etapa falla las siguientes no se ejecutan.
#
# Uso (desde la raíz del repositorio, con el entorno virtual activo):
#   bash pipelines/simular_cd.sh tests/datos/ventas_validas.csv
#   bash pipelines/simular_cd.sh tests/datos/ventas_con_nulos.csv

set -uo pipefail

ARCHIVO="${1:?Indica el archivo de ventas que revisa el Test de Datos}"
ETAPAS=("Build & Test" "Test de Datos" "Train & Validate" "Empaquetado" "Despliegue en Staging" "Despliegue en Producción")

etapa() {
  echo ""
  echo "=== Etapa $1/6: ${ETAPAS[$(($1 - 1))]} ==="
}

detener() {
  local fallida=$1
  echo ""
  echo "PIPELINE DETENIDO en la etapa $fallida: ${ETAPAS[$((fallida - 1))]}"
  echo "Etapas que no se ejecutan:"
  for ((i = fallida; i < ${#ETAPAS[@]}; i++)); do
    echo "  - ${ETAPAS[$i]}"
  done
  echo "El modelo no se empaqueta ni se despliega. Producción sigue con la versión que tenía."
  exit 1
}

etapa 1
ruff check src tests pipelines && pytest -q || detener 1

etapa 2
python -m src.calidad.validar_datos --entorno qa --archivo "$ARCHIVO" || detener 2

etapa 3
echo "(simulada) Se construyen las variables, se entrena el modelo y se compara con el de producción:"
echo "           MAPE máximo 15 %, tolerancia de 1 punto y máximo 20 % por país (config/qa.yaml)."

etapa 4
echo "(simulada) El modelo se registra en MLflow como una versión nueva con el alias 'candidato'."

etapa 5
echo "(simulada) Terraform aplica envs/qa.tfvars, Flyway migra la base de QA,"
echo "           el alias 'staging' pasa a la versión nueva y corre la prueba de humo."

etapa 6
echo "(simulada) Con la aprobación del líder técnico, el alias 'produccion' pasa a la versión nueva"
echo "           y la versión que sale queda con el alias 'anterior' para el rollback."

echo ""
echo "PIPELINE COMPLETO: el modelo llegó a producción."
