"""Utility functions for running contrail forecast pipeline in Beam."""

import apache_beam as beam
import numpy as np
from typing import Any, Iterable
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


class CocipGridFn(beam.DoFn):
    """Runs CocipGrid on a single set of inputs."""

    def __init__(self, configs: dict[str, Any]):
        # If weather is opened with a cache, it will persist until the worker
        # dies. Make sure weather is loaded lazily, though! This is run by the
        # manager, and the serialized DoFn is sent to the workers as a "starting
        # point."
        self.met = utils.open_met()
        self.rad = utils.open_rad()
    
    def process(self, indata: tuple[np.datetime64, int]) -> Iterable[tuple[str, xr.Dataset]]:
        """Evaluates the task. `indata` should be a tuple of (timestamp, seed)."""
        t, seed = indata
        rng = np.random.default_rng(seed)
        params = utils.create_cocip_grid_params(rng)

        model = CocipGrid(self.met, self.rad, params)

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
    configs = utils.load_configs()
    n_rollouts = configs["monte_carlo"]["n_rollouts"]
    seeds = rng.integers(0, 2**32, size=n_rollouts)

    rollout_inputs = [(t, seed) for seed in seeds]

    # TODO: you might have to something to make sure the configs are
    # sent to the workers properly. One option is to load them here
    # and pass them as a "side input" to the eval_task function
    return (
        root
        | "CreateSeeds" >> beam.Create(rollout_inputs)
        | "Evaluate" >> beam.ParDo(CocipGridFn(configs))
    )