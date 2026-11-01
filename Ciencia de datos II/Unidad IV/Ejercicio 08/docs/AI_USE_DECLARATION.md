# Declaración de uso de IA

## Herramienta
Claude Code (Claude Opus 5.5, de Anthropic) en Visual Studio Code, octubre de 2026.

## Mi trabajo
- Instalé el entorno y ejecuté LAB11 en mi equipo (anexo de evidencias, E1–E3). Después ejecuté LAB12 con los comandos del README.
- Completé y ajusté la ficha de impacto, los interesados, el registro de riesgos y la decisión de LAB12.
- Ejecuté las pruebas y las validaciones, revisé las métricas por grupo y definí los criterios del análisis.
- Integré el proyecto en el repositorio del curso e hice los commits y el push.

## Prompts relevantes
- Explicar qué pide cada campo de LAB11 y por qué.
- Revisar mis insumos y la redacción del registro de riesgos.
- Diagnosticar el error de `lab11_impact.py` y el fallo del push.
- Proponer un análisis de mitigación con Fairlearn y sus pruebas.
- Revisar el informe contra el mandato y la rúbrica.

## Apoyo recibido
- Explicaciones de los requisitos.
- Propuestas de redacción, que revisé y ajusté.
- Diagnóstico de errores.
- El código del módulo de mitigación (`src/inf8239_u04/mitigation.py`, `scripts/e07_mitigation.py`, `tests/test_mitigation.py`).
- El formato del PDF.

## Verificaciones
- Comparé las cifras del informe con los CSV y JSON generados y con la salida de consola (`reports/e07/run_log.txt`).
- Repetí el análisis de mitigación y obtuve resultados idénticos.
- Confirmé que las 12 pruebas pasan.

## Correcciones
1. El script base `lab11_impact.py` tenía un error de sintaxis: una cadena con saltos de línea reales. Se corrigió con `\n`.
2. Matizamos la lectura «la logística cumple las brechas» con intervalos de confianza bootstrap.
3. Medimos la alternativa sin modelo en lugar de solo enunciarla.

## LAB13 · Gobernanza y DSS con Streamlit
- **Mi trabajo:** completé la matriz RACI, revisé los umbrales de `configs/governance.yml`, ejecuté el pipeline de gobernanza, el simulacro de incidente y el tablero, y completé la Model Card y el runbook con la evidencia de LAB11–12. Pedí a la IA verificar el laboratorio contra el manual, revisé sus propuestas y las implementé.
- **Apoyo recibido:** propuestas de corrección (recomendación trazable, validación de un único Accountable y pruebas de contrato, RACI y app) y de redacción del postmortem, que revisé y ajusté.
- **Verificaciones:** ejecuté todas las pruebas, comparé la decisión y las cifras con `reports/lab13/` y `reports/e07/`, y abrí el tablero localmente.

## E08 · Expediente de gobernanza y simulacro
- **Mi trabajo:** ejecuté LAB13 en mi equipo y preparé las capturas de evidencia (anexo, E1–E7). Dirigí el trabajo con la IA: indiqué qué verificar contra el manual, el mandato y la rúbrica, definí el alcance y elegí el repositorio y la carpeta de entrega. Revisé cada propuesta antes de aceptarla y pedí cambios cuando fue necesario. Revisé e implementé los artefactos y sus valores (retención, traspasos, umbrales y decisión final). Ejecuté las pruebas y los scripts, hice los commits y las etiquetas, detecté los errores al integrar el proyecto en el repositorio del curso, los resolví con la IA e hice el push.
- **Prompts relevantes:** verificar LAB13 contra el manual y corregir lo faltante; completar E08 según el mandato y la rúbrica; generar el anexo con mis capturas; diagnosticar los errores al integrar el repositorio.
- **Apoyo recibido:** propuestas de código (monitoreo, simulacro, pruebas y generador del PDF) y de redacción, que revisé y ajusté; diagnóstico de errores de Git.
- **Verificaciones:** las pruebas pasan. Las cifras del informe se leen de los CSV y JSON de `reports/e08/`; las comparé con `run_log.txt`.
- **Correcciones:** (1) la alerta mensual omitía el recall cuando un grupo tenía poco soporte. (2) El PSI global no detectó el fallo del simulacro; se documentó y se añadió el perfil por zona. (3) Se recortó de las capturas la barra de estado con una cuenta corporativa. (4) Se corrigieron cifras de la Model Card, el datasheet y el postmortem para que coincidan con sus archivos de origen.

## Responsabilidad
Los valores del análisis son míos: el daño priorizado, las tolerancias, el soporte mínimo de 20 observaciones y la decisión de modificar y limitar. Puedo explicar cada parte y asumo la responsabilidad de lo entregado.
