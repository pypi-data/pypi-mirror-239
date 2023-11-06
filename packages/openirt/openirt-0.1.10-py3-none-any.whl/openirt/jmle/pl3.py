import numpy as np
from item_models import Model, PL3


def estimate_ability_max_lik(
    params: np.ndarray,
    results: np.ndarray,
    end=1e-10,
    eps=1e-10,
    bounds=(-7, 7),
) -> np.ndarray:
    """
    Estimate abilities using maximum likelihood estimation.
    """
    params = np.array(params)
    results = np.array(results)
    
    est = 0
    prev_est = est + 2 * end
    i = 0
    while abs(est - prev_est) > end and i < 15:
        P = PL3.pl3_p(est, params)[0]
        Q = 1 - P
        
        P_2pm = PL3.pl2_p(est, params)[0]
        W = P * Q
        denom = -np.sum(params[0] ** 2 * W * (P_2pm / P) ** 2)

        num = np.sum(params[0] * W * ((results - P) / W) * (P_2pm / P))
        prev_est = est
        est = est - (num / denom)
        # consider setting est to bounds and not returning. 
        if est < bounds[0]:
            return bounds[0]
        elif est > bounds[1]:
            return bounds[1]
        i+=1
    return est


def estimate_item_params_max_lik(
    model: Model,
    ability: np.ndarray,
    result: np.ndarray,
    a_orig=3,
    b_orig=0.1,
    c_orig=0.1,
    end=1e-10,
    eps=1e-10,
) -> np.ndarray:
    """
    Estimate item parameters using maximum likelihood estimation.

    Parameters
    ----------
        model : Model
            Instance of PL3 model.
        ability : np.ndarray
            Array of abilities.
        result : np.ndarray
            Results. Each row is a different individual, each column is a
            different item.
        sigm_orig : float
            Initial value for the discrimination parameter.
        lamb_orig : float
            Initial value for the difficulty parameter.
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
     
    est = np.array([a_orig, b_orig, c_orig], dtype=float)
    prev_est = est + 2 * end
        
    while np.all(np.abs(prev_est - est) > end):
        P = PL3.pl3_p(ability, est.reshape((3, 1))).T[0]
        if np.any(np.abs(P - est[2]) < eps) or np.any(np.abs(P) < eps):
            P = P + 1e-10
        Q = 1 - P
        P_2pm = PL3.pl2_p(ability, est.reshape((3, 1))).T[0]

        L11 = -np.sum((ability - est[1]) ** 2 * P * Q * (P_2pm / P) ** 2)
        L12 = np.sum(est[0] * (ability - est[1]) * P * Q * (P_2pm / P))
        L13 = -np.sum((ability - est[1]) * (Q / (1 - est[2])) * (P_2pm / P))
        L22 = -est[0] ** 2 * np.sum(P * Q * (P_2pm / P))
        L23 = np.sum(est[0] * (Q / (1 - est[2])) * (P_2pm / P))
        L33 = -np.sum((Q / (1 - est[2])) / (P - est[2]) * (P_2pm / P))
        L = np.array([[L11, L12, L13], [L12, L22, L23], [L13, L23, L33]])

        if abs(np.linalg.det(L)) < eps:
            L += np.identity(3) * 1e-10
        L_inv = np.linalg.inv(L)

        L1 = np.sum((result - P) * (ability - est[1]) * (P_2pm / P))
        L2 = -est[0] * np.sum((result - P) * (P_2pm / P))
        L3 = np.sum((result - P) / (P - est[2]) * (P_2pm / P))
        obs_mat = np.array([L1, L2, L3])
        prev_est = est
        est = est - np.matmul(L_inv, obs_mat)

        # enforce bounds
        for par in range(model.num_params):
            est[par] = (
                model.param_bounds[par][0]
                if est[par] < model.param_bounds[par][0]
                else est[par]
            )
            est[par] = (
                model.param_bounds[par][1]
                if est[par] > model.param_bounds[par][1]
                else est[par]
            )
    return est
