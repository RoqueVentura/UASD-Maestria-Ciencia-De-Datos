# Conclusión: Ejercicio 02 (U01.LAB03)

Mantuve el protocolo del Ejercicio 01 sin cambios: el dataset HCV, el target `hepatopatia`, las mismas exclusiones y la partición 80/20 estratificada con `random_state=42`. Antes de comparar fijé el F1-macro como métrica principal y la clase `si` (enfermo) como prioritaria, porque el error más costoso es dejar pasar a un paciente enfermo.

El máximo F1-macro lo obtuvo HistGradientBoosting (`boost`), con 0.9597. En la clase `si` tiene un recall de 0.867: detecta 13 de los 15 enfermos del conjunto de prueba, frente a 9 de la SVM base (`svm_c1`). La mediana de ajuste fue de 0.282 s y el modelo serializado ocupa 181.6 KB.

La frontera de Pareto entre F1-macro y tiempo de ajuste quedó formada por `logistic`, `rf_100` y `boost`. La alternativa más eficiente es la regresión logística: pierde 0.0458 de F1-macro, pero ahorra el 94.5 % del tiempo de ajuste (0.016 s frente a 0.282 s) y ocupa 177.1 KB menos (4.5 KB, un 97.5 % menos). `rf_100` ahorra un 33.3 % del tiempo, pero pierde 0.0221 de F1 y ocupa 152.2 KB más que `boost`. `rf_300` obtiene el mismo F1 que `rf_100` con cuatro veces más tiempo y casi 1 MB de tamaño, así que queda dominado.

Selecciono `boost`. El ahorro de la regresión logística es grande en proporción, pero en términos absolutos son unos 0.27 s por entrenamiento en un problema que no se reentrena de forma continua. A cambio, la logística detecta 11 de los 15 enfermos, dos menos que `boost`, y ese es justamente el error prioritario del protocolo. La logística sería la opción razonable solo si el modelo tuviera que ejecutarse con recursos muy limitados.

El PCA no aportó beneficio. Para conservar el 95 % de la varianza necesitó 10 de las 11 variables numéricas, el F1-macro fue idéntico al de la SVM sin PCA (0.844) y el ajuste tardó el doble. Los dos mapas t-SNE, con semillas 42 y 7, son prácticamente iguales: los enfermos forman pequeños grupos en la periferia y algunos quedan mezclados con los donantes, lo que es coherente con los falsos negativos. Esa separación visual no valida por sí sola ningún clasificador.

Las mediciones se hicieron en un equipo con Windows 11, procesador Intel64 Family 6 Model 140, Python 3.10.11 y scikit-learn 1.7.2. Los tiempos cambian entre ejecuciones y no equivalen a consumo energético; no se midió energía ni CO2. La predicción se midió una sola vez y los bosques aleatorios usan todos los núcleos, lo que afecta su tiempo. Con solo 15 enfermos en prueba, cada acierto mueve el recall casi siete puntos. El trabajo es académico y no sustituye un diagnóstico médico.
