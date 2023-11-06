from pathlib import Path
import sys

if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from item_models import Model, PL1, PL2, PL3, Norm
import numpy as np
import jmle.pl1 as pl1
import jmle.pl2 as pl2
import jmle.pl3 as pl3


def estimate_ability_max_lik(
    model: Model, params: np.ndarray, results: np.ndarray, **kwargs: dict
) -> np.ndarray:
    if isinstance(model, PL1):
        return pl1.estimate_ability_max_lik(params, results, **kwargs)
    if isinstance(model, PL2):
        return pl2.estimate_ability_max_lik(params, results, **kwargs)
    if isinstance(model, PL3):
        return pl3.estimate_ability_max_lik(params, results, **kwargs)
    raise NotImplementedError(
        "Cannot estimate ability using maximum liklihood estimation for given model."
    )


def estimate_item_params_max_lik(
    model: Model,
    ability: np.ndarray,
    result: np.ndarray,
    **kwargs,
) -> np.ndarray:
    if isinstance(model, PL1):
        return pl1.estimate_item_params_max_lik(model, ability, result, **kwargs)
    if isinstance(model, PL2):
        return pl2.estimate_item_params_max_lik(model, ability, result, **kwargs)    
    if isinstance(model, PL3):
        return pl3.estimate_item_params_max_lik(model, ability, result, **kwargs)
    raise NotImplementedError(
        "Cannot estimate parameters using maximum liklihood estimation for given model."
    )

def log_likelihood(model, responses, abilities, params):
    p = model.p(abilities, params).reshape(responses.shape[0])
    p[p < 1e-10] = 1e-10
    p[p > 1 - 1e-10] = 1 - 1e-10
    return np.sum(np.log(p) * responses + np.log(1 - p) * (1 - responses))


def jmle(
    model: Model,
    responses: np.ndarray,
    eps: float = 0.1,
    max_iterations: int = 1000,
) -> tuple:
    """
    Estimate abilities and item parameters using the EM algorithm with
    joint maximum liklihood estimation.

    Parameters
    ----------
        responses : np.ndarray
            Responses to items. Each row is a different subject, each
            column is a different item.
        eps : float
            Convergence threshold.
        max_iterations : int, optional
            Maximum number of iterations. Defaults to 1000.

    Returns
    -------
        np.ndarray
            Estimated abilities
        np.ndarray
            Estimated item parameters. Each column is a different item,
            each row is a different parameter.
    """
    responses = np.array(responses)
    subjects, items = responses.shape
    
    
    
    abilities = np.sum(responses, axis=1)
    abilities = (abilities - np.mean(abilities)) / np.std(abilities)
    prev_abilities = abilities + 2 * eps
    iteration = 0

    # params = np.array(model.prov_params)
    for i in range(10):
        params = np.array(
            [
                estimate_item_params_max_lik(model, abilities, responses[:, i])
                for i in range(items)
            ]
        ).T
        
        abilities = []
        for i in range(subjects):
            abilities.append(estimate_ability_max_lik(model, params, responses[i]))
        abilities = np.array(abilities)
        # abilities = (abilities - np.mean(abilities)) / np.std(abilities)
        # print(f'params: {params}')
        # print(f'abilities: {abilities}')
        # print(f'likelihood: {likelihood(model, responses, abilities, params)}')
        # print()
    print('done')
    return abilities, params
    while (
        np.any(np.abs(abilities - prev_abilities) > eps) and iteration < max_iterations
    ):
        print(1)
        params = np.array(
            [
                estimate_item_params_max_lik(model, abilities, responses[:, i])
                for i in range(items)
            ]
        ).T
        prev_abilities = abilities
        print(2)

        abilities = []
        for j in range(subjects):
            print(params, responses[j])
            abilities.append(estimate_ability_max_lik(model, params, responses[j]))
        abilities = np.array(abilities)
        iteration += 1
    return abilities, params
