import jax
import numpy as np

from nemos.basis import MSplineBasis
from nemos.glm import GLM


class DimensionMismatchError(Exception):
    """Exception raised for dimension mismatch errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def test_setup_msplinebasis():
    """
    Minimal test for MSplineBasis definition.

    Returns
    -------
    None

    Raises
    ------
    DimensionMismatchError
        If the output basis matrix has mismatched dimensions with the specified basis functions or window size.

    Notes
    -----
    This function performs a minimal test for defining the MBasis by generating basis functions using different orders.
    It checks if the output basis matrix has dimensions that match the specified number of basis functions and window size.
    """
    n_basis = 6
    window = 100
    for order in range(1, 6):
        spike_basis = MSplineBasis(n_basis_funcs=n_basis, order=order)
        spike_basis_matrix = spike_basis.evaluate(np.arange(window)).T
        if spike_basis_matrix.shape[0] != n_basis:
            raise DimensionMismatchError(
                f"The output basis matrix has {spike_basis_matrix.shape[1]} time points, while the number of basis specified is {n_basis}. They must agree."
            )

        if spike_basis_matrix.shape[1] != window:
            raise DimensionMismatchError(
                f"The output basis basis matrix has {spike_basis_matrix.shape[1]} window size, while the window size specified is {window}. They must agree."
            )


def test_run_end_to_end_glm():
    nn, nt = 10, 1000
    key = jax.random.PRNGKey(123)
    key, subkey = jax.random.split(key)
    spike_data = jax.random.bernoulli(subkey, jax.numpy.ones((nn, nt)) * 0.5).astype(
        "int64"
    )

    spike_basis = MSplineBasis(n_basis_funcs=6, order=3)
    spike_basis_matrix = spike_basis.evaluate(np.arange(100)).T
    model = GLM(spike_basis_matrix)

    model.fit(spike_data)
    model.predict(spike_data)
    key, subkey = jax.random.split(key)
    X = model.simulate(subkey, 20, spike_data[:, :100])
