# Copyright (c) 2020 Jon Thielen.
# Distributed under the terms of the Apache 2.0 License.
# SPDX-License-Identifier: Apache-2.0
"""
Shared GRIB Handling Utils
--------------------------

"""

import re

import cfgrib
from metpy.units import units

 
def open_datasets(filepath_template, **kwargs):
    """Open collection of datasets from grib file defined by template and args."""
    return cfgrib.open_datasets(
        filepath_template.format(**kwargs),
        backend_kwargs={'indexpath': ''}
    )


def search_variable_all(datasets, attributes=None, coords=None):
    """Search for all variables matching intersection of attribute and coord regexes."""
    coords = [] if coords is None else coords
    attributes = {} if attributes is None else attributes
    attributes_compiled = {
        attribute: re.compile(pattern)
        for attribute, pattern in attributes.items()
    }
    coords_compiled = [re.compile(coord_pattern) for coord_pattern in coords]

    results = []
    for ds in datasets:
        for var in ds.data_vars.values():
            # Attribute pattern full matches
            attr_match = all(
                bool(prog.fullmatch(var.attrs.get(attribute, None)))
                for attribute, prog in attributes_compiled.items()
            )
            coord_match = all(
                any(bool(prog.fullmatch(coord)) for coord in var.coords)
                for prog in coords_compiled
            )
            if attr_match and coord_match:
                results.append(var)
    return results


def search_variable_unique(datasets, attributes=None, coords=None):
    """Search for a unique variable matching intersection of attribute and coord regexes."""
    results = search_variable_all(datasets, attributes, coords)
    if len(results) == 0:
        raise RuntimeError("Requested variable not found in GRIB file.")
    elif len(results) > 1:
        raise RuntimeError("More than one variable matching request found in GRIB file.")
    return results[0]


def search_dataset_all(datasets, attributes=None, coords=None):
    """Search for a dataset matching intersection of attribute and coord regexes."""
    coords = [] if coords is None else coords
    attributes = {} if attributes is None else attributes
    attributes_compiled = {
        attribute: re.compile(pattern)
        for attribute, pattern in attributes.items()
    }
    coords_compiled = [re.compile(coord_pattern) for coord_pattern in coords]

    results = []
    for ds in datasets:
        # Attribute pattern full matches
        attr_match = all(
            bool(prog.fullmatch(ds.attrs.get(attribute, None)))
            for attribute, prog in attributes_compiled.items()
        )
        coord_match = all(
            any(bool(prog.fullmatch(coord)) for coord in ds.coords)
            for prog in coords_compiled
        )
        if attr_match and coord_match:
            results.append(ds)
    return results


def metpy_parse_variable(da):
    """
    Given a DataArray of a variable from cfgrib, add nice coordinate from MetPy.
    
    Right now only works with LCC projections
    """
    return da.metpy.assign_crs(
        grid_mapping_name='lambert_conformal_conic',
        longitude_of_central_meridian=da.attrs["GRIB_LoVInDegrees"],
        latitude_of_projection_origin=da.attrs["GRIB_LaDInDegrees"],
        standard_parallel=(
            da.attrs["GRIB_Latin1InDegrees"],
            da.attrs["GRIB_Latin2InDegrees"]
        )
    ).metpy.assign_y_x(tolerance=5 * units.km)
