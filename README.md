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
