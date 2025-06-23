#!/usr/bin/env python3
"""
GameVerse Hub Launcher
Simple launcher script that checks dependencies and starts the game hub
"""

import sys
import subprocess
import os

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_pygame():
    """Install pygame using pip"""
    print("Pygame not found. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install pygame. Please install it manually:")
        print("pip install pygame")
        return False

def main():
    print("🎮 GameVerse Hub Launcher")
    print("=" * 30)
    
    # Check if pygame is available
    if not check_pygame():
        if not install_pygame():
            sys.exit(1)
    
    # Check if main_menu.py exists
    if not os.path.exists("main_menu.py"):
        print("Error: main_menu.py not found!")
        print("Make sure you're running this from the gameverse_hub directory.")
        sys.exit(1)
    
    # Launch the game hub
    print("Starting GameVerse Hub...")
    try:
        import main_menu
        main_menu.main()
    except Exception as e:
        print(f"Error starting GameVerse Hub: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
