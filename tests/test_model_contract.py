from pathlib import Path

import numpy as np
import pytest

tf = pytest.importorskip("tensorflow")
from inf8239_u02_cv.data import CLASS_NAMES
from inf8239_u02_cv.models import build_cnn, build_cnn_flatten, build_dense

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"


def assert_valid_probabilities(probabilities, n_rows):
    assert probabilities.shape == (n_rows, len(CLASS_NAMES))
    assert np.isfinite(probabilities).all()
    assert (probabilities >= 0).all()
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0, atol=1e-5)


@pytest.mark.parametrize("factory", [build_cnn, build_dense, build_cnn_flatten])
def test_model_output_contract(factory):
    model = factory(tf)
    batch = np.random.default_rng(42).random((4, 28, 28, 1), dtype="float32")
    assert_valid_probabilities(model(batch).numpy(), 4)


def test_cnn_output_contract():
    model = build_cnn(tf)
    probabilities = model(np.zeros((2, 28, 28, 1), dtype="float32")).numpy()
    assert probabilities.shape == (2, 10)
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0, atol=1e-5)


def test_parameter_budgets():
    dense, cnn, flatten = (f(tf).count_params() for f in (build_dense, build_cnn, build_cnn_flatten))
    assert cnn < dense
    assert abs(flatten - dense) / dense < 0.05  # comparación con presupuesto similar


@pytest.mark.parametrize("filename", ["dense_baseline.keras", "best_cnn.keras", "cnn_flatten.keras"])
def test_saved_model_contract(filename):
    path = MODELS_DIR / filename
    if not path.exists():
        pytest.skip(f"{filename} no existe; ejecute scripts/train_cv.py")
    model = tf.keras.models.load_model(path)
    batch = np.random.default_rng(0).random((3, 28, 28, 1), dtype="float32")
    assert_valid_probabilities(model.predict(batch, verbose=0), 3)
