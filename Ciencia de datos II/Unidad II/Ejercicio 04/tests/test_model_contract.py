import numpy as np
import pytest

tf = pytest.importorskip("tensorflow")
from inf8239_u02_cv.data import CLASS_NAMES
from inf8239_u02_cv.models import build_cnn, build_dense


@pytest.mark.parametrize("factory", [build_cnn, build_dense])
def test_model_output_contract(factory):
    model = factory(tf)
    batch = np.random.default_rng(42).random((4, 28, 28, 1), dtype="float32")
    probabilities = model(batch).numpy()
    assert probabilities.shape == (4, len(CLASS_NAMES))
    assert np.isfinite(probabilities).all()
    assert (probabilities >= 0).all()
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0, atol=1e-5)


def test_cnn_output_contract():
    model = build_cnn(tf)
    probabilities = model(np.zeros((2, 28, 28, 1), dtype="float32")).numpy()
    assert probabilities.shape == (2, 10)
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0, atol=1e-5)


def test_cnn_has_fewer_parameters_than_dense():
    assert build_cnn(tf).count_params() < build_dense(tf).count_params()
