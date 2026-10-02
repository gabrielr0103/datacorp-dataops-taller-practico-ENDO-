# DataCorp Analytics: entorno DataOps

Parte práctica del taller asíncrono.

- **Curso:** Enfoque DataOps
- **Profesora:** Maia José Torres Nieves
- **Estudiante:** Gabriel Alejandro Rodríguez Pulido
- **Universidad:** Escuela Colombiana de Ingeniería Julio Garavito

## Contexto del caso

DataCorp Analytics ofrece servicios de análisis predictivo para el sector retail. Su equipo de ciencia de datos trabaja directamente sobre la base de datos de producción, lo que ha causado corrupción de datos, caídas del servicio y pérdida de confianza de los clientes. En este repositorio se diseña, de forma simulada, un entorno DataOps con entornos aislados, gestión de datos maestros y estrategias de control y replicabilidad (control de versiones, IaC y CD).

## Estrategia de ramas

El repositorio aplica la misma lógica de entornos que se propone para la empresa:

| Rama | Equivale a | Regla |
|---|---|---|
| `main` | Producción | Solo recibe cambios desde `develop` por pull request |
| `develop` | QA / staging | Integra las ramas de cada actividad por pull request |
| `feature/actividad-N-...` | Desarrollo | Una rama por actividad |

## Contenido

| Actividad | Tema | Documento | Estado |
|---|---|---|---|
| 1 | Diseño de entornos aislados | [docs/01-entornos-aislados.md](docs/01-entornos-aislados.md) | Pendiente |
| 2 | Implementación de MDM | [docs/02-mdm.md](docs/02-mdm.md) | Pendiente |
| 3 | Control de versiones para todo | [docs/03-control-versiones.md](docs/03-control-versiones.md) | Pendiente |
| 4 | Infraestructura como Código | [docs/04-iac.md](docs/04-iac.md) | Pendiente |
| 5 | Continuous Delivery para DataOps | [docs/05-continuous-delivery.md](docs/05-continuous-delivery.md) | Pendiente |
| 6 | Integración final | [docs/06-integracion-final.md](docs/06-integracion-final.md) | Pendiente |

Las capturas de pantalla de cada actividad están en la carpeta [evidencias](evidencias/).   
