# Conclusión LAB02: auditoría del dataset HCV y línea base

Elegí el dataset HCV Data de UCI (CC BY 4.0) porque permite plantear un problema de tamizaje realista: decidir, a partir de una analítica de sangre de rutina, qué personas deberían pasar a revisión hepatológica. Lo comparé con Maternal Health Risk, que descarté porque más de la mitad de sus filas están duplicadas y solo le quedan 452 observaciones únicas.

La auditoría fue lo que más aportó. La columna `Unnamed: 0`, que parece un simple índice, está ordenada por diagnóstico: los donantes ocupan las primeras 533 filas y los enfermos las últimas. Un árbol entrenado solo con esa columna obtiene un F1 de 1.0, así que la eliminé antes de modelar. También retiré `Category`, de la que sale el target, y las siete filas de donantes sospechosos, porque su etiqueta no es fiable. Los valores ausentes son pocos, pero aparecen sobre todo en pacientes enfermos; los imputé con la mediana dentro del pipeline para que solo se aprendan del conjunto de entrenamiento.

Con la misma partición estratificada y el mismo preprocesamiento, la línea base obtuvo un F1-macro de 0.467 y la SVM sin ajustar llegó a 0.844. La exactitud de la SVM es de 0.94, pero esa cifra engaña: de los 15 enfermos del conjunto de prueba, el modelo solo detectó 9. En este problema ese es el error que más importa, porque un paciente enfermo clasificado como sano se queda sin seguimiento. En cambio, entre los 107 donantes hubo una sola falsa alarma.

La causa principal es el desbalance. Solo el 12 % de las observaciones son positivas, y una SVM sin ajustes tiende a favorecer a la clase mayoritaria. El siguiente paso es probar `class_weight="balanced"` y buscar C y gamma con validación cruzada estratificada, reservando el conjunto de prueba para la evaluación final.

Hay que leer estos resultados con cautela: con 15 positivos en prueba, cada acierto mueve el recall casi siete puntos, los datos provienen de un solo centro y UCI no publica las unidades de las variables. El trabajo es académico y no sustituye un diagnóstico médico.
