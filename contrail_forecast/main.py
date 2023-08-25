"""Prototype for the contrail forecast model pipeline."""

import numpy as np
import utils
from pycontrails.models.cocipgrid import CocipGrid


def eval_task(t: np.datetime64, seed: int) -> None:
    """Evaluate the task.

    Should be run in some data processing pipeline.    
    """
    met = utils.open_met()
    rad = utils.open_rad()

    rng = np.random.default_rng(seed)
    params = utils.create_cocip_grid_params(rng)

    model = CocipGrid(met, rad, params)

    source = utils.create_source(t)
    mds = model.eval(source)
    ds = mds.data
    ds.attrs["seed"] = seed

    # TODO: save ds somewhere


def main() -> None:
    """Orchestrate the tasks."""
    # TODO: Generate the tasks dynamically
    t = np.datetime64("2023-05-07T09:00:00")

    rng = np.random.default_rng(None)
    n_rollouts = utils.load_configs()["monte_carlo"]["n_rollouts"]
    seeds = rng.integers(0, 2**32, size=n_rollouts)

    for seed in seeds:
        eval_task(t, seed)


if __name__ == "__main__":
    main()
