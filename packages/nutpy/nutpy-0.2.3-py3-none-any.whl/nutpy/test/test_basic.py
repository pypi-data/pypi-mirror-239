import numpy as np
from numpy.testing import assert_allclose

from nutpy.mission import Nut
from nutpy.algorithms import visibility as vs
from nutpy.core.kinematics import rotations as kr
from nutpy import utilities as utl


def test_Nut_creation():
    """
    Test that Nut instance can be created succesfully
    """

    nut_test = Nut()

    assert isinstance(nut_test, Nut)


def test_profile_TAT_trace():
    """
    Test analytical TAT profile
    """

    TAT_reference = np.array([0.04254254, 0.04151692, 0.03909489, 0.03388127, 0.03229565,
                              0.03150669, 0.03092467, 0.03028924, 0.02951777, 0.02851480,
                              0.02718002, 0.02534560, 0.02237365, 0.01890918, 0.01695880,
                              0.01549216, 0.01430990, 0.01333779, 0.01250647, 0.01179800,
                              0.01117113, 0.01062701, 0.01013127, 0.00969648, 0.00930243,
                              0.00894355, 0.00861793, 0.00832125, 0.00805100, 0.00780138,
                              0.00757426, 0.00736394, 0.00716674, 0.00698582, 0.00681541,
                              0.00665857, 0.00651790, 0.00638194, 0.00625952, 0.00613986,
                              0.00603094, 0.00593226, 0.00583764, 0.00575237, 0.00566921,
                              0.00559646, 0.00552792, 0.00546061, 0.00540440, 0.00535183,
                              0.00530204, 0.00525909, 0.00521695, 0.00518391, 0.00515233,
                              0.00512489, 0.00510381, 0.00508590, 0.00507118, 0.00506318,
                              0.00505895, 0.00505839, 0.00506142, 0.00507210, 0.00508542,
                              0.00510298, 0.00512786, 0.00516192, 0.00519817, 0.00524374,
                              0.00529413, 0.00535592, 0.00542683, 0.00550697, 0.00560115,
                              0.00570842, 0.00583264, 0.00597360, 0.00614359, 0.00634141,
                              0.00657792, 0.00686656, 0.00722902, 0.00771581, 0.00844791,
                              0.00981440, 0.01033137, 0.01043490, 0.01028230, 0.00993488,
                              0.00942679, 0.00878365, 0.00801882, 0.00714467, 0.00617026,
                              0.00510169, 0.00394707, 0.00270869, 0.00139237, 0.00000000])

    _, TAT = vs.analytical_profile(SSP=[45., 50., 10., 93., 7.5],
                                   delta_instrument=7.5,
                                   delta_detector=0.5,
                                   quantity='TAT',
                                   N=100,
                                   tf=1,
                                   precession='trace',
                                   sensor_flag=False,
                                   fig_flag=False
                                   )

    result = np.allclose(TAT, TAT_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_profile_MAT_trace():
    """
    Test analytical MAT profile
    """

    MAT_reference = np.array([25.52554922, 24.91017590, 23.45695814, 25.26468511, 26.96599045,
                              27.91033625, 28.41341239, 28.50906599, 28.24425720, 27.59653566,
                              26.51043387, 24.84948309, 22.00619285, 24.03821921, 24.45773064,
                              24.65694698, 24.76062827, 24.83826769, 24.87779382, 24.91908193,
                              24.93044126, 24.95417294, 24.94186702, 24.94803052, 24.94312810,
                              24.92842309, 24.91251633, 24.89534020, 24.88009884, 24.85793663,
                              24.84269450, 24.82297559, 24.79195895, 24.76558376, 24.72832482,
                              24.69514259, 24.68016424, 24.64379096, 24.62262461, 24.57720466,
                              24.54134303, 24.51575625, 24.47705918, 24.44903151, 24.40265099,
                              24.37484829, 24.34033422, 24.28681036, 24.25917123, 24.22519475,
                              24.18170962, 24.14772301, 24.09627614, 24.06597795, 24.02186345,
                              23.97658361, 23.94067726, 23.89929377, 23.85234977, 23.81628069,
                              23.77686672, 23.73310104, 23.68410895, 23.64795417, 23.60024317,
                              23.54729087, 23.50188654, 23.47055030, 23.41920689, 23.37770875,
                              23.32280163, 23.27995126, 23.23438532, 23.18129093, 23.13413392,
                              23.08035611, 23.02495637, 22.95344117, 22.89457067, 22.81760745,
                              22.72538829, 22.60796632, 22.44096971, 22.18620162, 21.59429629,
                              21.45609495, 23.40579829, 24.56930640, 25.24754144, 25.54401466,
                              25.50602874, 25.16371668, 24.51446619, 23.54802303, 22.23434790,
                              20.51248682, 18.28719425, 15.33714777, 11.12483075,  0.00000000])

    _, MAT = vs.analytical_profile(SSP=[45., 50., 10., 93.],
                                   delta_instrument=7.5,
                                   delta_detector=0.5,
                                   quantity='MAT',
                                   N=100,
                                   tf=1,
                                   precession='trace',
                                   sensor_flag=False,
                                   fig_flag=False
                                   )

    result = np.allclose(MAT, MAT_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_profile_MAX_trace():
    """
    Test analytical MAX profile
    """

    MAX_reference = np.array([25.31069648, 28.50295443, 30.57528669, 31.79803461, 32.31261599,
                              32.33325368, 32.32636159, 32.31822549, 32.30884993, 32.29824012,
                              32.28640195, 32.27334200, 32.25906751, 32.24358636, 32.22690709,
                              32.20903887, 32.18999153, 32.16977548, 32.14840175, 32.12588197,
                              32.10222837, 32.07745370, 32.05157133, 32.02459512, 31.99653950,
                              31.96741939, 31.93725021, 31.90604787, 31.87382876, 31.84060970,
                              31.80640796, 31.77124121, 31.73512756, 31.69808545, 31.66013374,
                              31.62129162, 31.58157859, 31.54101450, 31.49961947, 31.45741393,
                              31.41441853, 31.37065420, 31.32614208, 31.28090353, 31.23496008,
                              31.18833345, 31.14104552, 31.09311830, 31.04457392, 30.99543463,
                              30.94572276, 30.89546072, 30.84467098, 30.79337603, 30.74159841,
                              30.68936067, 30.63668534, 30.58359497, 30.53011203, 30.47625899,
                              30.42205823, 30.36753208, 30.31270277, 30.25759245, 30.20222316,
                              30.14661681, 30.09079520, 30.03477997, 29.97859263, 29.92225452,
                              29.86578681, 29.80921050, 29.75254640, 29.69581512, 29.63903709,
                              29.58223251, 29.52542137, 29.46862345, 29.41185828, 29.35514518,
                              29.29850322, 29.24195124, 29.18550780, 29.12919124, 29.07301964,
                              29.01701081, 28.96118230, 28.90555141, 28.85013514, 28.79495026,
                              28.74001324, 28.68534030, 28.59118637, 28.02966565, 26.91000548,
                              25.17567353, 22.70447346, 19.23416999, 14.06785511,  0.00000000])

    _, MAX = vs.analytical_profile(SSP=[45., 50., 10., 93.],
                                   delta_instrument=7.5,
                                   delta_detector=0.5,
                                   quantity='MAX',
                                   N=100,
                                   tf=1,
                                   precession='trace',
                                   sensor_flag=False,
                                   fig_flag=False
                                   )

    result = np.allclose(MAX, MAX_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_map_TAT_trace():
    """
    Test analytical TAT map
    """

    TAT_reference = np.array([0.00536103, 0.00000000, 0.00000000, 0.00536103, 0.00560432,
                              0.00535097, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
                              0.00535097, 0.00560432, 0.01193520, 0.00549129, 0.01042733,
                              0.00000000, 0.00000000, 0.00000000, 0.01042733, 0.00549129,
                              0.01026427, 0.00510783, 0.00000000, 0.00000000, 0.00000000,
                              0.00000000, 0.00510783, 0.01026427, 0.01193520, 0.00549129,
                              0.01042733, 0.00000000, 0.00000000, 0.00000000, 0.01042733,
                              0.00549129, 0.00560432, 0.00535097, 0.00000000, 0.00000000,
                              0.00000000, 0.00000000, 0.00535097, 0.00560432, 0.00536103,
                              0.00000000, 0.00000000, 0.00536103])

    _, TAT = vs.analytical_map(SSP=[45., 50., 10., 93.],
                               delta_instrument=7.5,
                               delta_detector=0.5,
                               quantity='TAT',
                               N=100,
                               tf=1,
                               precession='None',
                               sensor_flag=False,
                               fig_flag=False,
                               nside=2,
                               units='s')

    result = np.allclose(TAT, TAT_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_map_MAT_trace():
    """
    Test analytical MAT map
    """

    MAT_reference = np.array([23.27666675,  0.00000000,  0.00000000, 23.27666675, 24.37785078,
                              23.28338725,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
                              23.28338725, 24.37785078, 24.91108648, 24.31120741, 24.48417166,
                              0.000000000,  0.00000000,  0.00000000, 24.48417166, 24.31120741,
                              24.94516861, 23.53843149,  0.00000000,  0.00000000,  0.00000000,
                              0.000000000, 23.53843149, 24.94516861, 24.91108648, 24.31120741,
                              24.48417166,  0.00000000,  0.00000000,  0.00000000, 24.48417166,
                              24.31120741, 24.37785078, 23.28338725,  0.00000000,  0.00000000,
                              0.000000000,  0.00000000, 23.28338725, 24.37785078, 23.27666675,
                              0.000000000,  0.00000000, 23.27666675])

    _, MAT = vs.analytical_map(SSP=[45., 50., 10., 93.],
                               delta_instrument=7.5,
                               delta_detector=0.5,
                               quantity='MAT',
                               N=100,
                               tf=1,
                               precession='trace',
                               sensor_flag=False,
                               fig_flag=False,
                               nside=2,
                               units='s')

    result = np.allclose(MAT, MAT_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_map_MAX_trace():
    """
    Test analytical MAT map
    """

    MAX_reference = np.array([29.80512601,  0.00000000,  0.00000000, 29.80512601, 31.19336878,
                              29.81374711,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
                              29.81374711, 31.19336878, 32.13024294, 31.11496431, 28.90962196,
                              0.000000000,  0.00000000,  0.00000000, 28.90962196, 31.11496431,
                              32.05851538, 30.13572479,  0.00000000,  0.00000000,  0.00000000,
                              0.000000000, 30.13572479, 32.05851538, 32.13024294, 31.11496431,
                              28.90962196,  0.00000000,  0.00000000,  0.00000000, 28.90962196,
                              31.11496431, 31.19336878, 29.81374711,  0.00000000,  0.00000000,
                              0.000000000,  0.00000000, 29.81374711, 31.19336878, 29.80512601,
                              0.000000000,  0.00000000, 29.80512601])

    _, MAX = vs.analytical_map(SSP=[45., 50., 10., 93.],
                               delta_instrument=7.5,
                               delta_detector=0.5,
                               quantity='MAX',
                               N=100,
                               tf=1,
                               precession='trace',
                               sensor_flag=False,
                               fig_flag=False,
                               nside=2,
                               units='s')

    result = np.allclose(MAX, MAX_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_analytic_profile_interface():
    """
    Test analytical profile interface
    """
    Nut_test = Nut(SSP=[45., 50., 10., 93., 7.5],
                   delta_instrument=7.5,
                   delta_detector=0.5,
                   mission_time=1,
                   N=100
                   )

    TAT_reference = np.array([0.04254254, 0.04151692, 0.03909489, 0.03388127, 0.03229565,
                              0.03150669, 0.03092467, 0.03028924, 0.02951777, 0.02851480,
                              0.02718002, 0.02534560, 0.02237365, 0.01890918, 0.01695880,
                              0.01549216, 0.01430990, 0.01333779, 0.01250647, 0.01179800,
                              0.01117113, 0.01062701, 0.01013127, 0.00969648, 0.00930243,
                              0.00894355, 0.00861793, 0.00832125, 0.00805100, 0.00780138,
                              0.00757426, 0.00736394, 0.00716674, 0.00698582, 0.00681541,
                              0.00665857, 0.00651790, 0.00638194, 0.00625952, 0.00613986,
                              0.00603094, 0.00593226, 0.00583764, 0.00575237, 0.00566921,
                              0.00559646, 0.00552792, 0.00546061, 0.00540440, 0.00535183,
                              0.00530204, 0.00525909, 0.00521695, 0.00518391, 0.00515233,
                              0.00512489, 0.00510381, 0.00508590, 0.00507118, 0.00506318,
                              0.00505895, 0.00505839, 0.00506142, 0.00507210, 0.00508542,
                              0.00510298, 0.00512786, 0.00516192, 0.00519817, 0.00524374,
                              0.00529413, 0.00535592, 0.00542683, 0.00550697, 0.00560115,
                              0.00570842, 0.00583264, 0.00597360, 0.00614359, 0.00634141,
                              0.00657792, 0.00686656, 0.00722902, 0.00771581, 0.00844791,
                              0.00981440, 0.01033137, 0.01043490, 0.01028230, 0.00993488,
                              0.00942679, 0.00878365, 0.00801882, 0.00714467, 0.00617026,
                              0.00510169, 0.00394707, 0.00270869, 0.00139237, 0.00000000])

    _, TAT = Nut_test.analytical_profile(quantity='TAT',
                                         precession='trace',
                                         sensor_id=None,
                                         fig_flag=False
                                         )

    result = np.allclose(TAT, TAT_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_analytic_map_interface():
    """
    Test analytical map interface
    """
    Nut_test = Nut(SSP=[45., 50., 10., 93., 7.5],
                   delta_instrument=7.5,
                   delta_detector=0.5,
                   mission_time=1,
                   N=100,
                   nside=2
                   )

    TAT_reference = np.array([0.00536103, 0.00000000, 0.00000000, 0.00536103, 0.00560432,
                              0.00535097, 0.00000000, 0.00000000, 0.00000000, 0.00000000,
                              0.00535097, 0.00560432, 0.01193520, 0.00549129, 0.01042733,
                              0.00000000, 0.00000000, 0.00000000, 0.01042733, 0.00549129,
                              0.01026427, 0.00510783, 0.00000000, 0.00000000, 0.00000000,
                              0.00000000, 0.00510783, 0.01026427, 0.01193520, 0.00549129,
                              0.01042733, 0.00000000, 0.00000000, 0.00000000, 0.01042733,
                              0.00549129, 0.00560432, 0.00535097, 0.00000000, 0.00000000,
                              0.00000000, 0.00000000, 0.00535097, 0.00560432, 0.00536103,
                              0.00000000, 0.00000000, 0.00536103])

    _, TAT = Nut_test.analytical_map(quantity='TAT',
                                     precession='None',
                                     sensor_id=None,
                                     fig_flag=False
                                     )

    result = np.allclose(TAT, TAT_reference, rtol=1e-5, atol=1e-5)

    assert result


def test_attitude_emulation_algorithm():
    """
    Check that attitude is properly emulated with the quaternions.
    The emulated attitude is compared to that obtained with the euler
    sequence.
    """

    tf = 86400

    q0 = np.random.random((4, 1))

    SSP = [40., 50., 20., 5., 7.5]

    _, q = kr.emulate_attitude(tf, 8640, q0, SSP)

    qf = q[:, [-1]]

    phi = (2 * np.pi/(SSP[3] * 60)) * tf
    theta = SSP[0] * np.pi/180
    psi = (2 * np.pi/(SSP[2] * 60)) * tf

    q_euler = kr.euler_rotation_sequence_q(phi, theta, psi, '131')

    q_euler_f = kr.quat_product(q_euler, q0)

    assert_allclose(qf, q_euler_f)


def test_attitude_emulation():
    """
    Check that attitude is properly emulated with the quaternions.
    The emulated attitude is compared to that obtained with the euler
    sequence.
    """

    tf = 86400

    q0 = np.random.random((4, 1))

    SSP = [40., 50., 20., 5., 7.5]

    nut_test = Nut(SSP=SSP, mission_time=tf, q0=q0)
    nut_test.generate_attitude()

    _, q = kr.emulate_attitude(tf, 8640, q0, SSP)

    qf = q[:, [-1]]

    q_nut = nut_test._sat.attitude_df.values[[-1], :].T

    assert_allclose(qf, q_nut)


def test_sensor_analytic():
    """
    Check that the analytical profile for sensors is carried out succesfully
    """

    upm = Nut(SSP=[45, 55, 10, 93])

    _, _ = upm.analytical_profile(sensor_id=200, quantity='MAT')

    assert True


def test_numeric_analysis():
    """
    Check that the numerical analysis is carried out succesfully
    """

    upm = Nut(SSP=[45, 55, 10, 93])

    result = upm.numerical_analysis()

    assert result == 0


def test_TAT():
    """
    Check that the numerical and analytical results for TAT are equal within a
    tolerance
    """

    upm = Nut(SSP=[45, 55, 10, 93], delta_instrument=7.5, nside=32, N=100, dT=1, mission_time=86400)

    upm.numerical_analysis()

    _, TAT_n = upm.numerical_profile(quantity="TAT", fig_flag=False)

    _, TAT_a = upm.analytical_profile(quantity="TAT", fig_flag=False)

    rmse = 100 * utl.rmse(TAT_n, TAT_a)/86400

    test_result = rmse < 0.05

    assert test_result


def test_MAT():
    """
    Check that the numerical and analytical results for MAT are equal within a
    tolerance
    """

    upm = Nut(SSP=[45, 55, 10, 93], delta_instrument=7.5, nside=32, N=100, dT=1, mission_time=86400)

    upm.numerical_analysis()

    _, MAT_n = upm.numerical_profile(quantity="MAT", fig_flag=False)

    _, MAT_a = upm.analytical_profile(quantity="MAT", fig_flag=False)

    rmse = utl.rmse(MAT_n, MAT_a)

    test_result = rmse < 1

    assert test_result


def test_MAX():
    """
    Check that the numerical and analytical results for MAX are equal within a
    tolerance
    """

    upm = Nut(SSP=[45, 55, 10, 93], delta_instrument=7.5, nside=32, N=100, dT=1, mission_time=86400)

    upm.numerical_analysis()

    _, MAX_n = upm.numerical_profile(quantity="MAX", fig_flag=False)

    _, MAX_a = upm.analytical_profile(quantity="MAX", fig_flag=False)

    rmse = utl.rmse(MAX_n, MAX_a)

    test_result = rmse < 2

    assert test_result
