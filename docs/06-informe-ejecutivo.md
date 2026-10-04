# Informe ejecutivo: implementación de DataOps en DataCorp Analytics

Para: Dirección de DataCorp Analytics

Preparado por: Gabriel Alejandro Rodríguez Pulido

Fecha: octubre de 2026

## Resumen

En los últimos meses DataCorp ha tenido datos corruptos, caídas del servicio y reclamos de clientes que ya no confían en nuestras predicciones. Los tres problemas tienen un origen común: el equipo de ciencia de datos trabaja directamente sobre la base de datos de producción, sin un lugar separado para experimentar, sin una versión única de los datos de negocio y sin un proceso controlado para llevar los cambios a producción.

Este informe propone resolverlo en 24 semanas con un enfoque DataOps basado en tres componentes: entornos aislados, gestión de datos maestros y automatización con control de versiones. La primera fase dura dos semanas y elimina la causa directa de los incidentes. Se solicita a la dirección aprobar el plan, los recursos descritos al final y el inicio inmediato de esa primera fase.

## Riesgos actuales

El riesgo más visible es operativo. Cuando un científico de datos prueba una consulta o un modelo nuevo sobre la base real, cualquier error afecta al servicio que reciben los clientes en ese mismo momento. Una consulta mal escrita puede saturar la base y tumbar el servicio, y un script de prueba con un error puede sobrescribir datos de producción. Hoy no hay una barrera técnica que lo impida, porque las mismas cuentas que se usan para experimentar tienen permiso de escritura sobre producción.

El segundo riesgo afecta la relación con los clientes. Cuando una cadena pregunta por qué cambió una predicción, no siempre podemos responder, porque no queda registro de qué versión del código, de los datos y de la configuración produjo cada resultado. Un modelo que no se puede reconstruir tampoco se puede defender ante un cliente.

El tercer riesgo está en los datos de negocio. Cada sistema de origen define a su manera conceptos básicos como "cliente activo". En la práctica, el mismo indicador puede variar en más de 70 % según la fuente de la que se tome, y un cliente puede recibir en el mismo mes un informe y un dashboard con cifras distintas para la misma pregunta.

Hay además un riesgo legal. Los datos de los clientes de nuestras cadenas incluyen información personal protegida por la Ley 1581 de 2012, y hoy esa información se consulta y se copia sin controles suficientes. Por último, la infraestructura se configuró a mano, y parte del conocimiento sobre cómo está montada depende de pocas personas.

## Solución propuesta

La propuesta organiza el trabajo alrededor de tres preguntas: dónde se trabaja, sobre qué datos y cómo.

Para el dónde, se crean tres entornos separados. Desarrollo es el espacio para experimentar, con una muestra de datos sin información personal. QA es una réplica de producción con los datos personales enmascarados, donde cada cambio se prueba antes de salir. Producción queda reservado para atender a los clientes, y ninguna persona puede modificarlo directamente.

Para el sobre qué, se implementa un registro maestro de datos: un sistema que consolida clientes, productos, tiendas, proveedores, cuentas y calendario comercial desde todas las fuentes, elimina duplicados y publica una única versión de cada entidad. Cada entidad tiene un responsable de negocio que aprueba sus definiciones, empezando por la de cliente activo.

Para el cómo, todo lo que define el sistema queda registrado y automatizado. El código, la configuración y la infraestructura se guardan en un repositorio con historial completo, y cada cambio pasa por revisión de otra persona. La infraestructura se crea con código, de modo que los tres entornos salen del mismo molde. Un pipeline automático valida la calidad de los datos, entrena el modelo, lo compara con el que está en producción y solo lo publica si cumple los umbrales y el líder técnico lo aprueba. Si algo falla en producción, el sistema vuelve a la versión anterior en minutos.

## Beneficios esperados

El primer beneficio es la estabilidad. Al separar la experimentación de producción, los errores se quedan en desarrollo o en QA, donde no afectan a ningún cliente. La meta es no tener incidentes de producción causados por cambios sin probar en el último trimestre del plan.

El segundo es la confianza. Cada predicción podrá rastrearse hasta el código, los datos y la configuración que la produjeron, y cualquier modelo en producción podrá reconstruirse para explicarle a un cliente qué pasó. Los clientes verán una sola cifra para cada indicador, sin contradicciones entre reportes.

El tercero es la velocidad. Hoy cada cambio exige cuidado manual y coordinación. Con el pipeline, una mejora al modelo puede llegar a producción en menos de tres días hábiles después de aprobada, y una persona nueva en el equipo puede tener su entorno de trabajo listo en menos de un día.

El cuarto es el cumplimiento. Los datos personales solo existen completos en producción, el acceso queda registrado y las solicitudes de los titulares se atienden desde un único lugar.

Estos resultados se van a seguir con un tablero mensual de métricas, que incluye el tiempo de recuperación ante fallos, el porcentaje de modelos replicables, el número de incidentes en producción y el tiempo de incorporación de personas nuevas.

## Plan de implementación

El plan tiene seis fases en 24 semanas, con inicio propuesto el 2 de noviembre de 2026:

1. Contención (semanas 1 y 2): se retira el permiso de escritura de las cuentas personales sobre producción y se habilita una réplica de solo lectura para que el equipo siga trabajando.
2. Control de versiones e integración continua (semanas 3 a 6).
3. Entornos aislados creados con código (semanas 5 a 10).
4. Registro maestro de datos y nombramiento de responsables (semanas 10 a 17).
5. Pipeline de entrega continua, con el modelo de predicción de ventas como piloto (semanas 14 a 21).
6. Operación, capacitación y tablero de métricas (semanas 22 a 24).

Algunas fases se solapan porque no dependen entre sí. El punto de control principal es la semana 21, cuando el modelo de ventas llegue a producción solo a través del pipeline. Los demás modelos se migran después, siguiendo el camino ya probado.

## Recursos necesarios

En personas, el plan necesita un ingeniero de plataforma dedicado durante los seis meses, por contratación o por asignación interna, para la infraestructura en AWS y el pipeline. También necesita la dirección del líder de ingeniería de datos y la participación del líder de ciencia de datos en la migración del modelo de ventas. Por el lado del negocio, se pide nombrar responsables (data owners) para las entidades maestras, con cerca de una hora semanal cada uno, y dos personas que se encarguen de la calidad de los datos maestros (data stewards) con dedicación de un día por semana.

En infraestructura, el costo nuevo está en los entornos de desarrollo y QA, que hoy no existen. Para contenerlo, QA usa máquinas más pequeñas que producción y las estaciones de desarrollo se apagan fuera del horario laboral. El costo exacto se estima con la calculadora de precios de AWS a partir de los tamaños definidos en el código de infraestructura. Las herramientas principales (Terraform, Jenkins, Airflow, MLflow y DVC) son de código abierto, así que no generan costos de licencia.

Por último, se requieren unas 16 horas de capacitación para el equipo de datos en el nuevo flujo de trabajo, repartidas durante la fase 5.

## Riesgos del plan

El cambio más sensible es que los científicos de datos pierden el acceso directo a producción. Para que esto no frene su trabajo, la réplica de solo lectura está disponible desde la primera fase y el entorno de desarrollo tiene datos realistas. El segundo riesgo es la disponibilidad de los responsables de negocio. Por eso el registro maestro empieza solo con las entidades que usa el modelo de ventas. El tercero es pasar la infraestructura existente a código sin interrumpir el servicio. Para eso se importan los recursos actuales en lugar de recrearlos, y cualquier ajuste se hace en ventanas de mantenimiento acordadas con los clientes.

## Decisión que se solicita

Se solicita a la dirección:

- Aprobar el plan de 24 semanas.
- Autorizar la incorporación o asignación del ingeniero de plataforma.
- Designar a los responsables de las entidades maestras.
- Autorizar el inicio inmediato de la fase de contención, que en dos semanas elimina la causa principal de los incidentes actuales.
