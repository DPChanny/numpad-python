#!/usr/bin/env python3
"""
Build script for creating executable files for NumPad Typing Test.
Supports the new project structure with sources/ and builds/ directories.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_sources_dir():
    """Get the sources directory."""
    return get_project_root() / "sources"


def get_assets_dir():
    """Get the assets directory."""
    return get_project_root() / "assets"


def get_build_command():
    """Get the PyInstaller command with updated paths."""
    system = platform.system()
    sources_dir = get_sources_dir()
    assets_dir = get_assets_dir()
    project_root = get_project_root()

    base_cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name",
        "NumPad",
        "--distpath",
        str(project_root / "dist"),
        "--workpath",
        str(project_root / "build"),
        "--specpath",
        str(project_root),
    ]

    # Add all source files as additional data
    source_files = ["core.py", "characters.py", "style.py", "widgets.py"]
    for source_file in source_files:
        source_path = sources_dir / source_file
        if source_path.exists():
            base_cmd.extend(["--add-data", f"{source_path}:."])

    # Add platform-specific options
    if system == "Windows":
        icon_path = assets_dir / "icon.ico"
        version_path = assets_dir / "version.txt"

        if icon_path.exists():
            base_cmd.extend(["--icon", str(icon_path)])
        if version_path.exists():
            base_cmd.extend(["--version-file", str(version_path)])

    elif system == "Darwin":  # macOS
        icon_path = assets_dir / "icon.icns"
        if icon_path.exists():
            base_cmd.extend(["--icon", str(icon_path)])

    # Main entry point
    main_script = sources_dir / "numpad.py"
    base_cmd.append(str(main_script))

    return base_cmd


def clean_build_artifacts():
    """Clean up build artifacts from previous builds."""
    project_root = get_project_root()

    # Clean standard PyInstaller directories
    artifacts = ["build", "dist", "__pycache__"]

    for artifact_name in artifacts:
        artifact_path = project_root / artifact_name
        if artifact_path.exists():
            if artifact_path.is_dir():
                shutil.rmtree(artifact_path)
                print(f"Removed {artifact_path}")
            else:
                artifact_path.unlink()
                print(f"Removed {artifact_path}")

    # Remove .spec files from project root
    for spec_file in project_root.glob("*.spec"):
        spec_file.unlink()
        print(f"Removed {spec_file}")

    # Clean __pycache__ directories recursively
    for pycache in project_root.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            print(f"Removed {pycache}")


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyInstaller

        print(f"✓ PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("✗ Error: PyInstaller is not installed.")
        print("  Install it with: pip install pyinstaller")
        return False

    try:
        import tkinter

        print("✓ Tkinter is available")
    except ImportError:
        print("✗ Error: Tkinter is not available.")
        return False

    return True


def check_project_structure():
    """Check if the project structure is correct."""
    project_root = get_project_root()
    sources_dir = get_sources_dir()
    assets_dir = get_assets_dir()

    print("Checking project structure...")

    # Check required directories
    required_dirs = [sources_dir, assets_dir]
    for directory in required_dirs:
        if not directory.exists():
            print(f"✗ Missing directory: {directory}")
            return False
        print(f"✓ Found directory: {directory}")  # Check required source files
    required_files = [
        "numpad.py",
        "core.py",
        "characters.py",
        "style.py",
        "widgets.py",
    ]
    for file_name in required_files:
        file_path = sources_dir / file_name
        if not file_path.exists():
            print(f"✗ Missing source file: {file_path}")
            return False
        print(f"✓ Found source file: {file_name}")

    return True


def build_executable():
    """Build the executable using PyInstaller."""
    print("NumPad - Build Script")
    print("=" * 40)

    # Change to project root
    os.chdir(get_project_root())

    if not check_project_structure():
        print("\n✗ Project structure check failed.")
        return False

    if not check_dependencies():
        print("\n✗ Dependency check failed.")
        return False

    print(f"\nBuilding executable...")
    print(f"Platform: {platform.system()}")
    print(f"Architecture: {platform.machine()}")

    # Clean previous builds
    print("\nCleaning previous builds...")
    clean_build_artifacts()

    # Get build command
    cmd = get_build_command()
    print(f"\nRunning PyInstaller...")
    print(f"Command: {' '.join(cmd)}")

    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("\n✓ Build completed successfully!")

        # Show output location
        project_root = get_project_root()
        dist_dir = project_root / "dist"
        exe_files = list(dist_dir.glob("NumPad*"))
        if exe_files:
            exe_file = exe_files[0]
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"✓ Executable created: {exe_file}")
            print(f"✓ File size: {file_size:.1f} MB")

        # Clean up temporary build directory
        build_dir = project_root / "build"
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print("✓ Cleaned up temporary files")

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        if e.stderr:
            print(f"Error output:\n{e.stderr}")
        return False


def create_version_info():
    """Create a version info file for Windows builds."""
    assets_dir = get_assets_dir()
    version_file = assets_dir / "version.txt"

    if not version_file.exists():
        version_content = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'GitHub Copilot Test Project'),
           StringStruct(u'FileDescription', u'NumPad Typing Test'),
           StringStruct(u'FileVersion', u'1.0.0.0'),
           StringStruct(u'InternalName', u'NumPad'),
           StringStruct(u'LegalCopyright', u'© 2025 GitHub Copilot Test Project'),
           StringStruct(u'OriginalFilename', u'NumPad.exe'),
           StringStruct(u'ProductName', u'NumPad Typing Test'),
           StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
        version_file.write_text(version_content, encoding="utf-8")
        print(f"✓ Created version info file: {version_file}")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "clean":
            print("Cleaning build artifacts...")
            clean_build_artifacts()
            print("✓ Clean completed.")
            return
        elif sys.argv[1] == "version":
            print("Creating version info...")
            create_version_info()
            return

    # Create version info for Windows
    if platform.system() == "Windows":
        create_version_info()

    success = build_executable()

    if success:
        print(f"\n🎉 Build completed successfully!")
        print(f"📁 The executable can be found in the 'dist' directory.")
        print(f"🚀 You can now distribute the NumPad application!")
    else:
        print(f"\n💥 Build failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
