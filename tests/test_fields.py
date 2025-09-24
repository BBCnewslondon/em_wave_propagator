import numpy as np
from numpy.testing import assert_allclose

from em_wave.fields import Medium, plane_wave_snapshot


def test_plane_wave_amplitudes_and_phase():
    positions = np.linspace(0.0, 2.0 * np.pi, 100)
    amplitude = 2.5
    medium = Medium("test", refractive_index=1/3.0)  # speed = 3.0
    wavelength = 2.0 * np.pi
    phase = 0.3

    snapshot = plane_wave_snapshot(
        positions,
        time=0.5,
        phase=phase,
        wavelength=wavelength,
        electric_amplitude=amplitude,
        medium=medium,
    )

    k = 2 * np.pi / wavelength
    omega = k * medium.propagation_speed_relative
    expected_argument = k * positions - omega * 0.5 + phase
    expected_e = amplitude * np.sin(expected_argument)
    expected_b = (amplitude / medium.propagation_speed_relative) * np.sin(expected_argument)

    assert_allclose(snapshot.electric[1], expected_e)
    assert_allclose(snapshot.magnetic[2], expected_b)
    assert_allclose(snapshot.electric[0], 0.0)
    assert_allclose(snapshot.magnetic[0], 0.0)
    assert_allclose(snapshot.magnetic[1], 0.0)