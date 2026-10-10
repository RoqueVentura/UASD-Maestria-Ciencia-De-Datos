# Cierre interpretativo

- **Resultado principal:** Se aprobó el corpus Twitter Financial News Sentiment (9 543 textos, 3 clases) como base reproducible para clasificar sentimiento financiero.
- **Evidencia de calidad y procedencia:** Fuente original en Hugging Face (zeroshot), licencia MIT, commit ccbe24d, SHA-256 71aa99d0…20e8; auditoría con 0 nulos y 0 duplicados.
- **Riesgo o sesgo identificado:** Desbalance de clases (Neutral 64.7 %) y predominio de medios estadounidenses en inglés.
- **Decisión de aprobación o rechazo:** Se aprueba twitter-financial-news-sentiment; se rechaza fake_news_corpus_spanish por tamaño insuficiente (572) y etiqueta no definida.
- **Limitación que debe comunicarse:** Los resultados no se generalizan a otros idiomas, dominios ni periodos; accuracy sola es engañosa.
- **Siguiente verificación:** Comprobar duplicados entre sent_train.csv y sent_valid.csv antes de entrenar, y usar métricas por clase (F1 macro).