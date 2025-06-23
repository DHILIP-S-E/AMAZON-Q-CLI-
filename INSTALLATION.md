# GameVerse Hub - Installation Guide

## System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 512 MB available
- **Storage**: 50 MB free space
- **Display**: 1024x768 resolution or higher

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 1 GB available
- **Storage**: 100 MB free space
- **Display**: 1920x1080 resolution
- **Audio**: Sound card for audio effects (optional)

## Installation Methods

### Method 1: Quick Start (Recommended)

1. **Download/Clone the GameVerse Hub folder**
   ```bash
   # If using git
   git clone <repository-url>
   cd gameverse_hub
   
   # Or extract from ZIP file
   unzip gameverse_hub.zip
   cd gameverse_hub
   ```

2. **Run the automatic installer**
   ```bash
   python run_gameverse.py
   ```
   This will automatically install pygame if needed and start the hub.

### Method 2: Manual Installation

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation:
     ```bash
     python --version
     # Should show Python 3.7+ 
     ```

2. **Install Pygame**
   ```bash
   pip install pygame
   
   # Or install from requirements file
   pip install -r requirements.txt
   ```

3. **Verify Pygame Installation**
   ```bash
   python -c "import pygame; print('Pygame installed successfully!')"
   ```

4. **Run GameVerse Hub**
   ```bash
   python main_menu.py
   ```

### Method 3: Using Virtual Environment (Advanced)

1. **Create Virtual Environment**
   ```bash
   python -m venv gameverse_env
   
   # Activate (Windows)
   gameverse_env\Scripts\activate
   
   # Activate (macOS/Linux)
   source gameverse_env/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Hub**
   ```bash
   python main_menu.py
   ```

## Platform-Specific Instructions

### Windows

1. **Using Command Prompt:**
   ```cmd
   cd path\to\gameverse_hub
   python run_gameverse.py
   ```

2. **Using PowerShell:**
   ```powershell
   Set-Location "path\to\gameverse_hub"
   python run_gameverse.py
   ```

3. **Double-click method:**
   - Double-click `start_gameverse.bat`
   - Or double-click `run_gameverse.py` (if Python is associated)

### macOS

1. **Using Terminal:**
   ```bash
   cd /path/to/gameverse_hub
   python3 run_gameverse.py
   ```

2. **Make executable and run:**
   ```bash
   chmod +x start_gameverse.sh
   ./start_gameverse.sh
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and pip (if not installed):**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Run GameVerse Hub:**
   ```bash
   cd /path/to/gameverse_hub
   python3 run_gameverse.py
   ```

3. **Using the shell script:**
   ```bash
   chmod +x start_gameverse.sh
   ./start_gameverse.sh
   ```

## Troubleshooting Installation

### Common Issues and Solutions

#### "Python is not recognized"
**Problem**: Python not in system PATH
**Solution**: 
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH
- Use full path: `C:\Python39\python.exe` (Windows)

#### "No module named 'pygame'"
**Problem**: Pygame not installed
**Solution**:
```bash
pip install pygame
# If pip doesn't work, try:
python -m pip install pygame
# On macOS/Linux, try:
pip3 install pygame
```

#### "Permission denied" (Linux/macOS)
**Problem**: Script not executable
**Solution**:
```bash
chmod +x start_gameverse.sh
chmod +x run_gameverse.py
```

#### "ModuleNotFoundError: No module named 'main_menu'"
**Problem**: Running from wrong directory
**Solution**: Make sure you're in the gameverse_hub directory:
```bash
cd gameverse_hub
ls  # Should show main_menu.py
python main_menu.py
```

#### Pygame installation fails
**Problem**: Missing system dependencies
**Solution**:

**Windows**: Install Microsoft Visual C++ Redistributable

**macOS**: 
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame
```

**Linux**:
```bash
sudo apt install python3-pygame
# Or build dependencies:
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
pip3 install pygame
```

## Verification

### Test Installation
Run this command to verify everything works:
```bash
python -c "
import pygame
import json
import subprocess
import sys
import os
print('✓ All dependencies available')
print('✓ GameVerse Hub ready to run!')
"
```

### Test Game Launch
1. Start GameVerse Hub: `python main_menu.py`
2. Click on any game tile
3. Verify the game launches in a new window
4. Press ESC to return to hub

## Next Steps

After successful installation:
1. Read [USAGE.md](USAGE.md) for how to use the hub
2. Check [DEVELOPMENT.md](DEVELOPMENT.md) to add your own games
3. See [CONFIGURATION.md](CONFIGURATION.md) for customization options

## Getting Help

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting-installation) section above
2. Verify your Python version: `python --version`
3. Check if pygame works: `python -c "import pygame"`
4. Look at console output for error messages
5. Try running individual games directly: `python games/super_pixel_runner.py`

## Uninstallation

To remove GameVerse Hub:
1. Delete the gameverse_hub folder
2. Optionally remove pygame: `pip uninstall pygame`
3. If using virtual environment, delete the environment folder
