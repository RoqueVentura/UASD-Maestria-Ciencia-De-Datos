# Decision record

**Sistema:** Territorial Review DSS (sintético). Ordena casos por prioridad para que una persona los revise.
**Propietario:** Dirección de Gestión de Riesgo Territorial
**Fecha:** 2026-10-30

## Decisión: REVIEW

Se puede seguir preparando el sistema solo para un piloto con revisión humana obligatoria. No se aprueba su uso real hasta que LAB12 aporte evidencia de rendimiento y equidad.

## Evidencia disponible

- Evaluación de impacto completa: finalidad, decisión asistida, usos prohibidos, alternativa no predictiva (FIFO), condición de retiro y mecanismo de apelación (`student_inputs/lab11_impact.yml`).
- Cuatro partes interesadas analizadas (`stakeholders.csv`). La persona afectada tiene poder bajo y es quien más daño puede sufrir.
- Ocho riesgos con control, responsable y evidencia (`risk_register_scored.csv`).
- Datos sin identificadores directos, comprobado con `tests/test_privacy.py`.

## Tres riesgos prioritarios

| Riesgo | Prioridad | Interpretación | Responsable |
|---|---|---|---|
| R02 Sesgo de automatización | 9 | Es el más probable: el analista puede aceptar el puntaje sin revisar el caso, y entonces la revisión humana deja de ser real. | Supervisor de analistas |
| R01 Sesgo por subgrupo | 8 | Su impacto es alto y el riesgo residual sigue alto: el sistema podría perjudicar a grupos protegidos o a personas de 60+. Todavía no hay medición. | Equipo de datos |
| R07 Uso fuera de alcance | 8 | El puntaje podría usarse para decidir elegibilidad o intervenciones. El riesgo residual es alto porque una política escrita no impide el mal uso por sí sola. | Propietario institucional |

R01 y R07 tienen la misma prioridad (8), pero considero R01 más urgente: su daño recae sobre grupos protegidos y todavía no se ha medido.

## Incertidumbre

- MEASURE sigue pendiente: aún no se conocen el recall global ni las brechas por subgrupo (LAB12).
- La probabilidad y el impacto son estimaciones basadas en juicio, no mediciones. El orden de prioridad orienta la atención, pero no es una verdad matemática.
- Los datos son sintéticos, así que los resultados no se pueden trasladar a poblaciones reales.

## Condiciones para pasar a GO

1. LAB12 demuestra recall >= 0.68 y brechas de recall y FPR <= 0.16 entre grupos.
2. Los analistas reciben capacitación y el sistema registra que cada caso fue revisado antes de cerrarse.
3. La política de usos prohibidos queda firmada y los accesos al sistema quedan registrados.

## Condición de retiro (STOP)

Se suspende el sistema y se vuelve a la revisión FIFO con reglas explícitas si ocurre cualquiera de estos casos:

- el recall baja de 0.68;
- la brecha de recall o de FPR entre grupos supera 0.16;
- se detecta un uso fuera de alcance;
- se confirma un daño atribuible a la recomendación.

Quien decide la retirada es el propietario institucional.
