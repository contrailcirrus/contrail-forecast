"""Utility functions."""

import functools
import pathlib
from typing import Any

import numpy as np
import pandas as pd
import scipy.stats
import yaml
from pycontrails import MetDataset
from pycontrails.models.cocip import habit_dirichlet
from pycontrails.models.cocipgrid import CocipGridParams
from pycontrails.models.ps_model import PSGrid
from pycontrails.physics import units
from scipy.stats.distributions import rv_frozen


@functools.cache
def load_configs() -> dict[str, Any]:
    """Read configs.yaml."""
    path = pathlib.Path(__file__).parent / "configs.yaml"
    with path.open() as fp:
        return yaml.safe_load(fp)


def create_source(time: np.datetime64) -> MetDataset:
    """Create CocipGrid source."""
    configs = load_configs()
    params = configs["source_params"]

    delta = params["horizontal_resolution"]
    longitude = np.arange(-180.0, 180.0, delta)
    latitude = np.arange(-80, 80.1, delta)

    flight_levels = params["flight_levels"]
    altitude_ft = np.array(flight_levels, dtype=np.float64) * 100.0
    level = units.ft_to_pl(altitude_ft)

    return MetDataset.from_coords(longitude, latitude, level, time)


@functools.cache
def load_distributions() -> dict[str, rv_frozen]:
    """Load model parameter distributions."""
    configs = load_configs()
    distributions = configs["distributions"]

    out = {}
    for key, details in distributions.items():
        name = details["name"]
        params = details["params"]

        if name == "habit_dirichlet":
            gen = habit_dirichlet
        else:
            gen = getattr(scipy.stats, name)

        rv = gen(**params)
        out[key] = rv

    return out


def create_cocip_grid_params(rng: np.random.Generator) -> CocipGridParams:
    """Create parameters for CocipGrid."""
    configs = load_configs()
    params = configs["cocip_grid_params"]

    rvs = load_distributions()
    distr = {key: distr.rvs(random_state=rng) for key, distr in rvs.items()}

    return CocipGridParams(
        dt_integration=pd.Timedelta(params["dt_integration"]).to_numpy(),
        max_age=pd.Timedelta(params["max_age"]).to_numpy(),
        met_slice_dt=pd.Timedelta(params["met_slice_dt"]).to_numpy(),
        target_split_size=params["target_split_size"],
        target_split_size_pre_SAC_boost=params["target_split_size_pre_SAC_boost"],
        max_altitude_m=params["max_altitude_m"],
        min_altitude_m=params["min_altitude_m"],
        azimuth=params["azimuth"],
        segment_length=params["segment_length"],
        dsn_dz_factor=params["dsn_dz_factor"],
        interpolation_use_indices=params["interpolation_use_indices"],
        interpolation_bounds_error=params["interpolation_bounds_error"],
        interpolation_q_method=params["interpolation_q_method"],
        downselect_met=params["downselect_met"],
        verbose_outputs_formation=params["verbose_outputs_formation"],
        filter_sac=params["filter_sac"],
        copy_source=params["copy_source"],
        show_progress=params["show_progress"],
        aircraft_performance=PSGrid(),
        **distr,
    )


def open_met() -> MetDataset:
    """Open pl_store Zarr store."""
    configs = load_configs()
    store = configs["era5_zarr"]["pl_store"]
    return MetDataset.from_zarr(store)


def open_rad() -> MetDataset:
    """Open sl_store Zarr store."""
    configs = load_configs()
    store = configs["era5_zarr"]["sl_store"]
    return MetDataset.from_zarr(store)
