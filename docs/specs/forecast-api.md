# Contrail Forecast API

## Table of Contents

- [Overview](#overview)
- [grids](#grids)
- [regions](#regions)

## Overview

This document specifies API endpoints for contrail forecast data
provided to air traffic planners in support of navigational contrail
avoidance systems.

At present, this document specifies two endpoints for general
availability.

1.  **grids**: The first endpoint surfaces gridded netCDF content at 0.25
    degree grid spacing, across standardized flight levels, on a one
    hour interval, at all longitudes and latitudes ranging from \[-80,
    80\] (this is expected to expand and encompass the poles, with an
    update at a later time). These grids are available across several
    [aircraft classes](#aircraft-classes).  The variable returned in the netCDF
    is `contrails`, a domain-agnostic quantity of arbitrary units,
    existing in the range of \[0, 4]\, `0` being a location with no contrail impact,
    and `4` being a location with severe contrail impact.  The value of `contrails`
    is intended to scale, roughly, with the CO2 equivalence of contrail impact, and by extension,
    the appropriate fuel investment for avoiding a given region.
    i.e. one should be willing to burn 2x as much fuel to avoid a location with `contrails` of `3`
    over a region with `contrails` of `1.5`.

2.  **regions**: The second endpoint surfaces *contrail avoidance
    regions* (aka polygons) served as geoJSON content, at the same
    flight levels and temporal intervals as the grid above. Regions are
    available at pre-defined `contrails` thresholds of \[1, 2, 3, 4\].

These endpoints are opinionated and intended (primarily) for
machine-to-machine integration. These two endpoints represent a minimal
yet complete set of capabilities for air traffic planners to explore and
prototype contrail avoidance in air traffic decision support systems.

The signature, behavior and design considerations of these two endpoints
are detailed below.

Future work may include adding a discovery/recommendation endpoint, to
help consumers map aircraft configuration attributes to a recommended
aircraft class. The materialization of such an endpoint requires
additional product discovery, and should not block or hinder adoption of
the endpoints currently in GA.

<div style="page-break-after: always;"></div>

## grids

The `v1/grids` route returns pre-rendered netCDF assets. The URI of the
specific asset is fully defined by the suffixed path parameters. This
endpoint effectively acts as a wrapper for content distribution of
static assets in cloud storage.

### signature

Request

```
GET /v1/grids/aircraft_class/{ac_id}/timestamp/{ts}/flight_level/{fl} HTTP/2
Host: {TBD}
Headers:
    x-api-key: {key}
```

Response

```
Headers:
    content-type: application/netcdf
    model_forecast_hour: <int>
    model_prediction_at: <%Y-%m-%dT%H:%M:%S>
    model_run_at: <%Y-%m-%dT%H:%M:%S>
```

### auth

The `{key}` passed in `x-api-key` is a static (no expiry) token.

### aircraft classes

`{ac_id}`, which defines the aircraft_class, is one of:

- `low_e`
- `default`
- `high_e`

These aircraft classes correspond to the following pairs of
representative aircraft type and engine configurations. See [Engberg et al 2024](https://egusphere.copernicus.org/preprints/2024/egusphere-2024-1361/)
for more details on the creation of these aircraft classes.

|   |   |
|:--|:--|
| `low_e`    | `aircraft_type_icao`: B789   |
|            | `engine_uid`: 01P17GE211     |
| `default`  | `aircraft_type_icao`: B738   |
|            | `engine_uid`: 01P11CM116     |
| `high_e`   | `aircraft_type_icao`: A320   |
|            | `engine_uid`: 01P10IA021     |

The `aircraft_class` values were chosen such that they be self-describing
and ordinal yet leave sufficient room for future expansion.

### timestamp

The `ts` value has the form `%Y%m%d%H`. This hour-resolution timestamp
represents the target time of the model prediction ("predicted_at"
time).

Given that ECMWF delivers 73 hours of forecast data every 6 hours, it is
expected that a given ts will have multiple candidate URIs to serve to a
client.

If multiple candidate URIs exist for a given timestamp at the time of
the client request, the API should return the URI whose outputs were
generated using the nearest forecast time.

### flight level

The fl value represents the flight level (*hectofeet*) of the returned
netCDF global grid.

The fl value must be one of the following:

\[270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400,
410, 420, 430, 440\]

### error handling

A 422 status code and informative message should be returned if:

- the provided flight level is not recognized
- the provided timestamp is malformed
- the provided aircraft class is not recognized

A 400 status code and informative message should be returned if:

- the request is properly formed and interpretable, but the requested resource does not exist

### response headers

The response header must populate the following values to contextualize the response data.
*Populating these headers is imperative since the behavior of the API is not idempotent given the
behavior mentioned above.*

- `model_run_at` (`<%Y-%m-%dT%H:%M:%S>`): The analysis time of the forecast.
  This is the same as the [*forecast_reference_time* as defined by CF conventions](https://confluence.ecmwf.int/display/COPSRV/Metadata+recommendations+for+encoding+NetCDF+products+based+on+CF+convention#MetadatarecommendationsforencodingNetCDFproductsbasedonCFconvention-3.3.1Analysistime:theforecastreferencetime).
- `model_prediction_at` (`<%Y-%m-%dT%H:%M:%S>`): The valid time of the model prediction,
  i.e. it is the same as the `<ts>` value passed in the API call,
  and the `time` of the data returned in the gridded netCDF.
  This is the same as the [*valid time* as defined by CF Conventions](https://confluence.ecmwf.int/display/COPSRV/Metadata+recommendations+for+encoding+NetCDF+products+based+on+CF+convention#MetadatarecommendationsforencodingNetCDFproductsbasedonCFconvention-3.3.3Validtime).
- `model_forecast_hour` (`<int>`): The difference, in hours, between `model_predicted_at` and `model_run_at`.
  It represents how far out the meteorological forecast is for a given model output.
  This is similar to the [*forecast period* as defined by CF Conventions](https://confluence.ecmwf.int/display/COPSRV/Metadata+recommendations+for+encoding+NetCDF+products+based+on+CF+convention#MetadatarecommendationsforencodingNetCDFproductsbasedonCFconvention-3.3.2Forecast:theforecastperiod).

### response object

The netCDF object returned from the API represents contrail climate
forcing in an arbitrary `contrails` unit, on a 0.25 degree by 0.25 degree basis, for
a given flight level. The longitude range extends around the entire
globe. The latitude range extends from 80N to 80S.

The data types for the coordinates and data variables are outlined
below:

```text
<xarray.Dataset> Size: 4MB
Dimensions:    (longitude: 1440, latitude: 641, flight_level: 1, time: 1)
Coordinates:
  * longitude  (longitude) float32 6kB -180.0 -179.75 -179.5 ... 179.5 179.75
  * latitude   (latitude) float32 3kB -80.0 -79.75 -79.5 ... 79.5 79.75 80.0
  * flight_level      (flight_level) int16 2B 300
  * time       (time) datetime64[ns] 8B 2024-07-01T12:00:00
Data variables:
    contrails   (longitude, latitude, flight_level, time) float32 4MB ...
Attributes:
    forecast_reference_time:  "2024-07-01T06:00:00Z"
    aircraft_class: "default"
```

Note that `forecast_reference_time` in the dataset level *Attributes* has the same definition as
`model_run_at` in the API response header.
See the [Forecast Data spec](forecast-data.md) for more info.

The `contrails` data variable has the following *Attributes*:

```text
<xarray.DataArray 'contrails' (longitude: 1440, latitude: 641, level: 1, time: 1)> Size: 4MB
[923040 values with dtype=float32]
Coordinates:
  * longitude  (longitude) float32 6kB -180.0 -179.8 -179.5 ... 179.5 179.8
  * latitude   (latitude) float32 3kB -80.0 -79.75 -79.5 ... 79.5 79.75 80.0
  * flight_level      (flight_level) int16 2B 270
  * time       (time) datetime64[ns] 8B 2024-07-01T12:00:00
Attributes:
    long_name:  'Contrail forcing index'
    units:      ''
    valid_min:  0
    valid_max:  4
```

<div style="page-break-after: always;"></div>

## regions

The `v1/regions` route returns pre-rendered geojson assets. The URI of the
specific asset is fully defined by the suffixed path parameters. This
endpoint effectively acts as a wrapper for content distribution of
static assets in cloud storage.

### signature

Request

```text
GET /v1/regions/aircraft_class/{ac_id}/timestamp/{ts}/flight_level/{fl}/threshold/{threshold} HTTP/2
Host: {TBD}
Headers:
    x-api-key: {key}
```

Response

```text
Headers:
    content-type: application/geo+json
    model_forecast_hour: <int>
    model_prediction_at: <%Y-%m-%dT%H:%M:%S>
    model_run_at: <%Y-%m-%dT%H:%M:%S>
```

### auth

Same as [grids.auth](#auth)

### aircraft classes

Same as [grids.aircraft_classes](#aircraft-classes)

### timestamp

Same as [grids.timestamp](#timestamp)

### flight level

Same as [grids.flight_level](#flight-level)

### threshold

The threshold value is the `contrails` value used in generating
the regions polygons.  A polygon of a given threshold will surround
a region of `contrails` values equal or greater than the threshold.

The threshold value provided by the client must be one of the following:
\[ 1, 2, 3, 4\]

### error handling

Same as [grids.error_handling](#error-handling)

## response headers
Same as [grids.response_headers](#response-headers)

### response object

The geoJSON object returned is a FeatureCollection, with the following
format:

```text
{
  "type": "FeatureCollection",
  "features": [
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "type": "MultiPolygon",
          "coordinates": []
        }
      }
  ]
}
```

Note that the `FeatureCollection` holds a single Feature.

The positions defined in the polygon coordinates include the third
optional value of altitude
([ref](https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.1))

e.g. \[165.5,63.12, 10363\]. The altitude value is in units of *meters*.

## Changelog

### 2024.10.09
- `/grids` endpoint updated to return a modified netCDF file, replacing the variable `ef_per_m` with the variable `contrails`,
and adding `forcast_reference_time` and `aircraft_class` to the netCDF global attributes.
- `/regions` endpoint updated to return geoJSON polygons rendered with a threshold based on `contrails` rather than `ef_per_m`
  - new supported threshold include `[1, 2, 3, 4]`
- `/regions` geoJSON response object format updated from `.features.*` to `.features[].*`.
