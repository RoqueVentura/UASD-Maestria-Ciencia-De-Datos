# INF-8239 · Unidad 01 · Ejercicio 02

Ensambles, reducción dimensional y Green AI (U01.LAB03). Amplía el problema del Ejercicio 01 (detección de enfermedad hepática con el dataset HCV Data) con ensambles, PCA, t-SNE, mediciones repetidas y una decisión sobre la frontera de Pareto.

## Entorno

- Sistema operativo: Windows 11 Pro (10.0.26200)
- Procesador: Intel64 Family 6 Model 140
- Python: 3.10.11 (64 bits)
- scikit-learn: 1.7.2

## Estructura

```
data/raw/    dataset descargado (no se versiona)
notebooks/   green_ai.ipynb
reports/     resultados, figuras y conclusión
src/         paquete inf8239_u01 (descarga y frontera de Pareto)
tests/       pruebas de la frontera de Pareto
```

## Instalación (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Descarga del dataset

Se usa el mismo dataset del Ejercicio 01: HCV Data, del repositorio UCI (CC BY 4.0, DOI 10.24432/C5D612). La primera celda de datos del notebook lo descarga en `data/raw/dataset.csv` si no existe. También se puede descargar manualmente:

```powershell
$env:PYTHONPATH="src"
python -c "from inf8239_u01.data import download_csv; download_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00571/hcvdat0.csv')"
```

## Protocolo

Es el mismo del Ejercicio 01, fijado antes de comparar modelos:

- **Target:** `hepatopatia` (`si` = hepatitis, fibrosis o cirrosis; `no` = donante sano).
- **Exclusiones:** filas `0s=suspect Blood Donor`, `Unnamed: 0` (fuga) y `Category` (fuente del target).
- **Partición:** 80/20 estratificada con `random_state=42`.
- **Métrica principal:** F1-macro.
- **Clase prioritaria:** `si`.

## Ejecución

1. Abre `notebooks/green_ai.ipynb`, selecciona el kernel `.venv` y ejecuta **Run All**.
2. Ejecuta las pruebas:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

## Resultados

| Archivo | Contenido |
|---|---|
| `reports/green_ai_results.csv` | F1-macro, recall-macro, mediana de 3 ajustes, tiempo de predicción, tamaño serializado y pertenencia a la frontera de Pareto |
| `reports/pareto.png` | F1-macro frente a mediana de ajuste |
| `reports/tsne_two_seeds.png` | Mapas t-SNE con semillas 42 y 7 |
| `reports/models/*.joblib` | Modelos serializados (no se versionan) |
| `reports/conclusion.md` | Conclusión y decisión cuantificada |

Configuraciones comparadas: regresión logística, SVM con C=1 y C=10, Random Forest con 100 y 300 árboles, HistGradientBoosting y, por separado, SVM con PCA sobre el bloque numérico.

Los tiempos dependen del equipo y cambian entre ejecuciones. No representan consumo energético.
