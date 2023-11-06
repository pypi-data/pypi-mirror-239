from nutpy.core.satellite import Satellite
import nutpy.algorithms.visibility as vs
import nutpy.postprocessing.pgraph as pg
import nutpy.utilities as utl

import pandas as pd
import warnings


class Nut:
    """
    Interface with the user

    Attributes
    ----------
    name : str
        Name of the mission
    Tsim : float
        Period of time considered for the numerical analysis
    dT : float
        Step time used for the numerical analysis
    sensor_id : int
        Sensor id number
    SSP : list (5) of floats
        Scan strategy parameters [alpha (deg), beta (deg), spin period
        (min), precesion period (min), delta (deg)]
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
    """

    # default options
    default_config = {
        "name": "Default_mission",
        "SSP": [45.0, 50.0, 10.0, 93.0],
        "Tsim": 3600,
        "dT": 2,
        "N": 100,
        "Nth": 360,
        "nside": 16,
        "units": "s",
        "bar": True,
        "detailed": False,
        "dense": False,
        "annual": False,
    }

    def __init__(self, **kwargs):
        """
        Constructor

        Parameters
        ----------
        name : str
            Name of the mission
        """

        config = {**self.default_config, **kwargs}

        self.name = config["name"]
        self._Tsim = config["Tsim"]
        self._dT = config["dT"]
        self.N = config["N"]
        self.Nth = config["Nth"]
        self._nside = config["nside"]
        self.units = config["units"]
        self.bar = config["bar"]
        self._detailed = config["detailed"]
        self._dense = config["dense"]
        self._annual = config["annual"]

        self._sat = Satellite(**kwargs)

        self._alpha = self._sat.SSP[0]

        self.numerical_results_df = pd.DataFrame()
        self.sensors_results_global_df = pd.DataFrame()
        self.numerical_analysis_status = False

    @property
    def SSP(self):
        return self._sat.SSP

    @property
    def delta_instrument(self):
        return self._sat.inst.delta_instrument

    @property
    def delta_detector(self):
        return self._sat.inst.delta_detector

    @property
    def Tsim(self):
        return self._Tsim

    @property
    def dT(self):
        return self._dT

    @property
    def nside(self):
        return self._nside

    @property
    def border_angle(self):
        return self.SSP[0] + self.SSP[1] + self.delta_instrument

    def SSP_sensor(self, sensor_id):
        return (
            self._sat.alpha,
            self._sat.inst.sensor_beta(self._sat.beta, sensor_id),
            self._sat.Tspin,
            self._sat.Tprec,
        )

    def check_sensor_flag(self, sensor_id):
        if sensor_id is None:
            SSP = self.SSP
            sensor_flag = False
        else:
            SSP = self.SSP_sensor(sensor_id)
            sensor_flag = True

        return SSP, sensor_flag

    def check_attitude(self):
        """
        Checks if the generated attitude corresponds to the mission
        parameters
        """

        pass

    def check_numerical_analysis(self):
        """
        Checks if the numerical analysis has been performed
        """

        if not self.numerical_analysis_status:
            raise Exception("Numerical analysis has not been carried out yet")
        else:
            pass

        return 0

    def check_coherence_criteria(self):
        """
        Checks the coherence criteria is fullfilled
        """

        if utl.coherence_criteria(self.SSP, self._nside, self._dT):
            pass
        else:
            warnings.warn(
                "dT is too large for the analysis, results may not be accurate"
            )

        return 0

    def check_coherence_criteria_detectors(self):
        """
        Checks the coherence criteria for the detectors is fullfilled
        """

        if utl.coherence_criteria_detectors(self.SSP, self.delta_detector, self._dT):
            pass
        else:
            warnings.warn(
                "dT is too large for the analysis, results may not be accurate"
            )

        return 0

    def check_memory_usage(self):
        """
        Checks if memory usage is too high
        """

        memory_usage = utl.estimate_memory(self._nside, self._sat.inst.nd)[0]

        if memory_usage > 1:
            warnings.warn(
                "Under this parameters, detailed numeric analysis will require more than 1 GB of memory"
            )

        return 0

    def analytical_profile(
        self, quantity="TAT", precession="trace", sensor_id=None, fig_flag=True
    ):
        """
        Calculates analytically the demanded quantity from the temporal
        analysis for the instrument as a function of the angle regarding the
        precession axis

        Parameters
        ----------
        N : int
            Resolution of results
        tf : float
            Total time considered
        quantity : str
            Quantity to be computed
        fig_flag : bool
            If True, figure is returned
        precession : str
            Method to be used to account for precession

        Returns
        -------
        fig : matplotlib figure
            Figure of profile
        T : ndarray (N)
            Results of calculations (profile)
        """

        SSP, sensor_flag = self.check_sensor_flag(sensor_id)

        fig, T = vs.analytical_profile(
            SSP,
            self.delta_instrument,
            self.delta_detector,
            quantity,
            self.N,
            self.Tsim,
            precession=precession,
            annual=self._annual,
            sensor_flag=sensor_flag,
            fig_flag=fig_flag,
        )

        return fig, T

    def analytical_map(
        self, quantity="TAT", precession="trace", sensor_id=None, fig_flag=True
    ):
        """
        Calculates analytically the demanded quantity for all the celestial
        sphere and plots it.

        Parameters
        ----------
        quantity : str
            Quantity to be computed
        precession : str
            Method to be used to account for precession
        fig_flag : bool
            If True, figure is returned

        Returns
        -------
        fig : matplotlib figure
            Figure of profile
        data : ndarray (N)
            Results of calculations (value per pixel for Healpix scheme)
        """

        SSP, sensor_flag = self.check_sensor_flag(sensor_id)

        fig, data = vs.analytical_map(
            SSP,
            self.delta_instrument,
            self.delta_detector,
            quantity,
            self.N,
            self.Tsim,
            precession=precession,
            annual=self._annual,
            sensor_flag=sensor_flag,
            fig_flag=fig_flag,
            nside=self.nside,
            units=self.units,
        )

        return fig, data

    def generate_attitude(self):
        """
        Emulates satellite attitude motion
        """

        self._sat.generate_attitude(
            self._Tsim, self._dT, self._sat.q0, self.SSP, self._annual
        )

        return 0

    def numerical_analysis(self):
        """
        Performs numerical analysis.

        Computes which sensors are viewed and for how long

        This analysis produces two sets of data: sensors_results_global_df and sensors_results_detailed_dict.
        The former stores the Figures of Merit (FOM) of computed for each point in the sky. The second
        stores the FOM of each detectors for each case point in the sky (requires dense=True)
        """

        self.check_coherence_criteria()

        if self._detailed:
            self.check_coherence_criteria_detectors()
            self.check_memory_usage()

        self.generate_attitude()

        (
            self.numerical_results_df,
            self.numerical_results_detailed_df,
        ) = vs.numerical_analysis(
            self._sat.inst,
            self._nside,
            self.bar,
            self._detailed,
            self._dense,
            self.border_angle,
            self._annual,
        )

        self.numerical_analysis_status = True

        return 0

    def numerical_profile(
        self, quantity="TAT", unit="s", fig_flag=True, sensor_id=None
    ):
        """
        Calculates analytically the demanded quantity from the temporal
        analysis for the instrument as a function of the angle regarding the
        precession axis

        Parameters
        ----------
        N : int
            Resolution of results
        tf : float
            Total time considered [s]
        quantity : str
            Quantity to be computed
        fig_flag : bool
            If True, figure is returned
        precession : str
            Method to be used to account for precession

        Returns
        -------
        fig : matplotlib figure
            Figure of profile
        T : ndarray (N)
            Results of calculations (profile)
        """

        self.check_numerical_analysis()

        fig, T = vs.numerical_profile(
            self, quantity, unit, self.N, self.Nth, fig_flag, sensor_id
        )

        return fig, T

    def numerical_map(self, quantity="TAT", units="s", sensor_id=None, **kwargs):
        """
        Plot temporal analysis results

        Parameters
        ----------
        map_type : str
            Result to be plotted
        N : int
            Mesh for plotting

        Returns
        -------
        fig :  matplotlib figure
            Plotted figure

        """

        fig, data = vs.numerical_map(self, quantity, self.N, units, sensor_id, **kwargs)

        return fig, data

    def plot_focal_plane(
        self, cases_dict=None, case_id=None, quantity="Viewed", numbered=False
    ):
        """
        Plots focal plane results for a given case (pixel in sky)

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

        fig, ax = pg.plot_focal_plane(
            self._sat.inst.xd,
            self._sat.inst.yd,
            self._sat.inst.r,
            cases_dict,
            case_id,
            quantity,
            numbered,
        )

        return fig, ax

    def plot_trace(self):
        """
        Plots trace of the instrument over the sky (orthographic projection over the
        XZ-plane)

        Returns
        -------
        fig : matplotlib figure
            Figure of profile
        ax : axes
            Matplotlib figure axes of sensor array and FOV
        """

        fig, ax = pg.plot_trace(self.SSP, self.Tsim, self.dT)

        return fig, ax

    def visibility_results(self, quantity, sensor_id):
        """
        Retrieves visibility results and completes them

        Returns
        -------
        visibility_global_results_df : pandas DataFrame
            Results of visibility analysis
        """

        if sensor_id is None:
            if quantity in ["SGA", "PVS"] and (not self._detailed):
                raise Exception("Detailed results not present")
            else:
                data = self.numerical_results_df[quantity].values

        else:
            if not (self._detailed and self._dense):
                raise Exception("Detailed results not present")

            df = self.numerical_results_detailed_df
            data = df[df["sensor_id"] == sensor_id][quantity].values

        return data
