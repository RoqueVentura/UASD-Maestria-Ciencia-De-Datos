# INF-8239 · Unidad 02 · Proyecto NLP

Autor académico: Edwin Ramón José Nolasco

Proyecto base para LAB04–LAB06. No sustituya la comprensión por ejecución mecánica.

## Inicio rápido

```bash
uv python install 3.12
uv sync
uv run pytest -q
uv run python scripts/audit_data.py
```

Copie `.env.example` como `.env` y configure el dataset aprobado.

## Dataset

Complete `docs/DATASET_CARD.md`, el diccionario, la licencia y el procedimiento de obtención.
El archivo `data/sample/demo_text.csv` solamente comprueba la arquitectura.

## Entrenamiento

```bash
uv run python scripts/train_text.py
uv run streamlit run app/streamlit_app.py
```

## Interpretación

Toda conclusión debe separar observación, evidencia, interpretación y decisión.


## Obtención del dataset

Dataset: Twitter Financial News Sentiment (licencia MIT)
Fuente: https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment

1. Copie `.env.example` como `.env` y configure:
   DATA_SOURCE=url
   DATASET_URL=https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment/resolve/main/sent_train.csv
   DATASET_PATH=data/raw/dataset.csv
   TEXT_COLUMN=text
   TARGET_COLUMN=label
2. Ejecute `uv run python scripts/download_data.py`
3. Verifique el SHA-256: 71aa99d0d37feced03c999ec23b5b25302c92f39d69b6acb0a37aa076c5420e8

El dataset no se incluye en Git (`data/raw/` está en `.gitignore`).

## Clasificación de texto (LAB05)

```bash
uv run python scripts/train_text.py
uv run pytest tests/test_text_model.py -q
uv run streamlit run app/streamlit_app.py
```

El entrenamiento usa una partición estratificada 75/25 (semilla 42) y compara tres pipelines TF-IDF.
Clases: 0 = Bearish, 1 = Bullish, 2 = Neutral.

| Modelo | F1 macro |
|---|---|
| Regresión logística (seleccionado) | 0.726 |
| Complement Naive Bayes | 0.658 |
| Dummy (baseline) | 0.262 |

Artefactos:
- `reports/text_metrics.csv`: F1 macro por modelo
- `reports/confusion_text.png`: matriz de confusión del modelo seleccionado
- `reports/error_analysis.csv`: errores, 20 de ellos categorizados
- `reports/model_evaluation.md`: lectura de métricas, matriz y análisis de errores
- `models/text_model.joblib`: modelo seleccionado
- `docs/cierre_lab05.md`: cierre interpretativo y conclusión

Alcance: titulares financieros en inglés de Twitter. La predicción es una demostración académica, no una recomendación de inversión.

## Notebook ejecutado

`notebooks/01_corpus_clasificador_texto.ipynb` integra la auditoría (LAB04) y la evaluación (LAB05):
procedencia y SHA-256, auditoría, contrato de datos, duplicados y fuga, entrenamiento, métricas por clase,
matriz de confusión, 20 errores categorizados e inferencia con el modelo guardado. Solo lee archivos;
no modifica `reports/` ni `models/`. Requiere haber descargado el dataset y entrenado el modelo.

```bash
uv run jupyter execute --inplace notebooks/01_corpus_clasificador_texto.ipynb
```

En Windows, ejecútelo con `$env:PYTHONUTF8 = "1"` para conservar las tildes. También puede abrirse en
VS Code seleccionando el kernel de `.venv`.

## Instalación con pip

`requirements.txt` permite instalar las mismas versiones sin uv:

```bash
pip install -r requirements.txt
```

## Ejecución en la nube

`requirements-cloud.txt` se genera con:

```bash
uv export --format requirements.txt --output-file requirements-cloud.txt
```

El comando de inicio es `streamlit run app/streamlit_app.py`. La app usa rutas relativas y carga `models/text_model.joblib`, sin depender de `data/raw/` ni de secretos.
