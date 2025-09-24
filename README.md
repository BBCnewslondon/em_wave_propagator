# EM Wave Propagator

Visualize a transverse electromagnetic plane wave with perpendicular electric and magnetic field oscillations using Matplotlib.

## Features

- 3D animation highlighting propagation direction (x) with oscillating `E` (y) and `B` (z) fields
- Configurable wavelength, amplitude, propagation speed, and duration
- Support for different propagation mediums (vacuum, air, water, glass, diamond)
- Multiple polarization types: linear (y/z), circular (right/left-handed)
- Comparison mode to visualize waves in multiple mediums simultaneously
- Minimal CLI with optional export to video/gif
- Pure Python + Matplotlib, tested with `pytest`

## Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

# Animate wave in water
python main.py --medium water

# Show circular polarization
python main.py --polarization circular-right

# Compare waves in all mediums simultaneously
python main.py --compare

# Headless usage (no GUI window)
python main.py --no-show --save wave.gif
```

Use the CLI flags (run `python -m em_wave.cli --help`) to tweak the wave parameters. If you want to save the animation, pass `--save output.mp4`. Saving to MP4 requires FFmpeg to be installed and on your PATH.

When running without a display (e.g., on CI servers), add `--no-show` so Matplotlib switches to a non-interactive backend. Pair it with `--save` to export the animation.

## Running Tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

## Project Structure

```
├── README.md
├── main.py
├── pyproject.toml
├── requirements.txt
├── src
│   └── em_wave
│       ├── __init__.py
│       ├── animation.py
│       ├── cli.py
│       └── fields.py
└── tests
    └── test_fields.py
```

## Next Steps

- Adjust color schemes or add vector arrows for additional clarity
- Extend the animation to display polarization changes or standing waves
