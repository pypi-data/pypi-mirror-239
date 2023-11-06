import numpy as np

from astropy_healpix import HEALPix


def read_detectors_coordinates(file_name):
    """
    Read detectors coordinates from file

    The file must be in the working directory. Two columns separated by white space,
    comma as decimal separator

    Parameters
    ----------
    file_name : str
        Name of the file with the detectors coordinates

    Returns
    -------
    x : 1D-array
        X-axis coordinates of the detectors
    y : 1D-array
        Y-axis coordinates of the detectors
    """

    with open(file_name, "r", encoding="UTF-8") as data:
        x = []
        y = []
        for line in data:
            p = line.replace(",", ".").split()
            x.append(float(p[0]))
            y.append(float(p[1]))

    x = np.asarray(x)
    y = np.asarray(y)

    # coordinates are scaled so farthest point is at a radial distance of 0.9
    rmax = np.sqrt((x**2 + y**2)).max()
    ratio = (1 / rmax) * 0.9

    x *= ratio
    y *= ratio

    return x, y


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


def SSP_to_rad(SSP):
    """
    Changes SSP units.

    Angles change from degrees to radians and periodic motion periods (min) change
    to angular velocities (rad/s).

    Parameters
    ----------
    SSP : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/
        (deg, deg, min, min)

    Returns
    -------
    SSP_rad : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/
        (rad, rad, rad/s, rad/s)
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180
    omega_prec = 2 * np.pi / (SSP[3] * 60)
    omega_spin = 2 * np.pi / (SSP[2] * 60)

    SSP_rad = [alpha, beta, omega_spin, omega_prec]

    return SSP_rad


def coherence_criteria(SSP, nside, dT):
    """
    Checks if dT is low enough to ensure that viewed pixels are detected

    Parameters
    ----------
    SSP : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/
        (deg, deg, min, min)
    nside : integer
        Number of divisions of the sky sphere
    dT : float
        Step time used for the numerical analysis

    Returns
    -------
    flag : bool
        If True, dT is adequate
    """

    SSP_rad = SSP_to_rad(SSP)
    omega_spin = SSP_rad[2]
    omega_prec = SSP_rad[3]

    hp = HEALPix(nside=nside)

    omega = np.sqrt(
        (omega_spin * np.sin(SSP[1])) ** 2
        + (omega_prec + omega_spin * np.cos(SSP[1])) ** 2
    )
    arc_dT = omega * dT
    arc_grid = hp.pixel_resolution.to("rad").value

    flag = 2 * arc_dT < arc_grid

    return flag


def coherence_criteria_detectors(SSP, delta_detector, dT):
    """
    Checks if dT is low enough to ensure that all detectors viewed are catched

    Parameters
    ----------
    SSP : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/
        (deg, deg, min, min)
    delta_detector : float
        Half-angle of the detectors FoV
    dT : float
        Step time used for the numerical analysis

    Returns
    -------
    flag : bool
        If True, dT is adequate
    """

    SSP_rad = SSP_to_rad(SSP)
    omega_spin = SSP_rad[2]
    omega_prec = SSP_rad[3]

    delta_detector *= np.pi / 180

    omega = np.sqrt(
        (omega_spin * np.sin(SSP[1])) ** 2
        + (omega_prec + omega_spin * np.cos(SSP[1])) ** 2
    )
    arc_dT = omega * dT

    flag = 2 * arc_dT < delta_detector

    return flag


def estimate_memory(N, N_det, unit="GB"):
    """
    Estimates memory consumption in dense sensor analysis

    Parameters
    ----------
    N : int
        nside of HEALPix sphere
    N_det : int
        Number of detectors
    unit : str
        Units for memory usage display

    Returns
    -------
    memory : float
        Memory usage
    memory_text : str
        Message with the memory ussage
    """

    average_data_size = 18 / 7  # bytes

    n_columns = 7

    n_hp = 12 * N**2

    units_factor = {"GB": 1024**3, "MB": 1024**2, "KB": 1024}

    memory = average_data_size * n_columns * n_hp * N_det / units_factor[unit]

    memory_text = "Approximate memory usage: {:.2f} ".format(memory) + unit

    return memory, memory_text
