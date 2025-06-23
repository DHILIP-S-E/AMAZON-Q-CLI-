#!/usr/bin/env python3
"""
GameVerse Hub 2.0 Launcher
Automatically installs dependencies and launches the enhanced hub
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_and_install_pygame():
    """Check if pygame is installed, install if not"""
    try:
        import pygame
        print("✓ Pygame is already installed")
        return True
    except ImportError:
        print("Installing pygame...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("✓ Pygame installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install pygame")
            print("Please install pygame manually: pip install pygame")
            return False

def main():
    """Main launcher function"""
    print("🎮 GameVerse Hub 2.0 Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("games").exists():
        print("✗ Games folder not found!")
        print("Please run this script from the gameverse_hub directory")
        return False
    
    # Check and install pygame
    if not check_and_install_pygame():
        return False
    
    # Try to launch the enhanced hub
    try:
        print("\n🚀 Launching GameVerse Hub 2.0...")
        from enhanced_main_menu import main as run_enhanced_hub
        run_enhanced_hub()
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Falling back to original hub...")
        try:
            from main_menu import main as run_original_hub
            run_original_hub()
        except ImportError:
            print("✗ Could not launch any version of the hub")
            return False
    
    except Exception as e:
        print(f"✗ Error launching hub: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
