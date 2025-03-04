# Contrail Forecast Data

This document species the data contract for contrail forecast data.
This data is intended to be served by the interface defined in the sibling specification [Forecast API](forecast-api.md).

## Format

Data is designed to be stored in either a `netCDF4` or `zarr` format.
This document assumes data is stored in a `netCDF4` format.

## Domain

Forecast must be globally valid for each `forecast_reference_time`.

## Global Attributes

- (optional) `aircraft_class` (`str`): Aircraft class for forecast.
One of \[`"low_e"`, `"default"`, `"high_e"`\], where suffix `_e` references *emissions*.[^emissions]
- (optional) `model` (`str`): A descriptor of the model used in generating the `contrails` variable.

Additional attributes, in addition to the required and suggested ones above, may be added at the author's discretion.

## Dimensions

- `longitude` (`float32`): `np.arange(-180, 180, 0.25)`, EPSG:4326
- `latitude` (`float32`): `np.arange(-90, 90, 0.25)`, EPSG:4326
- `flight_level` (`int16` or `int32`): `[270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440]`, hectofeet [^flightlevels]
- `time` (`int32` or `int64`): [CF compatible time coordinates](https://cfconventions.org/cf-conventions/cf-conventions#time-coordinate). See [time dimensions](#time-dimensions) for more details.
- `forecast_reference_time` (`int32` or `int64`): [CF compatible time coordinates](https://cfconventions.org/cf-conventions/cf-conventions#time-coordinate). The forecast reference time is the "data time", i.e. the time at which the meteorological model was executed for each forecast `time` value. See [*forecast_reference_time* as defined by CF conventions](https://confluence.ecmwf.int/display/COPSRV/Metadata+recommendations+for+encoding+NetCDF+products+based+on+CF+convention#MetadatarecommendationsforencodingNetCDFproductsbasedonCFconvention-3.3.1Analysistime:theforecastreferencetime). See [time dimensions](#time-dimensions) for more details.

### Time dimensions

[CF conventions](https://cfconventions.org/cf-conventions/cf-conventions#time-coordinate) require
both `time` and `forecast_reference_time` have `units` and `calendar` variable attributes, e.g.:

```
units: hours since 2022-12-12
calendar: proleptic_gregorian
```

When reading or writing netCDF files with [xarray](https://docs.xarray.dev/en/stable), `xarray`
automatically decodes/encodes datetime arrays using CF conventions
When reading, `xarray` will decode datetime arrays directly into a `np.datetime64` array and hide the
`units` and `calendar` attributes.
When writing, `xarray` uses the `'proleptic_gregorian'` calendar and `units` of the smallest
time difference between values, with a reference time of the first time value.
See [xarray Time Units](https://docs.xarray.dev/en/stable/user-guide/io.html#time-units) for more information.

Its valid to write `time` and `forecast_reference_time` as unix time integers, but
`units` must still be specified as `"seconds since 1970-01-01 00:00:00"`.
`calendar` attribute may still be specified to define the set of dates (year-month-day combinations) which are permitted.

## Variables

- `contrails` (`float32`): (longitude, latitude, flight_level, time) Continuous contrail forcing index values from [0 - 4] [^contrailindex]
	- Attributes:
		- `units`: ""
		- `long_name`: Contrail forcing index
		- `valid_min`: 0 (*NB: Could be extended in the future to -4 to support cooling contrails*)
		- `valid_max`: 4

## Example

- See [example NetCDF forecast here](https://drive.google.com/file/d/1NQweF1pOrJH8RBKcdqgWzTfzD_IepO0I/view?usp=sharing)

Example scaling translates `ef_per_m` [^efinterpretation] to `contrails`  index via:

```
ds["contrails"] = ds["ef_per_m"].clip(min=1e7, max=2e9)
ds["contrails"] = ((ds["contrails"] - 1e7) / (2e9 - 1e7)) * 4
```

## Test

- [ ] Establish benchmark datasets for *substantially equivalent* data distributions
- [ ] Share 1 day of input data per quarter for validation exercise

## Implementation

- [ ] Add examples of cost function implementation

## References

- [NetCDF Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/cf-conventions/cf-conventions)
- [xarray: Reading and writing files](https://docs.xarray.dev/en/stable/user-guide/io.html)
- [Engberg et al 2024](https://egusphere.copernicus.org/preprints/2024/egusphere-2024-1361/)
- [weather.gov Turbulence](https://www.weather.gov/source/zhu/ZHU_Training_Page/turbulence_stuff/turbulence/turbulence.htm#:~:text=TURBULENCE%20INTENSITY,attitude%20or%20a%20slight%20bumpiness)
- [api.contrails.org Energy Forcing Interpretation](https://apidocs.contrails.org/ef-interpretation.html)


[^emissions]: See [Engberg et al 2024](https://egusphere.copernicus.org/preprints/2024/egusphere-2024-1361/) for details on aircraft classes. Each aircraft class maps to a specific aircraft type + engine UID combination:

	| Class label | Aircraft type icao | Engine UID |
	|---|---|---|
	| `low_e` (low emissions) | `B789` | `01P17GE211` |
	| `default` | `B738` | `01P17GE211` |
	| `high_e` (high emissions) | `A320` | `01P10IA021` |

[^flightlevels]: Flight levels are converted symmetrically to pressure levels using `pycontrails.physics.units.ft_to_pl()`

[^contrailindex]: Influenced by turbulence forecasts

	- 0: None
	- 1: Low (Light)
	- 2: Moderate
	- 3: High (Severe)
	- 4: Extreme

	For turbulence, 1 and 2 are generally carrier choice, while 3 and 4 are generally ANSP mandated.

[^efinterpretation]: See [Energy Forcing Interpretation](https://apidocs.contrails.org/ef-interpretation.html) for background informing example mapping from `ef_per_m` to `contrails` index.

## Changelog
