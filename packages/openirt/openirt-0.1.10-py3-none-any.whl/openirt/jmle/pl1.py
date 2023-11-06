import numpy as np
from item_models import Model, PL1
from jmle.pl2 import estimate_ability_max_lik as pl2_estimate_ability_max_lik


def estimate_ability_max_lik(
    params: np.ndarray,
    results: np.ndarray,
    end=0.00000001,
    eps=0.01,
    eps2=0.000001,
) -> np.ndarray:
    """
    Estimate abilities using the maximum likelihood method.
    See Model.estimate_ability_max_lik and PL2.estimate_ability_max_lik.
    """
    return pl2_estimate_ability_max_lik(
        [params[0], np.ones(len(params[0]))], results, end, eps, eps2
    )


def estimate_item_params_max_lik(
    model: Model,
    ability: np.ndarray,
    result: np.ndarray,
    end=1e-10,
    eps=1e-10,
) -> np.ndarray:
    """
    Estimate item parameters using maximum likelihood estimation.

    Parameters
    ----------
        model : Model
            Instance of PL1 model.
        ability : np.ndarray
            Array of abilities.
        result : np.ndarray
            Results. Each row is a different individual, each column is a
            different item.
        end : float
            Convergence threshold.
        eps : float
            Threshold for detecting a near-singular matrix.

    Returns
    -------
        np.ndarray
            Array of item parameters.
    """
    ability = np.array(ability)
    result = np.array(result)
    est = model.prov_params[0]
    prev_est = est + 2 * end
    while abs(est - prev_est) > end:
        P = PL1.pl1_p(ability, [[est]]).transpose()[0]
        L1 = np.sum(P - result)
        L2 = -np.sum(P * (1 - P))
        if abs(L2) < eps:
            L += 1e-10
        prev_est = est
        est = est - L1 / L2
        
        # enforce bounds
        est = model.param_bounds[0][0] if est < model.param_bounds[0][0] else est
        est = model.param_bounds[0][1] if est > model.param_bounds[0][1] else est
    return np.array([est])
