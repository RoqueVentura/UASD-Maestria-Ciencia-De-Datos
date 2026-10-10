from __future__ import annotations

import hashlib

import numpy as np

CLASS_NAMES = (
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
)
N_VALID = 6000


def normalize_images(images: np.ndarray) -> np.ndarray:
    values = images.astype("float32") / 255.0
    return values[..., None]


def validate_images(images: np.ndarray, labels: np.ndarray) -> None:
    if images.ndim != 4 or images.shape[1:] != (28, 28, 1):
        raise ValueError(f"Forma inesperada: {images.shape}")
    if len(images) != len(labels):
        raise ValueError("Imágenes y etiquetas no coinciden")
    if not np.isfinite(images).all() or images.min() < 0 or images.max() > 1:
        raise ValueError("Las imágenes deben estar normalizadas entre 0 y 1")
    if labels.min() < 0 or labels.max() >= len(CLASS_NAMES):
        raise ValueError("Etiquetas fuera del rango de clases")


def split_train_valid(images: np.ndarray, labels: np.ndarray, n_valid: int = N_VALID):
    """Partición fija: las últimas n_valid imágenes de entrenamiento forman validación."""
    return (images[:-n_valid], labels[:-n_valid]), (images[-n_valid:], labels[-n_valid:])


def load_splits(tf, n_valid: int = N_VALID):
    """Descarga Fashion-MNIST y devuelve (train, valid, test) normalizados y validados."""
    (x_train_all, y_train_all), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    (x_train, y_train), (x_valid, y_valid) = split_train_valid(
        normalize_images(x_train_all), y_train_all, n_valid)
    x_test = normalize_images(x_test)
    for images, labels in ((x_train, y_train), (x_valid, y_valid), (x_test, y_test)):
        validate_images(images, labels)
    return (x_train, y_train), (x_valid, y_valid), (x_test, y_test)


def _hashes(images: np.ndarray) -> list[str]:
    return [hashlib.md5(image.tobytes()).hexdigest() for image in images]


def audit_splits(splits: dict[str, tuple[np.ndarray, np.ndarray]]) -> dict:
    """Formas, rango, distribución de clases y duplicados exactos dentro y entre particiones."""
    audit: dict = {"splits": {}, "overlap": {}}
    hashes = {}
    for name, (images, labels) in splits.items():
        hashes[name] = _hashes(images)
        counts = np.bincount(labels, minlength=len(CLASS_NAMES))
        audit["splits"][name] = {
            "shape": list(images.shape),
            "dtype": str(images.dtype),
            "min": float(images.min()),
            "max": float(images.max()),
            "class_counts": counts.tolist(),
            "duplicates_within": len(hashes[name]) - len(set(hashes[name])),
        }
    names = list(splits)
    for i, first in enumerate(names):
        for second in names[i + 1:]:
            shared = set(hashes[first]) & set(hashes[second])
            audit["overlap"][f"{first}-{second}"] = len(shared)
    return audit
