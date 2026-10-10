# Cierre interpretativo · U02.LAB05

- **Resultado principal:** Los dos clasificadores superan ampliamente al baseline; la regresión logística con TF-IDF obtuvo el mejor F1 macro (0.726) frente a Naive Bayes (0.658) y al Dummy (0.262).
- **Modelo seleccionado y evidencia:** Regresión logística (`models/text_model.joblib`). Evidencia: `reports/text_metrics.csv`, `reports/confusion_text.png` y `reports/model_evaluation.md`.
- **Clase con mayor dificultad:** Bearish (0), con recall 0.611 y precision 0.606; 140 de 360 casos reales se pierden, 89 de ellos como Neutral.
- **Tipo de error más frecuente:** Jerga financiera y cifras (8 de 20 errores categorizados), seguido de ambigüedad (4).
- **Impacto en el contexto:** Una noticia negativa clasificada como neutral oculta un riesgo de mercado; una noticia neutral clasificada como Bearish o Bullish genera una falsa señal que podría motivar decisiones de inversión sin fundamento.
- **Limitación del dataset:** Solo inglés, solo Twitter, dominio financiero mayormente estadounidense, periodo no documentado y clases desbalanceadas (Neutral 65 %).
- **Decisión antes del despliegue:** Publicar únicamente como demostración académica, con advertencia de alcance visible; no usar para decisiones reales hasta mejorar el recall de Bearish.

## Conclusión

Este laboratorio transformó el corpus auditado en LAB04, Twitter Financial News Sentiment, en un sistema de clasificación de sentimiento financiero evaluado y reutilizable. El corpus contiene 9 543 titulares y tuits en inglés con tres clases: Bearish, Bullish y Neutral. A partir de una única partición estratificada 75/25 con semilla 42, se entrenaron tres pipelines que mantienen el vectorizador TF-IDF dentro del pipeline para evitar fuga de información: un DummyClassifier como baseline, Complement Naive Bayes y regresión logística con pesos balanceados.

La primera lección es que la accuracy aislada engaña. El baseline, que siempre predice Neutral, alcanza 0.648 de accuracy sin aprender nada, porque esa clase representa el 65 % del corpus. Su F1 macro, en cambio, es apenas 0.262. Por eso la comparación se hizo con F1 macro, que da el mismo peso a cada clase. Con ese criterio, la regresión logística (0.726) supera claramente a Naive Bayes (0.658). La diferencia no está en la clase mayoritaria, sino en las minoritarias: Naive Bayes solo recupera el 35 % de las noticias Bearish, mientras que la regresión logística recupera el 61 %.

Aun así, Bearish sigue siendo la clase más difícil. Tiene el menor recall (0.611) y la menor precision (0.606). La matriz de confusión muestra que 89 noticias negativas se clasificaron como neutrales, y que 106 noticias neutrales se marcaron como Bearish y otras 106 como Bullish. En un contexto financiero, estos errores no son simples números: una señal negativa que pasa inadvertida oculta un riesgo, y una falsa señal puede inducir a comprar o vender sin fundamento.

El análisis manual de 20 errores ofrece una hipótesis concreta. La categoría dominante fue la jerga financiera y las cifras (8 casos): expresiones como "profits almost halved", "+14.6%", "puts" o "hits the sidelines" llevan sentimiento, pero TF-IDF las trata como palabras aisladas y pierde el signo de los porcentajes. Le siguen la ambigüedad (4), las etiquetas discutibles (3), por ejemplo una advertencia de "calamidad económica" etiquetada como neutral, y los textos fuera del dominio (3), como frases motivacionales. También apareció un caso de negación ("fails to salvage"). Ninguna predicción se corrigió manualmente.

La aplicación Streamlit permite clasificar textos nuevos y advierte que se trata de una demostración académica. Las pruebas confirmaron que la app responde bien a titulares financieros claros, pero ante una frase en español o fuera del dominio igualmente devuelve una de las tres clases. Esto confirma que la salida es una predicción condicionada por los datos de entrenamiento y no una verdad.

Las conclusiones se limitan a titulares financieros en inglés publicados en Twitter, mayormente sobre el mercado estadounidense, en un periodo no documentado. No se pueden generalizar a otros idiomas, redes sociales ni temas.

Antes de un despliegue real proponemos dos pasos: verificar la hipótesis del análisis de errores conservando las cifras con su signo y comparando el recall de Bearish, y validar con `sent_valid.csv` verificando que no haya duplicados con el entrenamiento. Mientras tanto, el modelo solo debe publicarse como demostración, con su advertencia de alcance visible.
