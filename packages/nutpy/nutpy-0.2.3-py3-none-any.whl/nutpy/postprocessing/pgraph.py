import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy import units as u
from astropy_healpix import HEALPix
import os

import nutpy.numeric as nm

from nutpy.constants import plot_options


def plot_map(data, cbarlabel, N):
    """
    Plot temporal analysis results

    Parameters
    ----------
    data : 1D-array
        Data to plot (value per pixel for Healpix scheme))
    cbarlabel : str
        Label for the colorbar
    N : int
        Size of plotting mesh (2NxN)
    cbar_size : float
        Size of the colorbar
    projection_type : str
        Type of projection (Hammer, mollweide or orthographic)

    Returns
    -------
    fig :  matplotlib figure
        Plotted figure
    """

    cbar_size = plot_options["cbar_size"]
    projection = plot_options["projection"]
    print(projection)

    lon = np.linspace(-180.0, 180.0, 2 * N) * u.deg
    lat = np.linspace(-90.0, 90.0, N) * u.deg
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    npix = len(data)
    hp = HEALPix(nside=int(np.sqrt(npix / 12)))

    map_plot = data[hp.lonlat_to_healpix(lon_grid.ravel(), lat_grid.ravel())]

    map_plot = map_plot.reshape((N, 2 * N))

    fig = plt.figure()

    ax = plt.axes(projection=projection)
    yaxis = True

    lon_grid_plot = lon_grid.to(u.radian).value
    lat_grid_plot = lat_grid.to(u.radian).value

    im = ax.pcolormesh(
        lon_grid_plot,
        lat_grid_plot,
        map_plot,
        cmap=plt.cm.jet,
        rasterized=True,
        shading="auto",
    )

    cbar = plt.colorbar(im, fraction=cbar_size)

    cbar.set_label(cbarlabel)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(yaxis)

    return fig


def plot_focal_plane(
    xd, yd, r, cases_dict=None, case_id=None, quantity="Viewed", numbered=False
):
    """
    Plots focal plane results for a given case

    Parameters
    ----------
    xd : float
        X coordinates of detectors in focal plane
    yd : float
        Y coordinates of detectors in focal plane
    nd : int
        Number of detectors
    r : float
        Half-angle of the detector fov (degrees)
    cases_dict : dict
        Temporal results for point in the sky
    case_id : str
        Id of case to be plotted
    quantity : str
        Quantity to be shown
    numbered : bool
        If True, sensors Id is plotted

    Returns
    -------
    fig : matplotlib figure
        Figure of profile
    ax : axes
        Matplotlib figure axes of sensor array and FOV
    """

    fig, ax = plt.subplots(figsize=(10, 10))

    nd = len(xd)

    if case_id is None:
        sensor_data = np.zeros(nd)
        vmin_mod = 0
    else:
        case_df = cases_dict[case_id]

        sensor_data = case_df[quantity].values

        if quantity == "Viewed" and sensor_data.min() == 1:
            vmin_mod = 0
        else:
            vmin_mod = 1

    ax.set_aspect("equal", "box")

    cmap = matplotlib.cm.get_cmap("viridis")

    vmin = sensor_data.min() * vmin_mod
    vmax = sensor_data.max()

    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

    for i in range(nd):
        a_circle = plt.Circle((xd[i], yd[i]), r, color=cmap(norm(sensor_data[i])))
        ax.add_artist(a_circle)
        ax.text(
            xd[i],
            yd[i],
            str(i),
            fontsize=7,
            color="w",
            horizontalalignment="center",
            verticalalignment="center",
        )

    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(np.cos(t), np.sin(t))

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    if case_id is None:
        pass
    else:
        plt.colorbar(sm)

    ax.set_axis_off()

    return fig, ax


def plot_trace(SSP, Tsim, dT):
    """
    Plots trace of the instrument over the sky (orthographic projection over the
    XZ-plane)

    Parameters
    ----------
    SSP : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/
        (deg, deg, min, min)
    Tsim : float
        Total time considered
    dT : float
        Step time used

    Returns
    -------
    fig : matplotlib figure
        Figure of profile
    ax : axes
        Matplotlib figure axes of sensor array and FOV
    """

    N = int(Tsim / dT)
    time = np.linspace(0, Tsim, N)
    u = nm.u_trace(time, SSP)

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.plot(u[:, 0], u[:, 2])

    return fig, ax


def plot_double_results(
    x,
    y1,
    y2,
    tag=None,
    legend=None,
    xlabel="X-axis",
    ylabel="Y-axis (1)",
    grid=True,
    file_path="Results/Figures/",
    dpi=300,
    save=False,
    fmt="jpg",
):
    """
    Plots two sets of data (y1, y2) versus the same x as lines in the same axes

    Parameters
    ----------
    x : 1D-array
        Horizontal coordinates of the data points
    y1 : 1D-array
        Vertical coordinates of the first set of data points
    y2 : 1D-array
        Vertical coordinates of the second set of data points
    tag : str
        Name of the picture file
    legend : str
        Legend of data sets
    loc : int
        Location of the legend whitin the plot
    xlabel : str
        Label of the X-axis
    ylabel : str
        Label of the Y-axis
    grid : bool
        If True, grid is plotted
    same_grid : bool
        If True, ticks of both Y-axis are adjusted to share the grid
    file_path : str
        Path to the folder where to save the picture
    dpi : int
        Dots per inch
    save : bool
        If True, picture is saved
    fmt : str
        Format in which the picture is saved

    Returns
    -------
    fig : class instance
        Figure
    ax : class instance
        Axes
    """

    fig, ax = plt.subplots()
    ax.plot(x, y1)
    ax.plot(x, y2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if legend is None:
        pass
    else:
        ax.legend(legend)

    if grid:
        ax.minorticks_on()
        ax.grid(b=True, which="minor", alpha=0.2)
        ax.grid(b=True, which="major", alpha=1)

    if save:
        os.makedirs(file_path, exist_ok=True)
        fig.savefig(file_path + tag + "." + fmt, dpi=dpi, format=fmt)

    return fig, ax
