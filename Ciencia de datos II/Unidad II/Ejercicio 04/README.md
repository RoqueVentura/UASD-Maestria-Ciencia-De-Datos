# INF-8239 · U02.E04 · Clasificador visual con CNN (Fashion-MNIST)

Estudiante: Roque Alexis Ventura Vallejo (100805873)
Proyecto base y guía LAB07: Edwin Ramón José Nolasco

Compara un baseline denso y una CNN pequeña con la misma partición de Fashion-MNIST, y documenta
métricas por clase, curvas, errores visuales, costo computacional y la decisión técnica en
[MODEL_CARD.md](MODEL_CARD.md).

## Estructura

| Ruta | Contenido |
|---|---|
| `src/inf8239_u02_cv/data.py` | Clases, normalización, validación, partición fija y auditoría de duplicados |
| `src/inf8239_u02_cv/models.py` | `build_dense` (baseline) y `build_cnn` |
| `src/inf8239_u02_cv/evaluation.py` | Tiempo de inferencia repetido, pares más confundidos, tamaño de archivo |
| `scripts/train_cv.py` | Entrena ambos modelos y escribe `reports/` y `models/` |
| `scripts/check_runtime.py` | Versión de Python, TensorFlow y GPU detectada |
| `notebooks/01_fashion_mnist_cnn.ipynb` | Notebook ejecutado: auditoría, verificación del modelo guardado, curvas, errores y costo |
| `tests/` | Contratos de datos y de salida del modelo (pytest) |
| `reports/` | Métricas (`cv_metrics.json`, `classification_reports.json`, `audit.json`, `history.json`) y figuras |
| `reports/U02_E04_Roque_Ventura.pdf` | Informe de entrega del Ejercicio 04 |
| `reports/epochs30/` | Experimento de sensibilidad con 30 épocas |
| `models/` | `best_cnn.keras` y `dense_baseline.keras` |

## Reproducir (CPU, Windows/Linux/macOS)

Requiere [uv](https://docs.astral.sh/uv/). Desde la raíz del proyecto:

```bash
uv python install 3.12
uv sync --extra cpu                       # crea .venv con TensorFlow 2.21 CPU y dependencias de desarrollo
uv run python scripts/check_runtime.py
uv run python scripts/train_cv.py --epochs 8                          # corrida principal (~1 min en CPU)
uv run python scripts/train_cv.py --epochs 30 --run-name epochs30     # sensibilidad (~4 min en CPU)
uv run pytest -q
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_fashion_mnist_cnn.ipynb
```

El dataset (público, ~30 MB) lo descarga TensorFlow a su caché la primera vez. La semilla es 42 y
`TF_DETERMINISTIC_OPS=1`; en el mismo equipo cuatro corridas dieron el mismo F1. Los tiempos sí varían.

Sin uv: `python -m venv .venv`, activar el entorno, `pip install -r requirements.txt pytest`
y ejecutar los scripts con `PYTHONPATH=src`.

### GPU

Solo en WSL2/Linux con NVIDIA configurada: `uv sync --extra gpu`. En Windows nativo TensorFlow ≥ 2.11
no usa GPU; los resultados de este repositorio son en CPU.

### Colab

```python
%pip install -r requirements-colab.txt
```

## Resultados (prueba, 10,000 imágenes, 8 épocas)

| Modelo | F1-macro | Accuracy | Parámetros | Archivo | Entrenamiento | Inferencia |
|---|---|---|---|---|---|---|
| Baseline denso | 0.864 | 0.865 | 50,890 | 619 KB | 5.8 s | 0.012 ms/img |
| CNN pequeña | 0.789 | 0.793 | 19,466 | 262 KB | 66.9 s | 0.055 ms/img |

Con 30 épocas: denso 0.875 y CNN 0.848. Interpretación y decisión en [MODEL_CARD.md](MODEL_CARD.md).
