# Copyright (c) 2020 Jon Thielen.
# Distributed under the terms of the Apache 2.0 License.
# SPDX-License-Identifier: Apache-2.0
"""
Shared Plotting Utils
---------------------
"""

import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

from metpy.plots import USCOUNTIES, USSTATES

from .vendor.metpy import _areas

os.environ["PYART_QUIET"] = "1"
from pyart.graph import cm_colorblind  # noqa: I100


def single_panel_with_colorbar(config, projection):
    """Create a default single geographic map with colorbar."""
    fig = plt.figure(figsize=config["single_panel"]["figsize"])
    gs = gridspec.GridSpec(
        3,
        2,
        figure=fig,
        width_ratios=config["single_panel"]["width_ratios"],
        height_ratios=[0.2, 0.6, 0.2]
    )
    ax = plt.subplot(gs[:, 0], projection=projection)
    cax = plt.subplot(gs[1, 1])
    
    return fig, ax, cax


def set_extent_max_min_x_y(ax, da):
    """Set extent off of max and min MetPy's identified x and y coords."""
    ax.set_extent([
        da.metpy.x.data.min(),
        da.metpy.x.data.max(),
        da.metpy.y.data.min(),
        da.metpy.y.data.max()
    ], crs=da.metpy.cartopy_crs)


def set_extent_by_area_code(ax, code):
    """Set extent based on pre-identified code from MetPy."""
    ax.set_extent(_areas[code], crs=ccrs.PlateCarree())


def add_boundaries(ax):
    """Add default county, state, and coastline boundaries."""
    ax.add_feature(USCOUNTIES.with_scale('20m'), edgecolor=(0, 0, 0, 0.05), zorder=10)
    ax.add_feature(USSTATES.with_scale('20m'), edgecolor=(0, 0, 0, 0.9), zorder=0)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor=(0, 0, 0, 0.9), zorder=0)


cmaps = {
    "radar": cm_colorblind.HomeyerRainbow,
    "precip": "YlGnBu"
}
