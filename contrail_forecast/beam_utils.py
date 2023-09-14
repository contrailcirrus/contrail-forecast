"""Utility functions for running contrail forecast pipeline in Beam."""

import apache_beam as beam
import numpy as np
from typing import Iterable
import utils
import xarray as xr
from pycontrails.models.cocipgrid import CocipGrid

def _fix_attrs(ds: xr.Dataset) -> xr.Dataset:
    """Ensure the attributes are serializable via xr.Dataset.to_netcdf()."""
    for k, v in ds.attrs.items():
        if v is None:
            ds.attrs[k] = "none"
        elif isinstance(v, np.generic):
            ds.attrs[k] = v.item()
    return ds


def eval_task(t: np.datetime64, seed: int) -> Iterable[tuple[str, xr.Dataset]]:
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
    ds = _fix_attrs(ds)

    yield str(t), ds


def run_cocipgrid(root: beam.Pipeline) -> beam.Pipeline:
    """Run CocipGrid on a set of times, including Monte Carlo rollouts."""
    # TODO: Generate the tasks dynamically
    t = np.datetime64("2023-05-07T09:00:00")

    rng = np.random.default_rng(None)
    n_rollouts = utils.load_configs()["monte_carlo"]["n_rollouts"]
    seeds = rng.integers(0, 2**32, size=n_rollouts)

    rollout_inputs = [(t, seed) for seed in seeds]

    # TODO: you might have to something to make sure the configs are
    # sent to the workers properly. One option is to load them here
    # and pass them as a "side input" to the eval_task function
    return (
        root
        | "CreateSeeds" >> beam.Create(rollout_inputs)
        | "Evaluate" >> beam.FlatMapTuple(eval_task)
    )