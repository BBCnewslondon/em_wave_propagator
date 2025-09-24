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
    polarization: str = "linear-y",
) -> FieldSnapshot:
    """Return the electric and magnetic fields for a monochromatic plane wave.

    The wave propagates along +x. The polarization determines the orientation
    of the electric field:
    - "linear-y": E along +y, B along +z (default)
    - "linear-z": E along +z, B along -y
    - "circular-right": right-handed circular polarization
    - "circular-left": left-handed circular polarization

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
    polarization:
        Polarization type: "linear-y", "linear-z", "circular-right", "circular-left".
    """

    if positions.ndim != 1:
        raise ValueError("positions must be a 1D array of x-coordinates")

    if polarization not in ["linear-y", "linear-z", "circular-right", "circular-left"]:
        raise ValueError(f"Invalid polarization: {polarization}")

    k = 2 * np.pi / wavelength
    propagation_speed = medium.propagation_speed_relative
    omega = k * propagation_speed
    argument = k * positions - omega * time + phase

    electric = np.zeros((3, positions.size))
    magnetic = np.zeros((3, positions.size))

    if polarization == "linear-y":
        # E along y, B along z
        electric[1] = electric_amplitude * np.sin(argument)
        magnetic[2] = (electric_amplitude / propagation_speed) * np.sin(argument)
    elif polarization == "linear-z":
        # E along z, B along -y
        electric[2] = electric_amplitude * np.sin(argument)
        magnetic[1] = -(electric_amplitude / propagation_speed) * np.sin(argument)
    elif polarization == "circular-right":
        # Right-handed circular: E rotates clockwise when viewed toward the source
        # For +x propagation: E_y = E0 cos(θ), E_z = E0 sin(θ) where θ = kx - ωt
        electric[1] = electric_amplitude * np.cos(argument)      # Ey
        electric[2] = electric_amplitude * np.sin(argument)      # Ez
        # B = (1/v) k̂ × E, for k̂ = x̂, B_y = -E_z/v, B_z = E_y/v
        magnetic[1] = -(electric_amplitude / propagation_speed) * np.sin(argument)  # By
        magnetic[2] = (electric_amplitude / propagation_speed) * np.cos(argument)   # Bz
    elif polarization == "circular-left":
        # Left-handed circular: E rotates counterclockwise when viewed toward the source
        electric[1] = electric_amplitude * np.cos(argument)      # Ey
        electric[2] = -electric_amplitude * np.sin(argument)     # Ez (negative for left-handed)
        magnetic[1] = (electric_amplitude / propagation_speed) * np.sin(argument)   # By
        magnetic[2] = (electric_amplitude / propagation_speed) * np.cos(argument)   # Bz

    return FieldSnapshot(positions=positions, electric=electric, magnetic=magnetic)


__all__ = ["FieldSnapshot", "Medium", "VACUUM", "AIR", "WATER", "GLASS", "DIAMOND", "plane_wave_snapshot"]
