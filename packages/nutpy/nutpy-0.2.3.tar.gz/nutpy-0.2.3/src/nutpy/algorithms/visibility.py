import cmath
import warnings
import numpy as np
import scipy.integrate as integrate
from scipy.interpolate import interp1d
import scipy.optimize as opt
import matplotlib.pyplot as plt
from astropy_healpix import HEALPix
from astropy import units as u
import pandas as pd
from tqdm.auto import tqdm
from numba import jit

from nutpy import numeric as nm
import nutpy.constants as cte
from nutpy.core.kinematics import rotations as kr
from nutpy.postprocessing import pgraph


def analytical_profile(
    SSP,
    delta_instrument,
    delta_detector,
    quantity="TAT",
    N=100,
    tf=1,
    precession="trace",
    annual=False,
    sensor_flag=None,
    fig_flag=True,
):
    """
    Calculates analytically the demanded quantity as a function of the angle
    regarding the precession axis

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta_instrument : float
        FOV half-angle of the main instrument [deg]
    delta_detector : float
        FOV half-angle of detector (only used for detector analysis) [deg]
    quantity : str
        Quantity to be computed
    N : int
        Resolution of results
    tf : float
        Total time considered
    precession : str
        Method used to account for precession (trace/None/factor)
    sensor_flag : bool
        If True, the analysis is performd for a single detector
    fig_flag : bool
        If True, figure is returned

    Returns
    -------
    fig : matplotlib figure
        Figure of profile
    T : ndarray (N)
        Results of calculations (profile)
    """

    alpha = SSP[0]
    beta = SSP[1]
    delta = delta_instrument

    T = np.zeros(N)

    phi = np.linspace(0, alpha + beta + delta, N) * np.pi / 180

    if quantity == "TAT":
        T = total_access_time_profile(
            SSP, delta_instrument, delta_detector, N, tf, sensor_flag, annual
        )
    elif quantity == "MAT":
        T = mean_access_time_profile(
            SSP, delta_instrument, delta_detector, N, precession, sensor_flag, annual
        )
    elif quantity == "MAX":
        T = max_access_time_profile(
            SSP, delta_instrument, delta_detector, N, precession, sensor_flag
        )
    elif quantity == "NOA":
        T = number_access_profile(
            SSP,
            delta_instrument,
            delta_detector,
            N,
            tf,
            precession,
            annual,
            sensor_flag,
        )
    else:
        Exception("Such result does not exist")

    if fig_flag:
        fig = plt.plot(phi * 180 / np.pi, T)
    else:
        fig = None

    return fig, T


def analytical_map(
    SSP,
    delta_instrument,
    delta_detector,
    quantity="TAT",
    N=100,
    tf=1,
    precession="trace",
    annual=False,
    sensor_flag=False,
    fig_flag=True,
    nside=256,
    units="s",
):
    """
    Calculates analytically the demanded quantity for all the celestial
    sphere and plots it.

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta_instrument : float
        FOV half-angle of the main instrument [deg]
    delta_detector : float
        FOV half-angle of detector (only used for detector analysis) [deg]
    quantity : str
        Quantity to be computed
    N : int
        Resolution of results
    tf : float
        Total time considered
    precession : str
        Method used to account for precession (trace/None/factor)
    annual: bool
        If True, the analysis is performed for an annual profile
    sensor_flag : bool
        If True, the analysis is performd for a single detector
    fig_flag : bool
        If True, figure is returned
    nside : int
        Size of healpix sphere
    units : str
        Time units for the output

    Returns
    -------
    fig : matplotlib figure
        Figure of profile
    data : ndarray (N)
        Results of calculations (value per pixel for Healpix scheme)
    """

    alpha = SSP[0]
    beta = SSP[1]
    delta = delta_instrument

    T = np.zeros(N)

    phi = np.linspace(0, alpha + beta + delta, N) * np.pi / 180

    _, T = analytical_profile(
        SSP,
        delta_instrument,
        delta_detector,
        quantity,
        N,
        tf,
        precession,
        annual=annual,
        sensor_flag=sensor_flag,
        fig_flag=False,
    )

    hp = HEALPix(nside=nside)
    npix = hp.npix

    T_complete = np.concatenate([np.flip(T[1:]), T], axis=0)
    phi_complete = np.concatenate([np.flip(phi[1:]), phi], axis=0)

    f = interp1d(phi_complete, T_complete, bounds_error=False, fill_value=0)

    data = np.zeros(npix)

    # generate grid over the sky
    lon, lat = hp.healpix_to_lonlat(np.arange(npix))

    # compute angle with precession axis
    x = np.cos(lon.value) * np.cos(lat.value)
    s = np.arccos(x)

    data = f(s)

    factor = 1.0

    if quantity in cte.tags_dict:
        pass
    else:
        raise NameError(f"'{quantity}' result does not exist")

    main_label = cte.tags_dict[quantity]
    default_units = cte.units_dict[quantity]

    if default_units is None:
        units_label = ""
    else:
        if units == "s":
            factor = 1.0
        elif units == "min":
            factor = 60.0
        elif units == "h":
            factor = 3600.0
        units_label = " (" + units + ")"
        data = data * 1.0 / factor

    label = main_label + units_label

    if fig_flag:
        fig = pgraph.plot_map(data, label, N)
    else:
        fig = None

    return fig, data


def total_access_time_profile(
    SSP, delta_instrument, delta_detector, N, tf, annual, sensor_flag
):
    """
    Calculates analytically the total access time as a function of the angle
    regarding the precession axis

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta_instrument : float
        FOV half-angle of the main instrument [deg]
    delta_detector : float
        FOV half-angle of detector (only used for detector analysis) [deg]
    N : int
        Resolution of results
    tf : float
        Total time considered
    annual : bool
        If True, the analysis is performed for an annual profile
    sensor_flag : bool
        If True, the analysis is performd for a single detector

    Returns
    -------
    T : ndarray (N)
        Results of calculations (profile)
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180
    delta_instrument *= np.pi / 180

    if sensor_flag:
        delta = delta_detector * np.pi / 180
    else:
        delta = delta_instrument

    T = np.zeros(N)
    phi = np.linspace(0, alpha + beta + delta_instrument, N)

    if annual:
        for i in range(N):

            T[i] = tf * total_access_time_theta(SSP, delta, phi[i])
    else:
        for i in range(N):

            T[i] = tf * total_access_time_fraction(SSP, delta, phi[i])

    return T


def total_access_time_theta(SSP, delta, th):
    """
    Performs the second integration regarding chi.

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precession)/
        [deg, deg, min, min]
    delta : float
        FOV half-angle [rad]
    th : float
        Angle regarding the precession axis [rad]

    Returns
    -------
    tat : float
        Total access time for the given parameters
    """

    chi = np.linspace(0, np.pi, 1000)  # orbital rotation angle, intregration variable
    q = np.zeros_like(chi)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        for i in range(len(chi)):

            phi = np.arccos(np.cos(chi[i]) * np.cos(th))

            q[i] = total_access_time_fraction(SSP, delta, phi)

        tat = integrate.trapz(q, x=chi) / np.pi

    return tat


def total_access_time_fraction(SSP, delta, phi):
    """
    Calculates analytically the total access time for a given value of phi.

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta : float
        FoV half-angle
    phi : float
        phi coordinate (angle with precession axis)

    Returns
    -------
    ft : float
        Result of calculations
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180

    varphi = np.linspace(0, np.pi, 1000)
    q = np.zeros_like(varphi)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        for j, th in enumerate(varphi):

            q[j] = time_ratio(th, phi, alpha, beta, delta)

        ft = integrate.trapz(q, x=varphi) / np.pi

    return ft


def time_ratio(theta, phi, alpha, beta, delta):
    """
    Calculates time ratio for a given point in the sky and a SSP set.

    Parameters
    ----------
    theta : float
        Coordinate for the sky point [rad]
    phi : float
        Coordinate for the sky point [rad]
    alpha : float
        Scan law parameter [rad]
    beta : float
        Scan law parameter [rad]
    delta : float
        Field of view semiangle [rad]

    Returns
    -------
    ratio : float
        Percentage of time that points with the same phi coordinate are viewed
    """

    R = np.arccos(
        np.cos(alpha) * np.cos(beta) - np.sin(alpha) * np.sin(beta) * np.cos(theta)
    )
    numerator = np.cos(delta) - np.cos(R) * np.cos(phi)
    denominator = np.sin(R) * np.sin(phi)

    ratio = (1 / np.pi) * np.real(cmath.acos(numerator / denominator))

    return ratio


def mean_access_time_profile(
    SSP, delta_instrument, delta_detector, N, precession, sensor_flag, annual
):
    """
    Calculates analytically the mean access time as a function of the angle
    regarding the precession axis

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta_instrument : float
        FOV half-angle of the main instrument [deg]
    delta_detector : float
        FOV half-angle of detector (only used for detector analysis) [deg]
    N : int
        Resolution of results
    precession : str
        Method used to account for precession (trace/None/factor)
    sensor_flag : bool
        If True, the analysis is performd for a single detector
    annual_flag : bool
        If True, the analysis is performed for an annual profile

    Returns
    -------
    T : ndarray (N)
        Results of calculations (profile)
    """

    tf = 1

    TAT = total_access_time_profile(
        SSP, delta_instrument, delta_detector, N, tf, annual, sensor_flag
    )
    NOA = number_access_profile(
        SSP, delta_instrument, delta_detector, N, tf, precession, annual, sensor_flag
    )

    T = np.divide(TAT, NOA, out=np.zeros_like(TAT), where=(NOA != 0))

    return T


def number_access_profile(
    SSP, delta_instrument, delta_detector, N, tf, precession, annual, sensor_flag
):
    """
    Calculates analytically the number of accesses as a function of the angle
    regarding the precession axis.

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta_instrument : float
        FOV half-angle of the main instrument [deg]
    delta_detector : float
        FOV half-angle of detector (only used for detector analysis) [deg]
    N : int
        Resolution of results
    precession : str
        Method used to account for precession (trace/None/factor)
    sensor_flag : bool
        If True, the analysis is performd for a single detector

    Returns
    -------
    NA : ndarray (N)
        Results of calculations (profile)
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180

    delta_instrument *= np.pi / 180

    if sensor_flag:
        delta = delta_detector * np.pi / 180
    else:
        delta = delta_instrument

    NA = np.zeros(N)

    phi = np.linspace(0, alpha + beta + delta_instrument, N)

    for i in range(N):
        NA[i] = number_access(SSP, delta, phi[i], tf, precession, annual)

    return NA


def number_access(SSP, delta, phi, tf, precession, annual):
    """
    Calculates analytically the number of accesses for a given value of phi.

    Parameters
    ----------
    SSP : list (4)
        Scan Strategy Parameters (alpha, beta, spin, precesion)/
        [deg, deg, min, min]
    delta : float
        Field of view semiangle [rad]
    phi : float
        phi coordinate (angle with precession axis) [rad]
    precession : str
        Indicates type of method used for precession aproximation
        (trace/None/factor)

    Returns
    -------
    NA : ndarray (N)
        Results of calculations (profile)
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180
    omega_spin = 2 * np.pi / (60 * SSP[2])
    omega_prec = 2 * np.pi / (60 * SSP[3])
    Tspin = 60 * SSP[2]

    chi = np.linspace(0, np.pi, 1000)
    delta_theta = np.zeros_like(chi)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if annual:
            for i in range(len(chi)):
                varphi = np.arccos(np.cos(chi[i]) * np.cos(phi))

                if precession is False:

                    delta_theta[i] = delta_theta_pure(alpha, beta, delta, varphi)

                elif precession is True:

                    delta_theta[i] = delta_theta_trace(
                        alpha, beta, omega_spin, omega_prec, delta, varphi
                    )

            NA = (integrate.trapz(delta_theta, x=chi) / np.pi) * tf / (np.pi * Tspin)
        else:
            if precession is None:

                delta_theta = delta_theta_pure(alpha, beta, delta, phi)

            elif precession == "trace":

                delta_theta = delta_theta_trace(
                    alpha, beta, omega_spin, omega_prec, delta, phi
                )

            elif precession == "factor":

                delta_theta = delta_theta_factor(
                    alpha, beta, omega_spin, omega_prec, delta, phi
                )

            NA = 1 / (2 * np.pi / omega_spin) * delta_theta / np.pi

    return NA


def delta_theta_pure(alpha, beta, delta, phi):
    """
    Arc of points with the same phi coordinate between exterior and interior trace
    curves for the case of pure spin (no precession)

    Parameters
    ----------
    alpha : float
        Scan law parameter [rad]
    beta : float
        Scan law parameter [rad]
    delta : float
        Field of view semiangle [rad]
    phi : float
        phi coordinate (angle with precession axis) [rad]

    Returns
    -------
    delta_theta : float
        Length of the arc [rad]
    """

    if phi > (alpha + beta - delta):
        theta_exterior = 0

    else:
        theta_exterior = nm.theta_ext_simple(alpha, beta, delta, phi)

    if phi > (alpha + beta + delta):
        theta_interior = 0

    else:
        theta_interior = nm.theta_int_simple(alpha, beta, delta, phi)

    delta_theta = theta_interior - theta_exterior

    return delta_theta


def delta_theta_trace(alpha, beta, omega_spin, omega_prec, delta, phi):
    """
    Arc of points with the same phi coordinate between exterior and interior trace
    curves calculated with the trace method.

    Parameters
    ----------
    alpha : float
        Scan law parameter [rad]
    beta : float
        Scan law parameter [rad]
    omega_spin : float
        Spin speed [rad/s]
    omega_prec : float
        Precession speed [rad/s]
    delta : float
        Field of view semiangle [rad]
    phi : float
        phi coordinate (angle with precession axis) [rad]

    Returns
    -------
    delta_theta : float
        Length of the arc [rad]
    """

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        with np.errstate(divide="ignore", invalid="ignore"):

            if phi > (alpha + beta - delta):
                theta_exterior = 0

            elif phi < np.abs(np.abs(alpha - beta) - delta):
                # intersection time is found
                time_exterior = opt.minimize_scalar(
                    lambda t: (
                        np.abs(
                            nm.Rext(t, alpha, beta, delta, omega_prec, omega_spin)
                            - (np.abs(np.abs(alpha - beta) - delta))
                        )
                    ),
                    bounds=(0.0, np.pi / omega_spin),
                    method="bounded",
                ).x

                theta_exterior = nm.Thetaext(
                    time_exterior, alpha, beta, delta, omega_prec, omega_spin
                )

            else:
                time_exterior = opt.minimize_scalar(
                    lambda t: np.abs(
                        nm.Rext(t, alpha, beta, delta, omega_prec, omega_spin) - phi
                    ),
                    bounds=(0.0, np.pi / omega_spin),
                    method="bounded",
                ).x

                theta_exterior = nm.Thetaext(
                    time_exterior, alpha, beta, delta, omega_prec, omega_spin
                )

            if phi > (alpha + beta + delta):
                theta_interior = 0

            elif phi < (np.abs(alpha - beta) + delta):
                time_interior = opt.minimize_scalar(
                    lambda t: (
                        np.abs(
                            nm.Rint(t, alpha, beta, delta, omega_prec, omega_spin)
                            - (np.abs(alpha - beta) + delta)
                        )
                    ),
                    bounds=(0.0, np.pi / omega_spin),
                    method="bounded",
                ).x

                theta_interior = nm.Thetaint(
                    time_interior, alpha, beta, delta, omega_prec, omega_spin
                )

            else:
                time_interior = opt.minimize_scalar(
                    lambda t: np.abs(
                        nm.Rint(t, alpha, beta, delta, omega_prec, omega_spin) - phi
                    ),
                    bounds=(0.0, np.pi / omega_spin),
                    method="bounded",
                ).x

                theta_interior = nm.Thetaint(
                    time_interior, alpha, beta, delta, omega_prec, omega_spin
                )

    delta_theta = theta_interior - theta_exterior

    return delta_theta


def delta_theta_factor(alpha, beta, omega_spin, omega_prec, delta, phi):
    """
    Arc of points with the same phi coordinate between exterior and interior trace
    curves calculated with the trace method.

    Parameters
    ----------
    alpha : float
        Scan law parameter [rad]
    beta : float
        Scan law parameter [rad]
    omega_spin : float
        Spin speed [rad/s]
    omega_prec : float
        Precession speed [rad/s]
    delta : float
        Field of view semiangle [rad]
    phi : float
        phi coordinate (angle with precession axis) [rad]

    Returns
    -------
    delta_theta : float
        Length of the arc [rad]
    """

    phi_star_t_max = phi_star_t_max_f(delta, beta)

    if phi > (alpha + beta - delta):
        theta_exterior = 0

    else:
        theta_exterior = nm.theta_ext_simple(alpha, beta, delta, phi) / time_factor(
            omega_spin, omega_prec, alpha, phi_star_t_max, phi
        )

    if phi > (alpha + beta + delta):
        theta_interior = 0

    else:
        theta_interior = nm.theta_int_simple(alpha, beta, delta, phi) / time_factor(
            omega_spin, omega_prec, alpha, phi_star_t_max, phi
        )

    delta_theta = theta_interior - theta_exterior

    return delta_theta


def max_access_time_profile(
    SSP, delta_instrument, delta_detector, N, precession, sensor_flag
):
    """
    Calculates analytically the maximum access time as a function of precession-axis separation angle

    Parameters
    ----------
    SSP : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/(deg, deg, min, min)
    FOV : float
        Field of view total amplitude [deg]
    N : integer
        Discretization parameter of phi coordinate
    precession : str
        Indicates type of method used for precession aproximation trace/None/factor
    delta_detector : float
        Detector FOV half-angle

    Returns
    -------
    T : ndarray (N)
        Results of calculations (profile)
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180

    delta_instrument *= np.pi / 180

    if sensor_flag:
        delta = delta_detector * np.pi / 180
    else:
        delta = delta_instrument

    T = np.zeros(N)

    phi = np.linspace(0, alpha + beta + delta_instrument, N)

    T = [max_access_time(SSP, delta, phi[i], precession) for i in range(N)]

    return T


def max_access_time(SSP, delta, phi, precession):
    """
    Calculates analytically the maximum access time as a function of precession-axis separation angle

    Parameters
    ----------
    SSP : list (4)
        Scan Law Parameters (alpha, beta, spin, precesion)/(deg, deg, min, min)
    FOV : float
        Field of view total amplitude [deg]
    N : integer
        Discretization parameter of phi coordinate
    precession : str
        Indicates type of method used for precession aproximation trace/None/factor
    delta_detector : float
        Detector FOV half-angle

    Returns
    -------
    T : ndarray (N)
        Results of calculations (profile)
    """

    alpha = SSP[0] * np.pi / 180
    beta = SSP[1] * np.pi / 180
    omega_spin = 2 * np.pi / (60 * SSP[2])
    omega_prec = 2 * np.pi / (60 * SSP[3])
    Tspin = SSP[2] * 60

    phi_star_t_max = phi_star_t_max_f(delta, beta)
    tmax = access_time_max(Tspin, delta, beta)

    if precession == "trace":
        if phi > (alpha + phi_star_t_max):
            rstar = phi - alpha
            t = access_time(Tspin, delta, beta, rstar) * time_factor(
                omega_spin, omega_prec, alpha, phi_star_t_max, phi
            )

        elif phi < np.abs(alpha - phi_star_t_max):
            rstar = alpha - np.sign(alpha - phi_star_t_max) * phi
            t = access_time(Tspin, delta, beta, rstar) * time_factor(
                omega_spin, omega_prec, alpha, phi_star_t_max, phi
            )

        else:
            t = tmax * time_factor(omega_spin, omega_prec, alpha, phi_star_t_max, phi)

    else:
        raise NotImplementedError("Only trace method is avaiable.")

    return t


def phi_star_t_max_f(delta, beta):
    """
    Returns phi* coordinate that produces maximum time access

    Parameters
    ----------
    delta : float
        Field of view half-angle [rad]
    beta : float
        Scan law parameter [rad]

    Returns
    -------
    rstar : float
        phi* coordinate for maximum access time
    """

    numerator = np.sqrt(np.cos(delta) ** 2 - np.cos(beta) ** 2)
    denominator = np.cos(beta)

    rstar = np.arctan(numerator / denominator)

    return rstar


def access_time(Tspin, delta, beta, rstar):
    """
    Calculates the access time for defined SSP and phi* coordinate

    Parameters
    ----------
    Tspin : float
        Period of spin motion (sec)
    delta : float
        Field of view half-angle [rad]
    beta : float
        Scan law parameter [rad]
    rstar : float
        phi* coordinate [rad]

    Returns
    -------
    t_access : float
        Time of access (sec)
    """

    t_access = (Tspin / np.pi) * theta_access(delta, beta, rstar)

    return t_access


def access_time_max(Tspin, delta, beta):
    """
    Calculates maximum access time achievable for pure spin motion

    Parameters
    ----------
    Tspin : float
        Period of spin motion (sec)
    delta : float
        Field of view half-angle [rad]
    beta : float
        Scan law parameter [rad]

    Returns
    -------
    time_access_max : float
        Maximum time of access (sec)
    """

    numerator = np.sqrt(np.cos(delta) ** 2 - np.cos(beta) ** 2)
    denominator = np.sin(beta)

    time_access_max = (Tspin / np.pi) * np.real(cmath.acos(numerator / denominator))

    return time_access_max


def theta_access(delta, beta, rstar):
    """
    Calculates theta coordinate of access condition

    Parameters
    ----------
    delta : float
        Field of view half-angle [rad]
    beta : float
        Scan law parameter [rad]
    rstar : float
        phi* coordinate [rad]

    Returns
    -------
    theta : float
        Theta coordinate when access condition is met
    """

    numerator = np.cos(delta) - np.cos(beta) * np.cos(rstar)
    denominator = np.sin(beta) * np.sin(rstar)
    theta = np.real(cmath.acos(numerator / denominator))

    return theta


def tau_f(alpha, phi_star_t_max, phi):
    """
    Calculates tau angle for direction defined by phi coordinate

    Parameters
    ----------
    alpha : float
        Scan law parameter [rad]
    phi_star_t_max : float
        phi* coordinate for maximum time [rad]
    phi : float
        phi coordinate of direction of interest [rad]

    Returns
    -------
    tau_angle : float
        tau angle of direcction with phi coordinate [rad]
    """

    numerator = np.cos(alpha) * np.cos(phi_star_t_max) - np.cos(phi)
    denominator = np.sin(alpha) * np.sin(phi_star_t_max)

    tau = np.real(cmath.acos(numerator / denominator))

    return tau


def gamma_f(tau, phi_spin_angle, alpha):
    """
    Calculates gamma angle

    Parameters
    ----------
    tau : float
        tau angle [rad]
    phi_spin_angle : float
        Spin angle [rad]
    alpha : float
        Scan law parameter [rad]

    Returns
    -------
    gamma : float
        gamma angle [rad]
    """

    gamma = np.cos(tau) * np.cos(phi_spin_angle) + np.cos(alpha) * np.sin(tau) * np.sin(
        phi_spin_angle
    )

    return gamma


def phi_spin_angle_f(phi_star_t_max, tau, alpha):
    """
    Calculates phi angle

    Parameters
    ----------
    phi_star_t_max : float
        phi* coordinate for maximum access time [rad]
    tau : float
        tau angle [rad]
    alpha : float
        Scan law parameter [rad]

    Returns
    -------
    phi_spin_angle : float
        Spin angle [rad]
    """

    numerator = np.sin(phi_star_t_max) * np.sin(tau)
    denominator = np.cos(alpha) * np.sin(phi_star_t_max) * np.cos(tau) + np.sin(
        alpha
    ) * np.cos(phi_star_t_max)

    phi_spin_angle = np.arctan2(numerator, denominator)

    return phi_spin_angle


def time_factor(omega_spin, omega_prec, alpha, phi_star_t_max, phi):
    """
    Calculates the correction factor for access time when precession motion is present

    Parameters
    ----------
    omega_spin : float
        Scan law parameter [rad]
    omega_prec : float
        Scan law parameter [rad]
    alpha : float
        Scan law parameter [rad]
    phi_star_t_max : float
        phi* coordinate for maximum time [rad]
    phi : float
        phi coordinate of direction of interest [rad]

    Returns
    -------
    factor : float
        correction factor
    """

    t = tau_f(alpha, phi_star_t_max, phi)
    p = phi_spin_angle_f(phi_star_t_max, t, alpha)
    g = gamma_f(t, p, alpha)

    k = np.sign(alpha - phi_star_t_max)

    if phi > (alpha + phi_star_t_max):
        factor = (
            omega_spin
            * np.sin(phi - alpha)
            / (omega_spin * np.sin(phi - alpha) + omega_prec * np.sin(phi))
        )

    elif phi < np.abs(alpha - phi_star_t_max):
        factor = (
            omega_spin
            * np.sin(alpha - phi * k)
            / (omega_spin * np.sin(alpha - phi * k) - omega_prec * np.sin(phi * k))
        )

    else:
        factor = (
            omega_spin
            * np.sin(phi_star_t_max)
            / (omega_spin * np.sin(phi_star_t_max) + omega_prec * np.sin(phi) * g)
        )

    return factor


def numerical_analysis(
    instrument, nside, bar, detailed, dense, border_angle, annual=False
):
    """
    Performs numerical analysis

    Parameters
    ----------
    instrument : nutpy instrument class
        Instrument class instance
    nside : integer
        Number of divisions of the sky sphere
    bar : bool
        If True, shows progress bar
    detailed : bool
        If True, computes results for each sensor
    dense : bool
        If True, stores results from each detector
    border_angle : float
        Sum of alpha, beta and delta_instrument angles [deg]

    Returns
    -------
    numerical_results_df :  pandas DataFrame
        Results of temporal analysis
    numerical_results_detailed_df :  pandas DataFrame
        Results of temporal analysis for each sensor, if dense is False, None is
        returned
    """

    hp = HEALPix(nside=nside)
    npix = hp.npix

    time, pointing = kr.pointing(instrument.attitude_df, instrument.u0)

    if bar:
        pbar = tqdm(total=npix)

    u = np.zeros((3, 1))

    rows_list = []
    sensors_results_detailed_dict = {}

    lon, lat = hp.healpix_to_lonlat(range(npix))
    lon = lon.value
    lat = lat.value

    for i in range(npix):

        row_dict = {}

        u[0, 0] = np.cos(lat[i]) * np.cos(lon[i])
        u[1, 0] = np.cos(lat[i]) * np.sin(lon[i])
        u[2, 0] = np.sin(lat[i])

        if u[0, 0] > np.cos(border_angle * np.pi / 180) or annual:
            _, visibility = visibility_analysis(pointing, time, u, instrument.fov)

            access_count, each_access_time, start_access_time, _ = process_visibility(
                time, visibility
            )
        else:
            access_count, each_access_time, start_access_time, _ = (0, [], [], None)

        total_access_time = np.sum(each_access_time)

        row_dict["TAT"] = total_access_time
        row_dict["NOA"] = access_count

        if access_count == 0:
            row_dict["MAT"] = 0
            row_dict["MAX"] = 0
        else:
            row_dict["MAT"] = total_access_time / access_count
            row_dict["MAX"] = each_access_time.max()

        if dense:
            row_dict["Accesses_list"] = each_access_time
            row_dict["Start access time"] = start_access_time

        if detailed:
            sensors_results_df = process_sensors(visibility, instrument, u, i)

            n_viewed_sensors = sum(sensors_results_df["TAT"].values != 0)
            row_dict["PVS"] = 100 * n_viewed_sensors / (instrument.nd)

            if n_viewed_sensors == 0:
                row_dict["SGA"] = None
            else:
                row_dict["SGA"] = (
                    sensors_results_df["SGA"].values.sum() / n_viewed_sensors
                )

            if dense:
                sensors_results_detailed_dict[str(i)] = sensors_results_df
            else:
                sensors_results_detailed_dict[str(i)] = None

        rows_list.append(row_dict)

        if bar:
            pbar.update(1)

    if detailed and dense:
        numerical_results_detailed_df = pd.concat(
            sensors_results_detailed_dict.values(), ignore_index=True
        ).astype(
            {
                "pixel_id": "uint32",
                "sensor_id": "uint16",
                "TAT": "float32",
                "MAT": "float16",
                "MAX": "float16",
                "NOA": "uint16",
                "SGA": "float16",
            }
        )
    else:
        numerical_results_detailed_df = None

    numerical_results_df = pd.DataFrame(rows_list)
    numerical_results_df = numerical_results_df.astype(
        {"TAT": "float32", "MAT": "float16", "MAX": "float16", "NOA": "uint16"}
    )

    if bar:
        pbar.close()

    return numerical_results_df, numerical_results_detailed_df


def visibility_analysis(pointing, time, u, FOV):
    """
    Visibility for a given direction

    Parameters
    ----------
    pointing : ndarry (3,n)
        Pointing over time
    u : ndarray (3x1)
        Direction of study
    FOV : float
        Field of view (half-angle) [deg]

    Returns
    -------
    time :  1D array (n,)
        Time period analized
    visibility :  1D array (n,)
        1-> direction inside FOV, 0-> out of FOV
    """

    delta_c = np.cos(FOV * np.pi / 180 / 2)

    dot = np.dot(pointing.T, u)
    angle = dot.flatten()

    visibility = np.where(angle > delta_c, 1, 0)

    return time, visibility


@jit(nopython=True)
def process_visibility(time, visibility):
    """
    Process raw visibility data

    Parameters
    ----------
    time :  1D array (n,)
        Time period analized
    visibility :  1D array (n,)
        1-> direction inside FOV, 0-> out of FOV

    Returns
    -------
    ct :  int
        Number of accesses
    each_access_time :  1D array (ct,)
        Duration of each access
    start_access_time :  1D array (ct,)
        Start time of each access
    """

    dT = time[1]

    ct = 0

    visibility_n = np.concatenate((np.array([0]), visibility, np.array([0])))
    # access_io = np.where(np.sign(visibility_n[:-1]) != np.sign(visibility_n[1:]))[0]
    acs = visibility_n[:-1] < visibility_n[1:]
    ace = visibility_n[:-1] > visibility_n[1:]

    data = np.logical_or(acs, ace)
    access_io = data.nonzero()[0]

    enter = access_io[0::2]
    each_access_time = (access_io[1::2] - access_io[0::2]) * dT
    start_access_time = enter * dT

    ct = int(len(access_io) / 2)

    return ct, each_access_time, start_access_time, enter


def process_sensors(visibility, instrument, u, idx):
    """
    Detects which sensors are viewed and computes the figures of merit.
    The results

    Parameters
    ----------
    visibility : 1-D array (n)
        Indicates if there is instrument access with 1/0 in each step time
    instrument : class
        Instrument class instance
    u: ndarray (3xn)
        Position in the sky
    idx: int
        Pixel ID from the healpix discretization

    Returns
    -------
    df : pandas dataframe
        Results of calculations
    """

    # get index of accesses
    visibility_mask = visibility.astype(bool)

    time = instrument.attitude_df.index.values

    # number of sensors
    nd = instrument.nd

    sensor_id = np.arange(nd)
    pixel_id = np.ones(nd, dtype="int16") * idx

    # if no sensor is viewed, the corresponding dataframe is full of zeros
    if visibility.sum() == 0:
        data = np.concatenate(
            (
                pixel_id.reshape(-1, 1),
                sensor_id.reshape(-1, 1),
                np.zeros((nd, 5), dtype="int16"),
            ),
            axis=1,
        )

    else:
        # attitude of inst when there are accesses
        quats = instrument.attitude_df.values[visibility_mask, :].T

        v = kr.quat_trans_v(quats, u)

        # polarization vector
        E = nm.perpendicular_vector(u)

        # transform polarization vector to instrument axes
        Ep = kr.quat_trans_v(quats, E)

        # pointing direction in local frame
        vx = np.array([1, 0, 0])

        # calculation of polar coordinates
        rho = np.arccos(vx @ v) / (instrument.fov / 2 * np.pi / 180)
        phi = np.arctan2(v[2, :], v[1, :])

        # location of impacts
        x, y = nm.pol2cart(rho, phi)

        sensors_g_alpha = np.zeros(nd)

        sensors_tat = np.zeros(nd)
        sensors_mat = np.zeros(nd)
        sensors_max = np.zeros(nd)
        sensors_n = np.zeros(nd)
        sensors_g_alpha = np.zeros(nd)

        # loop over each sensor
        for i in range(nd):
            # filter time steps where trace is over sensor i
            sensors_visibility = nm.circle_check(
                x, y, instrument.xd[i], instrument.yd[i], instrument.r
            )

            access_count, each_access_time, _, enter = process_visibility(
                time, sensors_visibility
            )

            if access_count > 0:
                sensors_tat[i] = each_access_time.sum()
                sensors_mat[i] = each_access_time.mean()
                sensors_max[i] = each_access_time.max()
                sensors_n[i] = access_count
                sensors_g_alpha[i] = nm.g_alpha(Ep, enter)

        data = np.vstack(
            (
                pixel_id,
                sensor_id,
                sensors_tat,
                sensors_mat,
                sensors_max,
                sensors_n,
                sensors_g_alpha,
            )
        ).T

    data_df = pd.DataFrame(
        columns=["pixel_id", "sensor_id", "TAT", "MAT", "MAX", "NOA", "SGA"], data=data
    )

    return data_df


def numerical_profile(mission, quantity, unit, N, Nth, fig_flag, sensor_id):
    """
    Plots the profile (variation over phi) of the specified quantity.

    Parameters
    ----------
    mission : Mission class
        Mission with temporal analysis results
    quantity : str
        Result to be processed
    unit : str
        Time units for the output
    N : integer
        Discretization parameter for phi coordinate
    Nth : integer
        Discretizatio parameter for theta coordinate
    fig_flag : bool
        If True, figure is returned
    sensor_id : int
        ID of the sensor (only for sensor analysis)

    Returns
    -------
    fig : matplotlib figure
        Figure of profile
    T : ndarray (N)
        Results of calculations (profile)
    """

    data_df = mission.numerical_results_df
    alpha = mission.SSP[0]
    beta = mission.SSP[1]
    delta = mission.delta_instrument

    npix = len(data_df.index.values)
    nside = int(np.sqrt(npix / 12))

    phi = np.linspace(0, alpha + beta + delta, N) * np.pi / 180
    theta = np.linspace(0, 2 * np.pi, Nth)

    hp = HEALPix(nside=nside)

    T = np.zeros(N)

    ftime = 1
    if unit == "s":
        ftime = 1
    elif unit == "min":
        ftime = 60
    elif unit == "h":
        ftime = 3600

    factor = 1 / ftime

    data = mission.visibility_results(quantity, sensor_id)

    lon = np.zeros((N, Nth))
    lat = np.zeros((N, Nth))

    for i in range(N):

        x = np.cos(phi[i])
        y = np.sin(phi[i]) * np.sin(theta)
        z = np.sin(phi[i]) * np.cos(theta)

        lat[i, :] = np.arcsin(z)
        lon[i, :] = np.arctan2(y, x)

    lon[lon < 0] += 2 * np.pi

    interpolated_data = hp.interpolate_bilinear_lonlat(lon * u.rad, lat * u.rad, data)

    for i in range(N):
        T[i] = factor * interpolated_data[i, :].mean()

        if quantity == "MAX":
            T[i] = factor * interpolated_data[i, :].max()

    x_plot = phi * 180 / np.pi
    y_plot = T

    if fig_flag:
        fig = plt.plot(x_plot, y_plot)
    else:
        fig = None

    return fig, T


def numerical_map(mission, quantity, N, units, sensor_id):
    """
    Plots a hammer projection of the specified quantity for all the celestial.

    Parameters
    ----------
    mission : Mission class
        Mission with temporal analysis results
    quantity : str
        Result to be plotted (TAT/MAT/MAX/NOA)
    N : int
        Size of mesh for plotting
    units : str
        Time units for the output
    sensor_id : int
        ID of the sensor (only for sensor analysis)

    Returns
    -------
    fig :  matplotlib figure
        Plotted figure
    data : ndarray (N)
        Results of calculations (value per pixel for Healpix scheme)
    """

    factor = 1.0

    if quantity in cte.tags_dict:
        pass
    else:
        raise NameError(f"'{quantity}' result does not exist")

    data = mission.visibility_results(quantity, sensor_id)

    main_label = cte.tags_dict[quantity]
    default_units = cte.units_dict[quantity]

    if default_units is None:
        units_label = ""
    else:
        if units == "s":
            factor = 1.0
        elif units == "min":
            factor = 60.0
        elif units == "h":
            factor = 3600.0
        units_label = " (" + units + ")"
        data = data * 1.0 / factor

    label = main_label + units_label

    fig = pgraph.plot_map(data, label, N)

    return fig, data
