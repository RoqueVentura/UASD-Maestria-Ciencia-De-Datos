# Dataset Card

## Identificación
- Nombre: Twitter Financial News Sentiment
- Fuente original: https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment (archivo sent_train.csv)
- Responsable: zeroshot (publicador en Hugging Face)
- Versión o fecha: commit ccbe24de388e287beb92dd393a335c376b350ac3 (2024-02-23); SHA-256 71aa99d0d37feced03c999ec23b5b25302c92f39d69b6acb0a37aa076c5420e8
- Licencia: MIT
- Idioma: inglés

## Propósito y variable objetivo
Uso académico: clasificar el sentimiento de tuits de noticias financieras. La variable objetivo es `label` (0 = Bearish, 1 = Bullish, 2 = Neutral).

## Diccionario de datos

| Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|
| text | string | Tuit o titular de noticia financiera | Texto en inglés de 2 a 190 caracteres; puede incluir cashtags, URLs y menciones |
| label | int64 | Sentimiento anotado | 0 = Bearish, 1 = Bullish, 2 = Neutral |

Ejemplos anonimizados (URLs reemplazadas por [URL] y menciones por [USUARIO]):

| text | label |
|---|---|
| Business owner sues Target for copyright infringement | 0 |
| Household debt jumps the most in 12 years, Federal Reserve report says [URL] | 0 |
| China set to cut tariffs on $75B in U.S. imports by 50% | 1 |
| Hanesbrands EPS and revenue in-line | 1 |
| Indonesia's Reserves Jump to Near Record on Bond Sales | 2 |

## Procedimiento de obtención
1. Configurar `.env` con `DATA_SOURCE=url` y `DATASET_URL` apuntando a sent_train.csv.
2. `uv run python scripts/download_data.py`: descarga a `data/raw/dataset.csv` y muestra el SHA-256.
3. `uv run python scripts/audit_data.py`: auditoría de calidad.

Transformaciones: ninguna sobre `data/raw/`. Solo los ejemplos de esta ficha fueron anonimizados.

## Calidad observada
- 9 543 filas × 2 columnas
- Nulos: 0
- Duplicados de texto: 0
- Distribución: Neutral 64.7 %, Bullish 20.2 %, Bearish 15.1 % (desbalanceada)
- 4 470 textos con URLs y 294 con menciones @
- Algunos caracteres mal codificados y textos truncados

## Población cubierta y excluida
- Cubierta: tuits en inglés de medios y analistas financieros, mayormente del mercado de EE. UU.
- Excluida: otros idiomas, otras redes, temas no financieros e inversionistas individuales. Periodo no documentado.

## Riesgos, sesgos y usos prohibidos
- Sesgos: predominio de la clase Neutral, enfoque en medios estadounidenses y anotación subjetiva.
- Riesgos: menciones de cuentas públicas; los textos provienen de Twitter, sujeto a sus propios términos de uso.
- Usos prohibidos: decisiones de inversión reales, perfilar personas o cuentas, y generalizar los resultados a otros idiomas o dominios.
