# Declaración de uso de IA

## Herramienta
Claude (Anthropic), modelo Claude Opus 5.5, usado mediante Claude Code en VS Code.

## Finalidad
Usé la IA como apoyo en LAB11. No la usé como sustituto de mi trabajo: el análisis, la revisión y las decisiones finales fueron míos. Me ayudó a:
- entender la estructura del proyecto y lo que pedía cada archivo;
- proponer borradores de texto que luego revisé y modifiqué;
- detectar y corregir un error técnico en el script del laboratorio.

## Fragmentos afectados
- `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv` y `student_inputs/risk_register.csv`: la IA propuso un primer borrador del contenido. Yo lo revisé, lo ajusté al caso y lo completé.
- `reports/lab11/DECISION_RECORD.md`: redactamos el registro de decisión en conjunto, a partir de los riesgos prioritarios que calculó el script.
- `scripts/lab11_impact.py` (línea 11): corrección de un error de sintaxis.

## Verificaciones humanas
- Comprobé que los umbrales usados (recall >= 0.68 y brechas <= 0.16) coinciden con `configs/governance.yml`.
- Revisé que los escenarios de riesgo correspondan a los valores de probabilidad e impacto dados, y que cada riesgo tenga control, responsable y evidencia.
- Ejecuté `scripts/lab11_impact.py` y `pytest` (`test_impact.py`, `test_privacy.py`) y confirmé que todo pasó.
- Revisé la decisión REVIEW y su justificación antes de aceptarla.

## Errores detectados y correcciones
- **Error en el script base:** `scripts/lab11_impact.py` tenía un texto entre comillas con saltos de línea reales, lo que producía `SyntaxError: unterminated string literal`. Se corrigió usando `\n`.
- **Datos supuestos por la IA:** el nombre del propietario institucional ("Dirección de Gestión de Riesgo Territorial") y el plazo de apelación (10 días hábiles) son supuestos que la IA propuso para el caso sintético. Los revisé y acepté como parte del escenario didáctico.

## LAB12 · Auditoría de equidad
- **Finalidad:** apoyo para ejecutar las auditorías (logística y árbol), leer las métricas y redactar la interpretación.
- **Fragmentos afectados:** `student_inputs/lab12_decision.yml` y `reports/lab12/AUDIT_REPORT.md`, ambos redactados en conjunto a partir de las métricas generadas por `scripts/lab12_audit.py`.
- **Verificaciones humanas:** comparé las cifras del informe con `global_metrics.json`, `fairness_by_group.csv` y `fairness_intersectional.csv`. También ejecuté `validate_lab12_decision.py` y `pytest` (`test_fairness.py`, `test_model.py`).
- **Supuestos:** el soporte mínimo de 20 observaciones para los grupos interseccionales es un criterio propio, porque el proyecto no fija uno.

## Responsabilidad
Asumo la responsabilidad por el contenido entregado.
