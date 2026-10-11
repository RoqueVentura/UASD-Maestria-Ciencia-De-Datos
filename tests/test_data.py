import numpy as np
import pytest

from inf8239_u02_cv.data import (
    CLASS_NAMES,
    audit_splits,
    normalize_images,
    split_train_valid,
    validate_images,
)


def test_normalize_adds_channel_and_scales():
    raw = np.array([[[0] * 28] * 28, [[255] * 28] * 28], dtype=np.uint8)
    result = normalize_images(raw)
    assert result.shape == (2, 28, 28, 1)
    assert result.min() == 0
    assert result.max() == 1


def test_validate_rejects_wrong_shape():
    with pytest.raises(ValueError, match="Forma inesperada"):
        validate_images(np.zeros((2, 28, 28)), np.zeros(2))


def test_validate_rejects_values_outside_range():
    with pytest.raises(ValueError, match="normalizadas"):
        validate_images(np.full((2, 28, 28, 1), 255.0), np.zeros(2, dtype=int))


def test_validate_rejects_unknown_label():
    with pytest.raises(ValueError, match="rango de clases"):
        validate_images(np.zeros((2, 28, 28, 1)), np.array([0, len(CLASS_NAMES)]))


def test_there_are_ten_classes():
    assert len(CLASS_NAMES) == 10
    assert len(set(CLASS_NAMES)) == 10


def test_split_is_deterministic_and_disjoint():
    images = np.arange(20).reshape(20, 1)
    labels = np.arange(20)
    (x_train, _), (x_valid, _) = split_train_valid(images, labels, n_valid=5)
    assert len(x_train) == 15 and len(x_valid) == 5
    assert set(x_train.ravel()).isdisjoint(x_valid.ravel())
    (again, _), _ = split_train_valid(images, labels, n_valid=5)
    np.testing.assert_array_equal(x_train, again)


def test_audit_detects_overlap_between_splits():
    images = np.zeros((3, 28, 28, 1), dtype="float32")
    images[1] += 0.5
    images[2] += 0.25
    labels = np.array([0, 1, 2])
    audit = audit_splits({"a": (images[:2], labels[:2]), "b": (images[1:], labels[1:])})
    assert audit["overlap"]["a-b"] == 1
    assert audit["splits"]["a"]["class_counts"][:2] == [1, 1]


def test_real_dataset_contract():
    """Contrato sobre Fashion-MNIST real: tamaños de partición, forma, rango y 10 clases."""
    tf = pytest.importorskip("tensorflow")
    from inf8239_u02_cv.data import load_splits

    (x_train, y_train), (x_valid, y_valid), (x_test, y_test) = load_splits(tf)
    assert (len(x_train), len(x_valid), len(x_test)) == (54000, 6000, 10000)
    for images, labels in ((x_train, y_train), (x_valid, y_valid), (x_test, y_test)):
        assert images.shape[1:] == (28, 28, 1)
        assert images.dtype == np.float32
        assert 0.0 <= images.min() and images.max() <= 1.0
        assert set(np.unique(labels)) == set(range(len(CLASS_NAMES)))
