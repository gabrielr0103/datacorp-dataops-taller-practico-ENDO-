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
| 1 | Diseño de entornos aislados | [docs/01-entornos-aislados.md](docs/01-entornos-aislados.md) | Completada |
| 2 | Implementación de MDM | [docs/02-mdm.md](docs/02-mdm.md) | Pendiente |
| 3 | Control de versiones para todo | [docs/03-control-versiones.md](docs/03-control-versiones.md) | Pendiente |
| 4 | Infraestructura como Código | [docs/04-iac.md](docs/04-iac.md) | Pendiente |
| 5 | Continuous Delivery para DataOps | [docs/05-continuous-delivery.md](docs/05-continuous-delivery.md) | Pendiente |
| 6 | Integración final | [docs/06-integracion-final.md](docs/06-integracion-final.md) | Pendiente |

Las capturas de pantalla de cada actividad están en la carpeta [evidencias](evidencias/).   

## Configuración inicial del repositorio

Repositorio creado con las ramas `main` y `develop`:

![Ramas del repositorio](evidencias/00-ramas.png)

README inicial publicado en `develop`:

![README inicial](evidencias/00-readme-inicial.png)

## Actividad 1: Diseño de entornos aislados

Desarrollo completo en [docs/01-entornos-aislados.md](docs/01-entornos-aislados.md).

- 1.1: definición de DEV, QA/Staging y PROD para DataCorp (propósito, acceso, datos, infraestructura y control de código), con la justificación de cada decisión.
- 1.2: diagrama del recorrido de un cambio en el modelo de predicción de ventas, desde el push en una rama feature hasta la disponibilidad en vivo.
- 1.3: protocolo de actuación cuando el modelo falla en QA, con las herramientas y validaciones que impiden que llegue a producción.

### Evidencias

Documento de la actividad en GitHub, con la tabla de entornos y el diagrama de flujo:

![Tabla de entornos](evidencias/01-tabla-entornos.png)

![Diagrama de flujo](evidencias/01-diagrama-flujo.png)

Pull request de la actividad hacia `develop`:

![Pull request Actividad 1](evidencias/01-pull-request.png)