# Ficha del dataset

- **Dominio:** Salud: hepatología y laboratorio clínico.
- **Unidad de análisis:** Un paciente o donante de sangre, con una analítica sanguínea y sus datos demográficos (edad y sexo).
- **Decisión:** Priorizar qué analíticas de rutina se derivan a revisión hepatológica (tamizaje), no sustituir el diagnóstico.
- **Target:** `hepatopatia` (derivado de `Category`): `si` = hepatitis C, fibrosis o cirrosis; `no` = donante sano.
- **Tipo de tarea:** Clasificación binaria supervisada.
- **Error más costoso:** El falso negativo, es decir, clasificar como sano a un paciente con enfermedad hepática. Retrasa el tratamiento y la enfermedad puede avanzar hacia la cirrosis. Un falso positivo solo genera una prueba confirmatoria adicional.
- **Usuario:** Personal de laboratorio clínico o de atención primaria que revisa analíticas de rutina.

> **Advertencia:** este trabajo es académico y **no constituye un diagnóstico médico**.

## Candidatos

| Criterio | Candidato A: HCV Data | Candidato B: Maternal Health Risk |
|---|---|---|
| Procedencia | UCI ML Repository. Lichtinghagen, Klawonn y Hoffmann (Hannover Medical School). Donado el 09-06-2020. | UCI ML Repository. Marzia Ahmed (Daffodil International University). Donado el 14-08-2023. |
| Ficha | https://archive.ics.uci.edu/dataset/571/hcv+data | https://archive.ics.uci.edu/dataset/863/maternal+health+risk |
| Descarga | CSV directo: https://archive.ics.uci.edu/ml/machine-learning-databases/00571/hcvdat0.csv | Solo en ZIP: https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip |
| DOI | 10.24432/C5D612 | 10.24432/C5DP5D |
| Licencia | CC BY 4.0 (permite uso académico citando la fuente) | CC BY 4.0 |
| Filas/columnas | 615 × 14 (12 predictores, un ID y el target); 46 KB | 1014 × 7 (6 predictores y el target); 3 KB |
| Target y clases | `Category`: donante 533, donante sospechoso 7, hepatitis 24, fibrosis 21, cirrosis 30. Binarizado: `no` 533 / `si` 75. | `RiskLevel`: bajo 406, medio 336, alto 272 |
| Ausentes | 31 celdas en 26 filas (ALP 18, CHOL 10, ALB 1, ALT 1, PROT 1). Se concentran en pacientes enfermos. | Ninguno |
| Duplicados | 0 | **562 filas duplicadas (55 %)**: solo quedan 452 filas únicas |
| Riesgo de fuga | **Alto si no se trata.** La columna ID (`Unnamed: 0`) está ordenada por clase, así que por sí sola predice el target con F1 = 1.0. Se elimina. | Medio: los duplicados pueden quedar a la vez en entrenamiento y prueba. |
| Otros riesgos | Clases desbalanceadas (12 % positivos). Categoría ambigua "suspect Blood Donor". | `HeartRate` = 7 lpm (fisiológicamente imposible). Pocas variables. |

## Criterios de aceptación

| Criterio | A: HCV Data | B: Maternal Health Risk |
|---|---|---|
| ≥ 500 filas | ✅ 615 (608 tras excluir "sospechoso") | ⚠️ 1014 filas, pero solo 452 únicas |
| Target observable con ≥ 2 clases | ✅ | ✅ |
| Uso académico permitido | ✅ CC BY 4.0 | ✅ CC BY 4.0 |
| Variables disponibles al predecir | ✅ Las analíticas se obtienen antes del diagnóstico | ✅ |
| Compatible con CPU/Colab gratuito | ✅ 46 KB | ✅ 3 KB |

**Selección:** el candidato **A (HCV Data)**. Cumple todos los criterios, tiene descarga CSV directa y documentada, y presenta problemas reales que se resuelven dentro de un pipeline (ausentes, una variable categórica, desbalance, un identificador con fuga). El candidato B no llega a 500 observaciones únicas y tiene valores implausibles.

## Decisiones de preparación

- **Se excluyen las 7 filas `0s=suspect Blood Donor`.** Su etiqueta es incierta (no se sabe si están sanas o enfermas), así que no sirven ni como positivo ni como negativo fiable.
- **Se excluye `Unnamed: 0`.** Es un identificador de fila, no tiene significado clínico y está ordenado por clase, lo que constituye una fuga.
- **Se excluye `Category` de X.** Es la fuente del target.

## Cita

Lichtinghagen, R., Klawonn, F., & Hoffmann, G. (2020). *HCV data* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5D612
