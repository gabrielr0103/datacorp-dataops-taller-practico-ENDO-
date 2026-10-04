## Qué cambia

<!-- Describe el cambio en dos o tres frases y enlaza el issue si existe. -->

## Tipo de cambio

- [ ] Código (src, sql, notebooks)
- [ ] Configuración (config, mdm)
- [ ] Pipeline (DAG o Jenkinsfile)
- [ ] Infraestructura (Terraform)
- [ ] Datos (punteros DVC o procedencia)

## Lista de revisión

- [ ] Las pruebas pasan en local (`pytest`)
- [ ] El linter no reporta errores (`ruff check src tests pipelines`)
- [ ] Si cambian datos, se actualizó el archivo de `data/procedencia/`
- [ ] Si cambia una definición de MDM, se adjuntó el análisis de impacto
- [ ] Si cambia Terraform, se adjuntó la salida de `terraform plan`
- [ ] No se suben datos, credenciales ni archivos `.ipynb`

## Resultado en QA

<!-- Enlace a la ejecución de Jenkins y al experimento de MLflow. -->
