"""Matplotlib animation helpers for visualizing electromagnetic waves."""

from __future__ import annotations

from typing import Any, Optional, Tuple, cast

import numpy as np
from matplotlib import animation, pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  # type: ignore
from mpl_toolkits.mplot3d.art3d import Line3D

from .fields import plane_wave_snapshot, Medium, VACUUM


def build_em_wave_animation(
    duration: float = 8.0,
    fps: int = 30,
    spatial_extent: Tuple[float, float] = (0.0, 4.0 * np.pi),
    num_points: int = 200,
    wavelength: float = 2.0 * np.pi,
    electric_amplitude: float = 1.0,
    medium: Medium = VACUUM,
    mediums: Optional[list[Medium]] = None,
    phase: float = 0.0,
    polarization: str = "linear-y",
    save_path: Optional[str] = None,
) -> Tuple[Figure, animation.FuncAnimation]:
    """Create a Matplotlib animation depicting an EM plane wave.

    If mediums is provided, shows a comparison of waves in different mediums.
    Otherwise, shows a single wave in the specified medium.

    Returns the figure and ``FuncAnimation`` instance. If ``save_path`` is
    provided, the animation will be exported using Matplotlib's writers.
    """

    if fps <= 0:
        raise ValueError("fps must be positive")

    start, stop = spatial_extent
    if stop <= start:
        raise ValueError("spatial_extent must have stop > start")

    # Determine which mediums to display
    if mediums is not None:
        display_mediums = mediums
        comparison_mode = True
    else:
        display_mediums = [medium]
        comparison_mode = False

    positions = np.linspace(start, stop, num_points)
    frames = int(duration * fps)
    dt = 1.0 / fps

    fig = plt.figure(figsize=(12, 6) if comparison_mode else (9, 5.5))
    ax = cast(Axes3D, fig.add_subplot(111, projection="3d"))
    
    if comparison_mode:
        ax.set_title("EM Wave Comparison: Different Propagation Mediums")
    else:
        ax.set_title(f"Electromagnetic Plane Wave in {medium.name}")
    
    ax.set_xlabel("x (propagation)")
    ax.set_ylabel("E field (y)")
    ax.set_zlabel("B field (z)")

    # Define colors for different mediums
    colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple', 'tab:brown']
    
    # Create line objects for each medium
    e_lines = []
    b_lines = []
    for i, med in enumerate(display_mediums):
        color = colors[i % len(colors)]
        e_line = cast(Line3D, ax.plot([], [], [], color=color, lw=2, 
                                     label=f"E ({med.name})")[0])
        b_line = cast(Line3D, ax.plot([], [], [], color=color, lw=2, linestyle='--',
                                     label=f"B ({med.name})")[0])
        e_lines.append(e_line)
        b_lines.append(b_line)
    
    if comparison_mode:
        ax.legend(loc="upper right")
    else:
        ax.legend(loc="upper right")
    ax.view_init(elev=22.5, azim=-60)

    # Set axis limits with some padding for clarity.
    max_magnetic_amplitude = max(med.propagation_speed_relative for med in display_mediums)
    padding = 0.15 * electric_amplitude
    ax.set_xlim(start, stop)
    
    if polarization == "linear-z":
        ax.set_ylim(-electric_amplitude / max_magnetic_amplitude - padding, 
                    electric_amplitude / max_magnetic_amplitude + padding)
        ax.set_zlim(-electric_amplitude - padding, electric_amplitude + padding)
    elif polarization.startswith("circular"):
        # For circular polarization, E moves in y-z plane
        ax.set_ylim(-electric_amplitude - padding, electric_amplitude + padding)
        ax.set_zlim(-electric_amplitude - padding, electric_amplitude + padding)
    else:  # linear-y (default)
        ax.set_ylim(-electric_amplitude - padding, electric_amplitude + padding)
        ax.set_zlim(-electric_amplitude / max_magnetic_amplitude - padding, 
                    electric_amplitude / max_magnetic_amplitude + padding)

    time_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)

    def init():
        for e_line, b_line in zip(e_lines, b_lines):
            e_line.set_data_3d([], [], [])
            b_line.set_data_3d([], [], [])
        time_text.set_text("")
        return e_lines + b_lines + [time_text]

    def update(frame_index: int):
        time = frame_index * dt
        for i, (med, e_line, b_line) in enumerate(zip(display_mediums, e_lines, b_lines)):
            snapshot = plane_wave_snapshot(
                positions,
                time=time,
                phase=phase,
                wavelength=wavelength,
                electric_amplitude=electric_amplitude,
                medium=med,
                polarization=polarization,
            )

            if polarization.startswith("linear"):
                # For linear polarization, plot E and B in their respective planes
                if polarization == "linear-y":
                    e_y = snapshot.electric[1]  # Ey
                    b_z = snapshot.magnetic[2]  # Bz
                    zeros = np.zeros_like(positions)
                    e_line.set_data_3d(positions, e_y, zeros)
                    b_line.set_data_3d(positions, zeros, b_z)
                elif polarization == "linear-z":
                    e_z = snapshot.electric[2]  # Ez
                    b_y = snapshot.magnetic[1]  # By
                    zeros = np.zeros_like(positions)
                    e_line.set_data_3d(positions, zeros, e_z)
                    b_line.set_data_3d(positions, b_y, zeros)
            else:  # circular polarization
                # For circular polarization, show the projection in y-z plane
                # Plot E vector as a combination of Ey and Ez
                e_y = snapshot.electric[1]
                e_z = snapshot.electric[2]
                b_y = snapshot.magnetic[1]
                b_z = snapshot.magnetic[2]
                zeros = np.zeros_like(positions)
                e_line.set_data_3d(positions, e_y, e_z)
                b_line.set_data_3d(positions, b_y, b_z)

        time_text.set_text(f"t = {time:.2f} s")
        return e_lines + b_lines + [time_text]

    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=frames,
        interval=1000.0 / fps,
        blit=False,
        repeat=True,
    )

    if save_path:
        anim.save(save_path, fps=fps)

    return fig, anim


def show_em_wave_animation(*, show: bool = True, close_after: bool = False, **kwargs: Any) -> Tuple[Figure, animation.FuncAnimation]:
    """Build the EM wave animation, optionally display it, and return the artifacts."""

    save_path = kwargs.get("save_path")
    fig, anim = build_em_wave_animation(**kwargs)
    if not show and save_path is None:
        # Flag the animation as if it started so matplotlib does not warn when it is
        # garbage-collected without ever being displayed or saved.
        anim._draw_was_started = True  # type: ignore[attr-defined]
    if show:
        plt.show(block=True)
    elif close_after:
        plt.close(fig)

    return fig, anim


__all__ = ["build_em_wave_animation", "show_em_wave_animation"]
