from __future__ import annotations

from pathlib import Path
from statistics import median, pstdev
from time import perf_counter

import numpy as np
from sklearn.metrics import confusion_matrix

from inf8239_u02_cv.data import CLASS_NAMES


def measure_inference(model, images: np.ndarray, repeats: int = 5, batch_size: int = 256) -> dict:
    """Tiempo de inferencia sobre el mismo lote, con una pasada de calentamiento."""
    model.predict(images[:batch_size], batch_size=batch_size, verbose=0)
    runs = []
    for _ in range(repeats):
        start = perf_counter()
        model.predict(images, batch_size=batch_size, verbose=0)
        runs.append(1000 * (perf_counter() - start) / len(images))
    return {"median_ms_per_image": median(runs), "std_ms_per_image": pstdev(runs),
            "repeats": repeats, "batch_images": len(images)}


def top_confusions(y_true: np.ndarray, y_pred: np.ndarray, k: int = 5) -> list[dict]:
    """Pares (real, predicha) con más errores."""
    matrix = confusion_matrix(y_true, y_pred, labels=range(len(CLASS_NAMES)))
    np.fill_diagonal(matrix, 0)
    order = np.dstack(np.unravel_index(np.argsort(matrix, axis=None)[::-1], matrix.shape))[0]
    return [{"true": CLASS_NAMES[i], "pred": CLASS_NAMES[j], "count": int(matrix[i, j])}
            for i, j in order[:k]]


def file_size_kb(path: Path) -> float:
    return Path(path).stat().st_size / 1024
