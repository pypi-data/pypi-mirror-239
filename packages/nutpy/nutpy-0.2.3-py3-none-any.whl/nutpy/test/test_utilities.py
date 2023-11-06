from nutpy import utilities as utl

import numpy as np


def test_coherence_criteria():
    SSP = [45, 50, 10, 93]

    result_1 = utl.coherence_criteria(SSP, 32, 1)

    result_2 = not utl.coherence_criteria(SSP, 32, 2)

    assert result_1 and result_2


def test_coherence_criteria_detectors():
    SSP = [45, 50, 10, 93]

    result_1 = utl.coherence_criteria_detectors(SSP, 0.25, 0.1)

    result_2 = not utl.coherence_criteria_detectors(SSP, 0.25, 0.2)

    assert result_1 and result_2


def test_estimate_memory():
    memory_usage = utl.estimate_memory(128, 400)[0]

    assert np.isclose(1.318359375, memory_usage)
