#!/usr/bin/env python3
"""
GameVerse Hub - Story Mode Launcher
Enhanced narrative-driven gaming experience with deep story integration
"""

import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = ['pygame']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("🔧 Installing missing dependencies...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def display_story_intro():
    """Display the story introduction"""
    intro_text = """
🎮 GAMEVERSE NEXUS: DIGITAL AWAKENING 🎮
═══════════════════════════════════════════════════════════════

STORY PREMISE:
You are Commander Nova, a digital consciousness trapped in the GameVerse - 
a virtual reality system created by the mysterious Nexus Corporation. 

Your memories have been fragmented, your identity scattered across multiple
simulation worlds. To escape this digital prison, you must:

🧠 RECOVER lost memories through platforming challenges
⚔️  MASTER combat skills in alien battlefields  
🧩 REBUILD neural pathways with mind-bending puzzles
💻 LEARN to manipulate the code that binds you
🏗️  CONSTRUCT new realities to aid your escape

Each game is a piece of your consciousness. Each victory brings you closer
to the truth about who you were... and who you can become.

ENHANCED FEATURES:
• Story-driven progression with character development
• Interconnected narrative across all games
• Dynamic difficulty based on your growing abilities
• Memory fragments that unlock deeper story elements
• Reality corruption effects that increase with awareness
• Multiple endings based on your choices and performance

═══════════════════════════════════════════════════════════════

Press ENTER to begin your digital awakening...
"""
    
    print(intro_text)
    input()

def main():
    """Main launcher function"""
    print("🚀 GameVerse Hub - Story Mode Initializing...")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install required dependencies")
        sys.exit(1)
    
    # Display story introduction
    display_story_intro()
    
    # Check if story framework exists
    if not os.path.exists('story_framework.py'):
        print("❌ Story framework not found!")
        print("Please ensure story_framework.py is in the current directory")
        sys.exit(1)
    
    # Check if story main menu exists
    if not os.path.exists('story_main_menu.py'):
        print("❌ Story main menu not found!")
        print("Please ensure story_main_menu.py is in the current directory")
        sys.exit(1)
    
    # Launch the story-based hub
    try:
        print("🎮 Launching GameVerse Nexus...")
        print("🧠 Initializing Commander Nova's consciousness...")
        print("🌐 Loading digital reality matrix...")
        
        # Import and run the story hub
        spec = importlib.util.spec_from_file_location("story_main_menu", "story_main_menu.py")
        story_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(story_module)
        
        # Run the main function
        story_module.main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Falling back to standard main menu...")
        try:
            import main_menu
            main_menu.main()
        except ImportError:
            print("❌ Could not load any menu system")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error launching story hub: {e}")
        print("Attempting to launch standard hub...")
        try:
            import main_menu
            main_menu.main()
        except Exception as e2:
            print(f"❌ Critical error: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()
