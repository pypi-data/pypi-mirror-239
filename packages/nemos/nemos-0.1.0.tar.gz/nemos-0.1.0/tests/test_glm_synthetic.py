import matplotlib

matplotlib.use("agg")

import itertools

import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as onp

import nemos as nmo
from nemos.basis import RaisedCosineBasisLinear
from nemos.glm import GLM


def test_set_up_glm():
    """Test the setup of the Generalized Linear Model (GLM).

    Returns
    -------
    GLM
        The simulated model of the Generalized Linear Model.

    Notes
    -----
    This function performs the setup for the Generalized Linear Model (GLM) by creating the necessary objects and variables.
    It generates a raised cosine basis, defines the simulated model using the basis functions, and returns the GLM object.
    """
    nn, nt, ws = 2, 1000, 100
    simulation_key = jax.random.PRNGKey(123)

    spike_basis = RaisedCosineBasisLinear(n_basis_funcs=5)

    B = spike_basis.evaluate(onp.linspace(0, 1, ws)).T

    w0 = onp.array([-0.1, -0.1, -0.2, -0.2, -1])
    w1 = onp.array([0, 0.1, 0.5, 0.1, 0])

    W = onp.empty((2, 5, 2))
    for i, j in itertools.product(range(nn), range(nn)):
        W[i, :, j] = w0 if (i == j) else w1

    simulated_model = GLM(B)


def test_fit_glm2():
    jax.config.update("jax_platform_name", "cpu")
    jax.config.update("jax_enable_x64", True)

    nn, nt, ws = 2, 1000, 100
    simulation_key = jax.random.PRNGKey(123)

    spike_basis = RaisedCosineBasisLinear(n_basis_funcs=5)

    B = spike_basis.evaluate(onp.linspace(0, 1, ws)).T

    w0 = onp.array([-0.1, -0.1, -0.2, -0.2, -1])
    w1 = onp.array([0, 0.1, 0.5, 0.1, 0])

    W = onp.empty((2, 5, 2))
    for i, j in itertools.product(range(nn), range(nn)):
        W[i, :, j] = w0 if (i == j) else w1

    simulated_model = GLM(B)
    simulated_model.spike_basis_coeff_ = jnp.array(W)
    simulated_model.baseline_log_fr_ = jnp.ones(nn) * 0.1

    init_spikes = jnp.zeros((2, ws))
    spike_data = simulated_model.simulate(simulation_key, nt, init_spikes)
    sim_pred = simulated_model.predict(spike_data)

    fitted_model = GLM(
        B,
        solver_name="GradientDescent",
        solver_kwargs=dict(maxiter=1000, acceleration=False, verbose=True, stepsize=-1),
    )

    fitted_model.fit(spike_data)
    fit_pred = fitted_model.predict(spike_data)

    fig, axes = plt.subplots(2, 1)
    axes[0].plot(onp.arange(nt), spike_data[0])
    axes[0].plot(onp.arange(ws, nt + 1), sim_pred[0])
    axes[0].plot(onp.arange(ws, nt + 1), fit_pred[0])
    axes[1].plot(onp.arange(nt), spike_data[1])
    axes[1].plot(onp.arange(ws, nt + 1), sim_pred[1])
    axes[1].plot(onp.arange(ws, nt + 1), fit_pred[1])

    fig, axes = plt.subplots(nn, nn, sharey=True)
    for i, j in itertools.product(range(nn), range(nn)):
        axes[i, j].plot(B.T @ simulated_model.spike_basis_coeff_[i, :, j], label="true")
        axes[i, j].plot(B.T @ fitted_model.spike_basis_coeff_[i, :, j], label="est")
        axes[i, j].axhline(0, dashes=[2, 2], color="k")
    axes[-1, -1].legend()
    plt.close("all")
