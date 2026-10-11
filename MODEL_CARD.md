# Model Card · Fashion-MNIST CNN

## Modelo y versión
- **Modelo elegido: `cnn_flatten`** (`models/cnn_flatten.keras`, paquete `inf8239_u02_cv` 0.1.0):
  Conv2D(32, 3×3) → MaxPool → Conv2D(64, 3×3) → MaxPool → Flatten → Dropout(0.25) → Dense(10, softmax).
  50,186 parámetros.
- Referencias con la misma partición y entrenamiento:
  - `dense_baseline` (`models/dense_baseline.keras`): Flatten → Dense(64, ReLU) → Dense(10). 50,890 parámetros.
  - `small_cnn`, CNN original del laboratorio (`models/best_cnn.keras`): mismas convoluciones, pero
    GlobalAveragePooling en lugar de Flatten. 19,466 parámetros.
- Entrenamiento: Adam, entropía cruzada categórica dispersa, lote 128, máximo 8 épocas,
  EarlyStopping (paciencia 2, restaura los mejores pesos según `val_loss`), semilla 42.
- Autor: Roque Alexis Ventura Vallejo, octubre de 2026. Uso académico (INF-8239, U02.E04).

## Uso previsto
Ejercicio didáctico de clasificación de imágenes de prendas en escala de grises de 28×28 con 10 categorías,
para comparar arquitecturas y practicar evaluación por clase, análisis de errores y medición de costo.

## Usos fuera de alcance
- Fotografías reales de ropa (color, fondo, pose o resolución distintos): no evaluado.
- Cualquier decisión sobre personas: imágenes médicas, OCR, vigilancia, identificación, moderación.
- Producción o comercio electrónico sin reentrenar y validar con datos del dominio real.

## Dataset y particiones
- Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017), licencia MIT, descargado con `tf.keras.datasets.fashion_mnist`.
- Entrenamiento: primeras 54,000 imágenes del conjunto oficial de entrenamiento.
  Validación: últimas 6,000 (partición fija). Prueba: 10,000 oficiales, usadas solo al final.
- Auditoría (`reports/audit.json`): 0 duplicados exactos dentro de cada partición y 0 imágenes compartidas
  entre particiones (hash MD5 de píxeles). Prueba balanceada (1,000 por clase); validación entre 555 y 633.

## Preprocesamiento
Píxeles `uint8` → `float32` en [0, 1] y canal añadido: forma (28, 28, 1). `validate_images` comprueba forma,
rango, valores finitos y etiquetas en 0–9. Sin aumento de datos.

## Métricas globales y por clase
Conjunto de prueba, 8 épocas (`reports/cv_metrics.json`, `reports/classification_reports.json`):

| Modelo | F1-macro | Accuracy |
|---|---|---|
| **CNN Flatten** | **0.900** | **0.902** |
| Baseline denso | 0.864 | 0.865 |
| CNN del laboratorio | 0.789 | 0.793 |

| Clase | F1 CNN Flatten | Recall CNN Flatten | F1 denso | F1 CNN lab |
|---|---|---|---|---|
| T-shirt/top | 0.850 | 0.898 | 0.818 | 0.717 |
| Trouser | 0.983 | 0.980 | 0.974 | 0.959 |
| Pullover | 0.857 | 0.848 | 0.754 | 0.675 |
| Dress | 0.913 | 0.913 | 0.863 | 0.796 |
| Coat | 0.839 | 0.922 | 0.780 | 0.664 |
| Sandal | 0.978 | 0.992 | 0.951 | 0.916 |
| **Shirt** | **0.676** | **0.577** | 0.651 | 0.422 |
| Sneaker | 0.955 | 0.954 | 0.935 | 0.901 |
| Bag | 0.979 | 0.981 | 0.960 | 0.926 |
| Ankle boot | 0.966 | 0.958 | 0.951 | 0.915 |

Pares más confundidos por la CNN Flatten: Shirt → T-shirt/top (170), Shirt → Coat (140), Pullover → Coat (88).

Curvas (`reports/training_curves.png`): la CNN del laboratorio subajusta (ambas pérdidas siguen bajando en la
época 8); la CNN Flatten termina con pérdida de entrenamiento y de validación casi iguales (≈0.24), sin
sobreajuste. Sensibilidad con 30 épocas en `reports/epochs30/`: la CNN Flatten llega a 0.910 y EarlyStopping la
detiene en la época 15 (mejor época 13: desde ahí la validación deja de mejorar, primer indicio de
sobreajuste); el denso llega a 0.875 y la CNN del laboratorio a 0.848, todavía mejorando en la época 30.

## Comparación de costo
- Hardware: Intel Core i7-1165G7 (11.ª gen., 2.8 GHz), 15.7 GB de RAM, sin GPU; Windows 11.
- Entorno: Python 3.12.13, TensorFlow 2.21.0 (CPU), Keras 3.15.1, scikit-learn 1.9.1.

| Medida (8 épocas) | CNN Flatten | Baseline denso | CNN del laboratorio |
|---|---|---|---|
| Parámetros | 50,186 | 50,890 | 19,466 |
| Archivo `.keras` | 622 KB | 619 KB | 262 KB |
| Entrenamiento | 108.6 s | 6.4 s | 66.8 s |
| Inferencia (mediana de 5, lote 256) | 0.062 ms/img | 0.010 ms/img | 0.060 ms/img |

Los tiempos varían entre corridas: el denso fue el más rápido en todas las mediciones, pero la relación
con la CNN Flatten fue de 1.3 a 6 veces (script de 8 y 30 épocas y notebook).

## Decisión técnica
Se elige la CNN Flatten. Con el mismo presupuesto de parámetros y el mismo tamaño de archivo que el baseline,
gana 3.6 puntos de F1-macro y mejora las 10 clases. Cuesta unas 17 veces más tiempo de entrenamiento y entre 1.3 y 6 veces más tiempo de
inferencia en CPU, pero en valores absolutos (menos de 2 minutos de entrenamiento y
0.06 ms por imagen) el costo es bajo para este benchmark. Si la latencia en CPU fuera la restricción principal,
el baseline denso sería la alternativa. La CNN del laboratorio se descarta: cuesta más que el denso y rinde
menos, porque GlobalAveragePooling promedia la posición de los rasgos.

## Limitaciones y riesgos
- Fashion-MNIST es un benchmark centrado, en escala de grises y con fondo limpio; un buen resultado no se
  transfiere a otros dominios.
- Shirt sigue siendo la clase más débil (recall 0.577): se confunde con T-shirt/top, Coat y Pullover.
- Hay errores con probabilidad 1.00 (`reports/cnn_flatten_errors.png`); la salida no está calibrada.
- Algunas imágenes parecen ambiguas o mal etiquetadas (índices de prueba 1300 y 787).
- Una sola semilla y una sola partición: no se reporta varianza entre corridas.

## Supervisión y monitoreo
- No usar sin revisión humana fuera del contexto académico.
- Antes de otro dominio: recolectar y etiquetar datos propios, rehacer la partición y la auditoría, y revisar
  métricas por clase, no solo la accuracy.
- Si se desplegara: vigilar la distribución de clases predichas y la tasa de baja confianza, muestrear errores
  para revisión y reentrenar cuando cambie la distribución de entrada.
