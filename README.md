# NumPad Typing Test

A cross-platform GUI application for practicing numeric keypad typing skills. This project was created as a **GitHub Copilot test project** to demonstrate AI-assisted development capabilities.

## ✨ Features

- **Cross-Platform Support**: Windows, macOS, and Linux
- **Modern GUI**: Built with Tkinter for native look and feel
- **Real-Time Statistics**: NPM (Numbers Per Minute) tracking
- **Visual Feedback**: Color-coded character highlighting
  - 🔵 Blue: Current character to type
  - 🟢 Green: Correctly typed characters
  - 🔴 Red: Incorrectly typed characters
- **Extended Character Set**: Supports digits (0-9) and mathematical operators (+, -, /, \*, .)
- **Performance Optimized**: Smooth rendering without flicker
- **Executable Builds**: One-click build process for distribution

## 🏗️ Project Structure

```
NumPad/
├── sources/           # Source code files
│   ├── numpad.py     # Main application entry point
│   ├── core.py       # Typing test engine and statistics
│   ├── characters.py # Character generation and validation
│   ├── style.py      # Visual styling and color management
│   └── widgets.py    # Reusable UI components
├── scripts/           # Build and utility scripts
│   ├── build.py      # Main build script
│   ├── build_windows.bat  # Windows build automation
│   └── build_unix.sh      # Linux/macOS build automation
├── assets/            # Resources and assets
│   ├── icon.ico      # Application icon (Windows)
│   └── version.txt   # Version information (Windows)
├── dist/              # Output directory for executables (created during build)
├── environment.yml    # Conda environment specification
└── README.md         # This file
```

## 🚀 Quick Start

### Prerequisites

- **Anaconda** or **Miniconda** installed
- **Python 3.10+** (automatically installed via conda environment)

### Windows

1. Double-click `scripts/build_windows.bat`
2. The executable will be created in the `dist/` folder
3. Run `dist/NumPad.exe`

### Linux/macOS

```bash
# Make script executable (first time only)
chmod +x scripts/build_unix.sh

# Build application
./scripts/build_unix.sh

# Run executable
./dist/NumPad
```

### Development Setup

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate numpad

# Run application in development mode
python sources/numpad.py

# Build executable manually
python scripts/build.py
```

## 🎮 Usage

1. **Launch** the application
2. **Type** the highlighted character using your numeric keypad
3. **Watch** your NPM (Numbers Per Minute) score in real-time
4. **Press R** to reset and start a new test
5. **Practice** with digits and mathematical operators

### Keyboard Controls

- **Numeric Keys (0-9)**: Type the displayed character
- **Operators (+, -, /, \*, .)**: Type mathematical operators
- **R Key**: Reset test and generate new sequence

## 🛠️ Development

### Architecture

This project demonstrates **modular Python architecture** with clear separation of concerns:

- **`core.py`**: Business logic for typing tests and statistics calculation
- **`characters.py`**: Character generation and input validation
- **`style.py`**: Centralized styling and color management
- **`widgets.py`**: Reusable UI components with efficient rendering
- **`numpad.py`**: Main application orchestration and event handling

### Key Technical Features

- **Performance Optimization**: Label reuse strategy eliminates GUI flicker
- **Modular Design**: Eliminates code duplication through component-based architecture
- **Cross-Platform Compatibility**: Handles OS-specific styling and behaviors
- **Build Automation**: Comprehensive build pipeline with error handling

### GitHub Copilot Integration

This project showcases **GitHub Copilot's capabilities** in:

- 🤖 **Code Generation**: AI-assisted creation of complex GUI applications
- 🔧 **Refactoring**: Intelligent code organization and optimization
- 🎨 **Architecture Design**: Modular component-based structure
- 🚀 **Build Automation**: Cross-platform deployment pipeline
- 📝 **Documentation**: Comprehensive README and code comments

## 🔧 Build Commands

### Basic Build

```bash
python scripts/build.py
```

### Clean Previous Builds

```bash
python scripts/build.py clean
```

### Create Version Info (Windows)

```bash
python scripts/build.py version
```

## 📦 Distribution

The built executable is self-contained and includes:

- Python runtime
- All required dependencies
- Application assets
- Platform-specific optimizations

**File sizes (approximate):**

- Windows: ~15-20 MB
- Linux: ~20-25 MB
- macOS: ~25-30 MB

## 🧪 Testing & Validation

This project was developed to **test GitHub Copilot's capabilities** in:

1. **GUI Development**: Creating responsive Tkinter applications
2. **Performance Optimization**: Solving rendering issues and lag
3. **Code Organization**: Refactoring monolithic code into modular components
4. **Cross-Platform Support**: Handling platform-specific requirements
5. **Build Automation**: Creating robust deployment pipelines

## 🤝 Contributing

As a **GitHub Copilot test project**, contributions are welcome to further explore AI-assisted development:

1. Fork the repository
2. Create a feature branch
3. Test with GitHub Copilot assistance
4. Submit a pull request with insights about the AI collaboration

## 📄 License

This project is released under the MIT License - see the LICENSE file for details.

## 🎯 Project Goals

This **GitHub Copilot test project** demonstrates:

- ✅ **AI-Assisted Development**: Effective human-AI collaboration
- ✅ **Rapid Prototyping**: From concept to working application
- ✅ **Code Quality**: Clean, maintainable, and well-documented code
- ✅ **Performance Engineering**: Optimized user experience
- ✅ **Deployment Automation**: Production-ready build pipeline

---

**Built with GitHub Copilot** 🤖✨
_Showcasing the future of AI-assisted software development_
