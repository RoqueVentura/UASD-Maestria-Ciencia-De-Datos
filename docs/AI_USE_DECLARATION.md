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
- **Mi trabajo:** completé la matriz RACI, revisé los umbrales de `configs/governance.yml`, ejecuté el pipeline de gobernanza, el simulacro de incidente y el tablero, y completé la Model Card y el runbook con la evidencia de LAB11–12.
- **Apoyo de Claude Code:** revisión del laboratorio contra el checklist; corrección para que una puerta sin evidencia no pase como GO; validación de un único Accountable en la RACI; recomendación trazable (versión, política, evidencia y acción humana) en `deployment_decision.json` y en la app; pruebas de contrato (columna faltante), RACI, trazabilidad y app; propuesta de redacción del postmortem del simulacro.
- **Verificaciones:** ejecuté todas las pruebas, revisé que la decisión y las cifras del postmortem coincidan con `reports/lab13/` y `reports/e07/`, y abrí el tablero localmente.

## Responsabilidad
Los valores del análisis son míos: el daño priorizado, las tolerancias, el soporte mínimo de 20 observaciones y la decisión de modificar y limitar. Puedo explicar cada parte y asumo la responsabilidad de lo entregado.
