"""Utilities for computing electromagnetic plane wave fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class Medium:
    """Properties of a propagation medium."""

    name: str
    refractive_index: float
    permittivity_relative: float = 1.0  # ε_r
    permeability_relative: float = 1.0  # μ_r

    @property
    def propagation_speed_relative(self) -> float:
        """Relative propagation speed compared to vacuum (c=1)."""
        return 1.0 / self.refractive_index

    @property
    def impedance_relative(self) -> float:
        """Relative impedance compared to vacuum."""
        return np.sqrt(self.permeability_relative / self.permittivity_relative)


# Common mediums
VACUUM = Medium("Vacuum", 1.0, 1.0, 1.0)
AIR = Medium("Air", 1.0003, 1.0006, 1.0000004)
WATER = Medium("Water", 1.33, 1.77, 1.0)
GLASS = Medium("Glass", 1.5, 2.25, 1.0)
DIAMOND = Medium("Diamond", 2.4, 5.76, 1.0)


@dataclass(frozen=True)
class FieldSnapshot:
    """Snapshot of the electric and magnetic fields along a 1D slice."""

    positions: np.ndarray  # shape (N,)
    electric: np.ndarray  # shape (3, N)
    magnetic: np.ndarray  # shape (3, N)

    def components(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return individual electric field components (Ex, Ey, Ez)."""

        return tuple(self.electric[i] for i in range(3))

    def magnetic_components(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return individual magnetic field components (Bx, By, Bz)."""

        return tuple(self.magnetic[i] for i in range(3))


def plane_wave_snapshot(
    positions: np.ndarray,
    time: float,
    phase: float = 0.0,
    wavelength: float = 1.0,
    electric_amplitude: float = 1.0,
    medium: Medium = VACUUM,
) -> FieldSnapshot:
    """Return the electric and magnetic fields for a monochromatic plane wave.

    The wave propagates along +x, the electric field oscillates along +y, and the
    magnetic field oscillates along +z. The amplitudes follow the relation
    |B| = |E| / v where v is the propagation speed in the medium.

    Parameters
    ----------
    positions:
        1D array of spatial sample points along the propagation direction (x).
    time:
        Time at which to evaluate the fields.
    phase:
        Optional additional phase in radians.
    wavelength:
        Spatial wavelength of the wave.
    electric_amplitude:
        Peak amplitude of the electric field in arbitrary units.
    medium:
        The propagation medium.
    """

    if positions.ndim != 1:
        raise ValueError("positions must be a 1D array of x-coordinates")

    k = 2 * np.pi / wavelength
    propagation_speed = medium.propagation_speed_relative
    omega = k * propagation_speed
    argument = k * positions - omega * time + phase

    electric = np.zeros((3, positions.size))
    magnetic = np.zeros((3, positions.size))

    electric[1] = electric_amplitude * np.sin(argument)
    magnetic_amplitude = electric_amplitude / propagation_speed
    magnetic[2] = magnetic_amplitude * np.sin(argument)

    return FieldSnapshot(positions=positions, electric=electric, magnetic=magnetic)


__all__ = ["FieldSnapshot", "Medium", "VACUUM", "AIR", "WATER", "GLASS", "DIAMOND", "plane_wave_snapshot"]
