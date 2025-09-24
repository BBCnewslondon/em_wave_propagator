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
        polarization="linear-y",
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


def test_circular_polarization():
    positions = np.linspace(0.0, 2.0 * np.pi, 100)
    amplitude = 1.0
    medium = Medium("test", refractive_index=1.0)  # speed = 1.0
    wavelength = 2.0 * np.pi
    time = 0.0
    phase = 0.0

    # Test right-handed circular polarization
    snapshot_right = plane_wave_snapshot(
        positions,
        time=time,
        phase=phase,
        wavelength=wavelength,
        electric_amplitude=amplitude,
        medium=medium,
        polarization="circular-right",
    )

    k = 2 * np.pi / wavelength
    omega = k * medium.propagation_speed_relative
    argument = k * positions - omega * time + phase

    expected_ey = amplitude * np.cos(argument)
    expected_ez = amplitude * np.sin(argument)
    expected_by = -(amplitude / medium.propagation_speed_relative) * np.sin(argument)
    expected_bz = (amplitude / medium.propagation_speed_relative) * np.cos(argument)

    assert_allclose(snapshot_right.electric[1], expected_ey)  # Ey
    assert_allclose(snapshot_right.electric[2], expected_ez)  # Ez
    assert_allclose(snapshot_right.magnetic[1], expected_by)  # By
    assert_allclose(snapshot_right.magnetic[2], expected_bz)  # Bz
    assert_allclose(snapshot_right.electric[0], 0.0)  # Ex should be 0
    assert_allclose(snapshot_right.magnetic[0], 0.0)  # Bx should be 0