"""Command-line interface for the EM wave animation demo."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .fields import AIR, DIAMOND, GLASS, Medium, VACUUM, WATER


def get_medium(name: str) -> Medium:
    """Return the Medium instance for the given name."""
    mediums = {
        "vacuum": VACUUM,
        "air": AIR,
        "water": WATER,
        "glass": GLASS,
        "diamond": DIAMOND,
    }
    return mediums[name]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Animate an electromagnetic plane wave with perpendicular E and B fields in different mediums.",
    )
    parser.add_argument("--duration", type=float, default=8.0, help="Animation duration in seconds.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the animation.")
    parser.add_argument(
        "--extent",
        type=float,
        nargs=2,
        metavar=("START", "STOP"),
        default=(0.0, 4.0),
        help="Spatial extent along the propagation direction (x-axis).",
    )
    parser.add_argument("--wavelength", type=float, default=1.0, help="Wavelength of the wave.")
    parser.add_argument("--amplitude", type=float, default=1.0, help="Electric field amplitude.")
    parser.add_argument(
        "--medium",
        choices=["vacuum", "air", "water", "glass", "diamond"],
        default="vacuum",
        help="Propagation medium.",
    )
    parser.add_argument("--phase", type=float, default=0.0, help="Initial phase offset in radians.")
    parser.add_argument(
        "--points",
        type=int,
        default=200,
        help="Number of spatial samples used to draw the wave.",
    )
    parser.add_argument(
        "--save",
        type=Path,
        default=None,
        help="Optional output file (mp4/gif) to save the animation before showing it.",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Show comparison of waves in all available mediums simultaneously.",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Render the animation without opening a GUI window (useful for headless environments).",
    )
    return parser


def main(arguments: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(arguments)

    if args.no_show or args.save is not None:
        import matplotlib

        matplotlib.use("Agg")  # Use a non-interactive backend when not displaying.

    from .animation import show_em_wave_animation

    if args.compare:
        mediums_list = [VACUUM, AIR, WATER, GLASS, DIAMOND]
        _fig, _ = show_em_wave_animation(
            duration=args.duration,
            fps=args.fps,
            spatial_extent=(args.extent[0], args.extent[1]),
            wavelength=args.wavelength,
            electric_amplitude=args.amplitude,
            mediums=mediums_list,
            phase=args.phase,
            num_points=args.points,
            save_path=str(args.save) if args.save is not None else None,
            show=not args.no_show,
            close_after=args.no_show,
        )
    else:
        _fig, _ = show_em_wave_animation(
            duration=args.duration,
            fps=args.fps,
            spatial_extent=(args.extent[0], args.extent[1]),
            wavelength=args.wavelength,
            electric_amplitude=args.amplitude,
            medium=get_medium(args.medium),
            phase=args.phase,
            num_points=args.points,
            save_path=str(args.save) if args.save is not None else None,
            show=not args.no_show,
            close_after=args.no_show,
        )

    if args.save is not None:
        print(f"Animation saved to {args.save}")


if __name__ == "__main__":
    main()
