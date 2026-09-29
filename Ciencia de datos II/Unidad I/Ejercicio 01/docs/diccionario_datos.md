# Diccionario de datos: HCV Data

**Fuente de todas las variables:** UCI ML Repository, HCV Data (DOI 10.24432/C5D612). Son analíticas de sangre de donantes y de pacientes con hepatitis C.

**Unidades:** UCI no las publica. Las indicadas se infieren de los rangos observados y de la bibliografía de los autores (Hoffmann et al., 2018). Deben verificarse antes de cualquier interpretación clínica.

**Disponibilidad:** todas las variables de laboratorio se obtienen de la misma extracción de sangre, antes de establecer el diagnóstico, así que están disponibles en el momento de predecir.

| Variable | Significado | Unidad | Tipo | Ausentes | Transformación prevista | Riesgo |
|---|---|---|---|---|---|---|
| `Unnamed: 0` | Identificador de fila | — | entero | 0 | **Excluir** | **Fuga:** está ordenado por clase y predice el target con F1 = 1.0 |
| `Category` | Diagnóstico: 0 donante, 0s donante sospechoso, 1 hepatitis, 2 fibrosis, 3 cirrosis | — | categórica | 0 | Se deriva el target `hepatopatia`; se excluyen las filas `0s`; la columna no entra en X | Es la fuente del target: usarla como predictor sería fuga |
| `Age` | Edad | años | entero | 0 | Imputar con la mediana y estandarizar | Bajo |
| `Sex` | Sexo (m/f) | — | categórica | 0 | Imputar con la moda y aplicar one-hot | Sesgo: 377 hombres frente a 238 mujeres |
| `ALB` | Albúmina | g/L | continua | 1 | Imputar con la mediana y estandarizar | Bajo |
| `ALP` | Fosfatasa alcalina | U/L | continua | 18 | Imputar con la mediana y estandarizar | Los ausentes se concentran en pacientes enfermos (ausencia informativa) |
| `ALT` | Alanina aminotransferasa | U/L | continua | 1 | Imputar con la mediana y estandarizar | Valores extremos (hasta 325) |
| `AST` | Aspartato aminotransferasa | U/L | continua | 0 | Estandarizar | Valores extremos (hasta 324) |
| `BIL` | Bilirrubina | µmol/L | continua | 0 | Estandarizar | Valores extremos (hasta 254) |
| `CHE` | Colinesterasa | kU/L | continua | 0 | Estandarizar | Bajo |
| `CHOL` | Colesterol | mmol/L | continua | 10 | Imputar con la mediana y estandarizar | Ausencia informativa |
| `CREA` | Creatinina | µmol/L | continua | 0 | Estandarizar | Valores extremos (hasta 1079, posible insuficiencia renal) |
| `GGT` | Gamma-glutamil transferasa | U/L | continua | 0 | Estandarizar | Valores extremos (hasta 651) |
| `PROT` | Proteínas totales | g/L | continua | 1 | Imputar con la mediana y estandarizar | Bajo |
| `hepatopatia` | **Target derivado:** `si` si `Category` es 1, 2 o 3; `no` si es 0 | — | binaria | 0 | Variable objetivo | Desbalance: 75 `si` frente a 533 `no` (12 %) |
