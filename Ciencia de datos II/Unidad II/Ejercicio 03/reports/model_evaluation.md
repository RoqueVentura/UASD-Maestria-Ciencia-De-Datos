# Evaluación de modelos · U02.LAB05

Corpus: Twitter Financial News Sentiment (`sent_train.csv`, 9 543 textos).
Partición estratificada 75/25 con semilla 42; prueba = 2 386 textos.
Clases: 0 = Bearish, 1 = Bullish, 2 = Neutral.

## Métricas

| Modelo | F1 macro | Accuracy |
|---|---|---|
| Regresión logística | 0.726 | 0.795 |
| Complement Naive Bayes | 0.658 | 0.779 |
| Dummy (baseline) | 0.262 | 0.648 |

Reporte por clase del modelo seleccionado (regresión logística):

| Clase | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| 0 · Bearish | 0.606 | 0.611 | 0.609 | 360 |
| 1 · Bullish | 0.686 | 0.713 | 0.699 | 481 |
| 2 · Neutral | 0.875 | 0.863 | 0.869 | 1545 |

## Lectura de las métricas

**¿Supera el baseline?**
Sí. La regresión logística (F1 macro 0.726) supera al Dummy (0.262) por +0.46 y a Naive Bayes (0.658) por +0.07. La mejora justifica seleccionarla.

**¿Qué clase se pierde?**
Bearish (0), con el menor recall (0.611). En la fila 0 de la matriz, 140 de 360 casos reales se pierden: 89 se predicen como Neutral y 51 como Bullish.

**¿Qué predicción es poco confiable?**
La predicción Bearish (0), con la menor precision (0.606). La columna 0 tiene 143 falsos positivos: 106 eran Neutral y 37 Bullish.

**¿Existe desbalance?**
Sí. Support: Neutral 1 545 (65 %), Bullish 481 (20 %), Bearish 360 (15 %). El Dummy alcanza 0.648 de accuracy prediciendo siempre Neutral, por lo que la accuracy aislada es engañosa. Naive Bayes logra 0.779 de accuracy, pero solo recupera el 35 % de los Bearish.

**¿Puede generalizar?**
No fuera del corpus. Las conclusiones aplican solo a titulares y tuits financieros en inglés, publicados en Twitter por medios y analistas (mayormente de EE. UU.), en un periodo no documentado.

## Matriz de confusión (`reports/confusion_text.png`)

| Real \ Predicho | 0 · Bearish | 1 · Bullish | 2 · Neutral |
|---|---|---|---|
| 0 · Bearish | **220** | 51 | 89 |
| 1 · Bullish | 37 | **343** | 101 |
| 2 · Neutral | 106 | 106 | **1333** |

- **Diagonal (aciertos):** 220 Bearish, 343 Bullish, 1 333 Neutral.
- **Mayor confusión fuera de la diagonal:** Neutral predicho como Bearish (106) y como Bullish (106), seguido de Bullish predicho como Neutral (101).
- **Costo real:** cuando una noticia neutral se marca como Bearish o Bullish, se genera una falsa señal de mercado que podría motivar decisiones de compra o venta sin fundamento. A la inversa, las 89 noticias Bearish marcadas como Neutral son señales negativas que pasan inadvertidas.

## Análisis de errores (`reports/error_analysis.csv`)

El modelo seleccionado cometió 490 errores en prueba. Se clasificaron manualmente 20 (columna `category`); las predicciones no se modificaron.

| Categoría | Errores | Ejemplo |
|---|---|---|
| Jerga financiera / cifras | 8 | "Celanese Q4 profits almost halved" (real Bearish, predicho Neutral) |
| Ambigüedad | 4 | "Asian shares mixed as doubts grow on elusive U.S.-China trade deal" |
| Etiqueta discutible | 3 | "Jokowi Warns of Economic Calamity From Forest Fires" (etiquetado Neutral) |
| Tema fuera del dominio | 3 | "It is only failure if you stay down after the fall…" |
| Texto insuficiente | 1 | "Ahold Delhaize share buyback update" |
| Negación | 1 | "Nokia's surprise profit rise fails to salvage 2019 dividend" |

**Hipótesis verificable:** el error dominante es la jerga financiera. TF-IDF no capta que "+14.6%", "halved", "puts" o "hits the sidelines" expresan sentimiento, y el signo de cifras como "-3.5%" se pierde al tokenizar. Siguiente experimento: conservar cifras con su signo o incorporar un léxico o modelo del dominio financiero, y comparar el recall de Bearish.

## Conclusión

La regresión logística obtuvo el mejor F1 macro (0.726). Sin embargo, la clase **Bearish** presentó el menor recall (0.611), con **140 falsos negativos**, la mayoría confundidos con Neutral (89). En este contexto ese error implica **no detectar noticias negativas para el mercado y presentarlas como neutrales**. Por ello proponemos **analizar los errores Bearish↔Neutral, evaluar más ejemplos negativos o ajustar el umbral de decisión** antes de publicar.
