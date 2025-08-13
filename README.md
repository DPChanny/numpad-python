# NumPad

A cross-platform GUI application for practicing numeric keypad typing skills.

## Quick Start

### Windows

1. Double-click `build_windows.bat`
2. The executable will be created in the `dist` folder

### Linux/macOS

1. Run `./build_unix.sh`
2. The executable will be created in the `dist` folder

### Manual Setup

```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate numpad

# Run application
python numpad.py

# Build executable
python build.py
```

## Features

- Real-time typing accuracy measurement
- Numbers Per Minute (NPM) calculation
- Cross-platform support (Windows, macOS, Linux)
- Standalone executable generation

## Controls

- **Start Test**: Begin typing session
- **Reset**: Clear statistics
- **Stop Test**: End session and show results
- **Enter**: Start test (keyboard shortcut)
- **Escape**: Stop test (keyboard shortcut)

## Project Structure

```
NumPad/
├── core.py              # Core typing test logic
├── numpad.py            # GUI application
├── build.py             # Build script
├── build_windows.bat    # Windows build script
├── build_unix.sh        # Linux/macOS build script
├── environment.yml      # Conda environment
└── README.md           # This file
```
