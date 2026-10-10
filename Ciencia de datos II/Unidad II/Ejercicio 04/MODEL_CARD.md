# Model Card · Fashion-MNIST CNN

## Modelo y versión
- `small_cnn` (`models/best_cnn.keras`, paquete `inf8239_u02_cv` 0.1.0): Conv2D(32, 3×3) → MaxPool →
  Conv2D(64, 3×3) → MaxPool → GlobalAveragePooling → Dropout(0.25) → Dense(10, softmax). 19,466 parámetros.
- Referencia: `dense_baseline` (`models/dense_baseline.keras`): Flatten → Dense(64, ReLU) → Dense(10, softmax).
  50,890 parámetros.
- Entrenamiento: Adam, entropía cruzada categórica dispersa, lote 128, máximo 8 épocas,
  EarlyStopping (paciencia 2, restaura mejores pesos según `val_loss`), semilla 42.
- Autor: Roque Alexis Ventura Vallejo, octubre de 2026. Uso académico (INF-8239, U02.E04).

## Uso previsto
Ejercicio didáctico para comparar una red densa y una CNN en clasificación de imágenes en escala de
grises de 28×28 con 10 categorías de prendas, y para practicar evaluación por clase, análisis de errores
y medición de costo.

## Usos fuera de alcance
- Fotografías reales de ropa (color, fondo, pose, resolución distinta): no evaluado.
- Cualquier decisión sobre personas: imágenes médicas, OCR, vigilancia, identificación, moderación.
- Producción o comercio electrónico sin reentrenar y validar con datos del dominio real.

## Dataset y particiones
- Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017), licencia MIT, descargado con
  `tf.keras.datasets.fashion_mnist`.
- Entrenamiento: primeras 54,000 imágenes del conjunto oficial de entrenamiento.
  Validación: últimas 6,000 (partición fija, sin aleatoriedad). Prueba: 10,000 oficiales, usadas solo al final.
- Auditoría (`reports/audit.json`): 0 duplicados exactos dentro de cada partición y 0 imágenes
  compartidas entre particiones (hash MD5 de píxeles). Prueba balanceada (1,000 por clase);
  validación entre 555 (Sneaker) y 633 (Coat) por clase.

## Preprocesamiento
Píxeles `uint8` → `float32` en [0, 1] (división entre 255) y canal añadido: forma (28, 28, 1).
`validate_images` comprueba forma, rango, valores finitos y etiquetas en 0–9. Sin aumento de datos.

## Métricas globales y por clase
Conjunto de prueba, corrida principal de 8 épocas (`reports/cv_metrics.json`,
`reports/classification_reports.json`):

| Modelo | F1-macro | Accuracy |
|---|---|---|
| Baseline denso | 0.864 | 0.865 |
| CNN | 0.789 | 0.793 |

| Clase | F1 denso | F1 CNN | Recall CNN |
|---|---|---|---|
| T-shirt/top | 0.818 | 0.717 | 0.805 |
| Trouser | 0.974 | 0.959 | 0.929 |
| Pullover | 0.754 | 0.675 | 0.649 |
| Dress | 0.863 | 0.796 | 0.845 |
| Coat | 0.780 | 0.664 | 0.670 |
| Sandal | 0.951 | 0.916 | 0.883 |
| **Shirt** | 0.651 | **0.422** | **0.364** |
| Sneaker | 0.935 | 0.901 | 0.953 |
| Bag | 0.960 | 0.926 | 0.937 |
| Ankle boot | 0.951 | 0.915 | 0.896 |

Pares más confundidos por la CNN: Shirt → T-shirt/top (274), Pullover → Coat (159),
Shirt → Coat (135), Pullover → Shirt (133), Shirt → Pullover (128).

Curvas (`reports/training_curves.png`): en la CNN ambas pérdidas siguen bajando en la época 8 y la
accuracy de validación supera a la de entrenamiento (Dropout solo actúa al entrenar). Es subajuste,
no sobreajuste. Con 30 épocas (`reports/epochs30/`) la CNN llega a F1 0.848 y el denso a 0.875.

## Comparación de costo
- Hardware: Intel Core i7-1165G7 (11.ª gen., 2.8 GHz), 15.7 GB de RAM, sin GPU; Windows 11.
- Entorno: Python 3.12.13, TensorFlow 2.21.0 (CPU), Keras 3.15.1, scikit-learn 1.9.1.
- Parámetros: CNN 19,466; denso 50,890 (la CNN usa 2.6 veces menos).
- Tamaño de archivo `.keras`: CNN 262 KB; denso 619 KB.
- Tiempo de entrenamiento (8 épocas): CNN 66.9 s; denso 5.8 s (11.5 veces más para la CNN; entre 8.4 y 11.5
  veces en cuatro corridas).
- Tiempo de inferencia (10,000 imágenes, lote 256, mediana de 5 repeticiones tras calentamiento):
  CNN 0.055 ms/imagen; denso 0.012 ms/imagen. En la réplica del notebook: 0.036 y 0.009.
  La CNN fue entre 4 y 5 veces más lenta en CPU en todas las mediciones.

## Decisión técnica
Con este presupuesto, la CNN no justifica su costo: tiene menos parámetros y ocupa menos disco, pero
entrena unas 10 veces más lento, infiere entre 4 y 5 veces más lento en CPU y obtiene 7.5 puntos menos de F1-macro.
Para este benchmark se prefiere el baseline denso. La causa probable es la arquitectura: con
GlobalAveragePooling, solo 64 filtros y 8 épocas, la CNN no alcanza a aprender. Antes de descartar
las convoluciones habría que probar más épocas, una cabeza Flatten + Dense o más filtros, y medir
de nuevo el costo. Esa hipótesis no está evaluada en este repositorio.

## Limitaciones y riesgos
- Fashion-MNIST es un benchmark centrado, en escala de grises y con fondo limpio; un buen resultado
  no se transfiere a otros dominios.
- La clase Shirt es la más débil en ambos modelos (recall 0.364 en la CNN): se confunde con
  T-shirt/top, Coat y Pullover.
- Hay errores con confianza ≥ 0.92 (`reports/cnn_errors.png`), por ejemplo camisas anchas predichas
  como Bag. La probabilidad de salida no está calibrada y no debe leerse como certeza.
- Algunas imágenes parecen ambiguas o mal etiquetadas (índices 8742 y 2905 de prueba).
- Una sola semilla y una sola partición: no se reporta varianza entre corridas.

## Supervisión y monitoreo
- No usar sin revisión humana fuera del contexto académico.
- Antes de otro dominio: recolectar y etiquetar datos propios, rehacer la partición y la auditoría,
  y revisar métricas por clase, no solo la accuracy.
- Si se desplegara: vigilar la distribución de clases predichas y la tasa de baja confianza,
  muestrear errores para revisión y reentrenar cuando cambie la distribución de entrada.
