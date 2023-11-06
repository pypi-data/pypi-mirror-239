import numpy as np
from nutpy.core.kinematics import rotations as kr
import nutpy.utilities as utl
import pkg_resources
import pandas as pd


class Satellite:
    """
    Satellite model class, includes instances of Instrument class

    Attributes
    ----------
    SSP : list (5) of floats
        Scan strategy parameters [alpha (deg), beta (deg), spin period
        (min), precesion period (min), delta (deg)]
    q0 : ndarray (4,1)
        Initial satellite attitude expressed as quaternion
    attitude : pandas DataFrame
        Attitude over time of the satellite
    instrument_pointing : pandas DataFrame
        Pointing of the instrument over time
    inst : Instrument class
        Instance of instrument class with default configuration
    """

    default_config = {
        "SSP": [45.0, 50.0, 10.0, 93.0],
        "q0": np.array([0, 0, 0, 1]).reshape(-1, 1),
        "attitude": pd.DataFrame(columns=["q1", "q2", "q3", "q4"]),
        "instrument_pointing": pd.DataFrame(columns=["ux", "uy", "uz"]),
    }

    def __init__(self, **kwargs):
        """
        Constructor

        Parameters
        ----------
        q0 : ndarray (4,1)
            Initial satellite attitude expressed as quaternion
        attitude : pandas DataFrame (empty)
            Attitude over time of the satellite
        instrument_pointing : pandas DataFrame (empty)
            Pointing of the instrument over time
        """

        self.inst = Instrument(**kwargs)

        config = {**self.default_config, **kwargs}

        self.q0 = config["q0"]
        self.attitude_df = config["attitude"]

        self.alpha = config["SSP"][0]
        self.beta = config["SSP"][1]
        self.Tspin = config["SSP"][2]
        self.Tprec = config["SSP"][3]

        self.mounting_matrix = kr.Cz(self.beta * np.pi / 180)

    @property
    def instrument_attitude_df(self):
        return self.inst.attitude_df

    @property
    def SSP(self):
        return (self.alpha, self.beta, self.Tspin, self.Tprec)

    def generate_attitude(self, Tsim, dT, q0, SSP, annual):
        """
        Generates satellite and instrument attitude

        Parameters
        ----------
        Tsim : float
            Period of time considered for the numerical analysis
        dT : float
            Step time
        q0 : ndarray (4,1)
            Initial satellite attitude expressed as quaternion
        SSP : list (5) of floats
            Scan strategy parameters [alpha (deg), beta (deg), spin period
            (min), precesion period (min), delta (deg)]
        """

        time, satellite_quaternions = kr.emulate_attitude(Tsim, dT, q0, SSP, annual)

        self.attitude_df = pd.DataFrame(
            columns=self.attitude_df.columns, data=satellite_quaternions.T, index=time
        )

        mounting_quaternion = kr.C2q(self.mounting_matrix)

        instrument_quaternions = kr.quat_product(
            mounting_quaternion, satellite_quaternions
        )

        self.inst.attitude_df = pd.DataFrame(
            columns=self.attitude_df.columns, data=instrument_quaternions.T, index=time
        )

        return 0


class Instrument:
    """
    Instrument model

    Attributes
    ----------
    delta_intrument : float
        Half-angle of the isntrument fov (degrees)
    delta_detector : float
        Half-angle of the detector fov (degrees)
    Nx : int
        Number of horizontal detectors (rectangular array)
    Ny : int
        Number of vertical detectors (rectangular array)
    layout : str
        Type of array layout (circular/rectangular/custome)
    Nd : int
        Number of detectors of the circular array
    file_name : str
        File with detectors positions
    xd : float
        X coordinates of detectors in focal plane
    yd : float
        Y coordinates of detectors in focal plane
    nd : int
        Number of detectors
    r : float
        Half-angle of the detector fov (degrees)
    ids : 1D-array
        List of detectors id
    """

    default_config = {
        "delta_instrument": 7.5,
        "delta_detector": 0.25,
        "Nx": 20,
        "Ny": 20,
        "layout": "rectangular",
        "Nd": 400,
        "file_name": "example_custome_layout.txt",
        "u0": np.array([1, 0, 0]).reshape(-1, 1),
    }

    def __init__(self, **kwargs):
        """
        Constructor

        Parameters
        ----------
        delta_intrument : float
            Half-angle of the isntrument fov (degrees)
        delta_detector : float
            Half-angle of the detector fov (degrees)
        Nx : int
            Number of horizontal detectors (rectangular array)
        Ny : int
            Number of vertical detectors (rectangular array)
        layout : str
            Type of array layout (circular/rectangular/custome)
        Nd : int
            Number of detectors of the circular array
        file_name : str
            File with detectors positions
        u0 : ndarray (3,1)
            Direction of observation (in instrument frame)
        """

        self.grid_functions_dict = {
            "rectangular": self.generate_rectangular_grid,
            "circular": self.generate_circular_grid,
            "custome": self.generate_custome_grid,
        }

        config = {**self.default_config, **kwargs}

        self.delta_instrument = config["delta_instrument"]
        self.delta_detector = config["delta_detector"]
        self.Nx = config["Nx"]
        self.Ny = config["Ny"]
        self.layout = config["layout"]
        self.Nd = config["Nd"]
        self.file_name = config["file_name"]
        self.u0 = config["u0"]

        self.xd = None
        self.yd = None
        self.nd = None
        self.r = None
        self.ids = None
        self.mounting_matrix = None

        # generate desired layout
        self.grid_functions_dict[self.layout]()

    @property
    def fov(self):
        return 2 * self.delta_instrument

    def generate_rectangular_grid(self):
        """ "
        Generates rectangular array of detectors

        The fov of the instrument is considered to have unitary radius, then the
        size of a rectangle circumscribed to it calculated. Such rectangle have
        the same side lenghts ratio (Lx/Ly) as the ratio of detectors (Nx/Ny)
        """

        # ratio of detectors
        s = self.Nx / self.Ny

        # scale detectors half-angle fov (its size) with instrument half-angle
        # fov (fov size)
        self.r = self.delta_detector / (self.delta_instrument)

        # size of rectangle (with its sides having  ratio s) circumscribed to
        # unitary circle (fov)
        Lx = 2 * np.sqrt(1 / (1 + 1 / (s**2)))
        Ly = Lx / s

        # length between corner detectors centers
        lx = Lx / 2 - self.r
        ly = Ly / 2 - self.r

        # position of Nx/Ny detectors, equally spaced
        x = np.linspace(-lx, lx, self.Nx)
        y = np.linspace(-ly, ly, self.Ny)

        X, Y = np.meshgrid(x, y)

        self.xd = X.flatten()
        self.yd = Y.flatten()

        # number of detectors
        self.nd = self.Nx * self.Ny

        # id of detectors
        self.ids = np.arange(self.nd)

        return 0

    def generate_circular_grid(self):
        """
        Generates circular array of detectors

        This distribution is the same as the seeds of a sunflower

        References
        ----------
        .. [1] https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere/26127012#26127012 # noqa
        """

        # scale detectors half-angle fov (its size) with instrument half-angle fov (fov size)
        self.r = self.delta_detector / (self.delta_instrument)

        indices = np.arange(0, self.Nd, dtype=float) + 0.5

        # golden number
        phi = (1 + 5**0.5) / 2

        # sequence of raius and angle
        r = np.sqrt(indices / self.Nd) - self.r
        theta = 2 * np.pi * phi * indices

        self.xd = r * np.cos(theta)
        self.yd = r * np.sin(theta)

        # number of detectors
        self.nd = self.Nd

        # id of detectors
        self.ids = np.arange(self.nd)

        return 0

    def generate_custome_grid(self):
        """
        Generates custome array of detectors

        The coordinates of the detectors center are retrieved from txt file
        """

        # scale detectors half-angle fov (its size) with instrument half-angle
        # fov (fov size)
        self.r = self.delta_detector / (self.delta_instrument)

        self.folder_path = pkg_resources.resource_filename("nutpy", "data/")

        self.xd, self.yd = utl.read_detectors_coordinates(
            self.folder_path + self.file_name
        )

        # number of detectors
        self.nd = len(self.xd)

        # id of detectors
        self.ids = np.arange(self.nd)

        return 0

    def sensor_beta(self, beta, sensor_id):
        """
        Calculates the modified Scan Strategy parameters based on the location
        of the choosen sensor in the instrument layout.

        Parameters
        ----------
        beta : float
            Scan Strategy Parameter beta (deg)
        sensor_id : int
            Sensor id number

        Returns
        -------
        beta_mod : float
            Modified Scan Strategy Parameter beta (deg)
        """

        delta = self.delta_instrument

        # adjust beta to account for the sensor location in focal plane
        # xd and yd coordinates are normalized with delta
        xd = self.xd[sensor_id] * delta
        yd = self.yd[sensor_id] * delta

        # new beta
        beta_mod = np.sqrt((beta + xd) ** 2 + yd**2)

        return beta_mod
