#!/usr/bin/env python3
"""
Build script for creating executable files for NumPad Typing Test.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def get_build_command():
    """Get the PyInstaller command."""
    system = platform.system()

    base_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name",
        "NumPad",
        "--add-data",
        "core.py:.",
    ]

    # Add platform-specific options
    if system == "Windows":
        # Check if icon and version files exist
        if os.path.exists("icon.ico"):
            base_cmd.extend(["--icon=icon.ico"])
        if os.path.exists("version.txt"):
            base_cmd.extend(["--version-file=version.txt"])
    elif system == "Darwin":  # macOS
        if os.path.exists("icon.icns"):
            base_cmd.extend(["--icon=icon.icns"])

    base_cmd.append("numpad.py")
    return base_cmd


def clean_build_artifacts():
    """Clean up build artifacts from previous builds."""
    artifacts = ["build", "dist", "__pycache__"]

    for artifact in artifacts:
        if os.path.exists(artifact):
            if os.path.isdir(artifact):
                shutil.rmtree(artifact)
                print(f"Removed {artifact} directory")

    # Remove .spec files
    for spec_file in Path(".").glob("*.spec"):
        os.remove(spec_file)
        print(f"Removed {spec_file}")


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyInstaller

        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("Error: PyInstaller is not installed.")
        print("Install it with: pip install pyinstaller")
        return False

    try:
        import tkinter

        print("Tkinter is available")
    except ImportError:
        print("Error: Tkinter is not available.")
        return False

    return True


def build_executable():
    """Build the executable using PyInstaller."""
    if not check_dependencies():
        return False

    print("Building executable...")
    print(f"Platform: {platform.system()}")

    # Clean previous builds
    clean_build_artifacts()

    # Get build command
    cmd = get_build_command()
    print(f"Running: {' '.join(cmd)}")

    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")

        # Show output location
        dist_dir = Path("dist")
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*"))
            if exe_files:
                print(f"Executable created: {exe_files[0]}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main function."""
    print("NumPad - Build Script")
    print("=" * 20)

    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        print("Cleaning build artifacts...")
        clean_build_artifacts()
        print("Clean completed.")
        return

    success = build_executable()

    if success:
        print("\nBuild completed successfully!")
        print("The executable can be found in the 'dist' directory.")
    else:
        print("\nBuild failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
