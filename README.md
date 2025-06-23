# GameVerse Hub 🎮

A Python-powered game selector built with Pygame that provides a stylish menu interface to launch multiple mini-games.

## ✨ Features

- **Animated Main Menu**: Retro-style UI with pulsing title and moving background
- **10 Mini-Games**: Platformer, Arcade, Shooter, Puzzle, Quiz, Racing, Simulation, Board, Typing, and Clicker games
- **Modular Architecture**: Easy to add new games by dropping Python scripts into the games folder
- **JSON Configuration**: Games are configured via `games_config.json` for easy management
- **Sound Effects**: Hover and selection sounds (placeholder implementation)
- **Smooth Transitions**: Fade effects and hover animations
- **OOP Design**: Clean, extensible code structure

## 🚀 Quick Start

```bash
# 1. Install Pygame
pip install pygame

# 2. Navigate to GameVerse Hub
cd gameverse_hub

# 3. Run the hub (auto-installs dependencies)
python run_gameverse.py
```

**That's it! 🎮 The hub opens with games ready to play.**

## 📚 Documentation

Choose the guide that fits your needs:

- **[📖 QUICK_START.md](QUICK_START.md)** - Get running in 3 steps
- **[⚙️ INSTALLATION.md](INSTALLATION.md)** - Detailed setup for all platforms  
- **[🎮 USAGE.md](USAGE.md)** - Complete user guide
- **[🔧 CONFIGURATION.md](CONFIGURATION.md)** - Customize the hub
- **[👨‍💻 DEVELOPMENT.md](DEVELOPMENT.md)** - Add your own games
- **[📋 DOCUMENTATION.md](DOCUMENTATION.md)** - Complete documentation index

## 🎮 Included Games

### Fully Playable Games (5)
1. **Super Pixel Runner** - Side-scrolling platformer with enemies and power-ups
2. **Retro Breakout** - Classic brick-breaking arcade action  
3. **Alien Storm** - Space shooter with waves of alien enemies
4. **Mind Maze** - Number puzzle brain teaser
5. **Cookie Clicker** - Incremental clicking with upgrades system

### Placeholder Games (5)
Ready for your own implementations: Quiz Master, Speed Racer, City Builder, Chess Master, Type Fighter

## 🏗️ Project Structure

```
gameverse_hub/
├── 📄 Documentation
│   ├── README.md              # This file
│   ├── QUICK_START.md         # 3-step setup guide
│   ├── INSTALLATION.md        # Detailed installation
│   ├── USAGE.md              # Complete user guide
│   ├── CONFIGURATION.md       # Customization options
│   ├── DEVELOPMENT.md         # Developer guide
│   └── DOCUMENTATION.md       # Documentation index
├── 🚀 Launchers
│   ├── main_menu.py          # Main hub application
│   ├── run_gameverse.py      # Auto-installer launcher
│   ├── start_gameverse.sh    # Linux/macOS launcher
│   └── start_gameverse.bat   # Windows launcher
├── ⚙️ Configuration
│   ├── games_config.json     # Game definitions
│   └── requirements.txt      # Python dependencies
├── 🎮 Games
│   ├── super_pixel_runner.py # Platformer
│   ├── retro_breakout.py     # Arcade
│   ├── alien_storm.py        # Shooter
│   ├── mind_maze.py          # Puzzle
│   ├── cookie_clicker.py     # Clicker
│   └── [5 placeholder games]
└── 📁 Assets
    ├── fonts/                # Custom fonts
    ├── music/                # Sound effects & music
    └── icons/                # Game icons & images
```

## 🎯 How It Works

1. **Launch**: Run the hub using any launcher method
2. **Navigate**: Mouse hover shows game descriptions
3. **Play**: Click tiles to launch games in separate windows  
4. **Return**: Press ESC in any game to return to hub
5. **Extend**: Add your own games via simple configuration

## 🔧 Quick Customization

### Add Your Own Game
```bash
# 1. Create your game file
echo "# Your game code here" > games/my_game.py

# 2. Add to configuration
# Edit games_config.json and add:
{
  "title": "My Game",
  "file": "my_game.py", 
  "description": "My awesome game"
}

# 3. Restart hub - your game appears!
```

### Customize Appearance
```python
# Edit main_menu.py color constants:
BLUE = (64, 128, 255)     # Change menu colors
SCREEN_WIDTH = 1024       # Adjust window size
ITEMS_PER_ROW = 3         # Change grid layout
```

## 🎮 Controls

### Main Menu
- **Mouse**: Hover and click to select games
- **ESC**: Exit application

### Universal Game Controls  
- **ESC**: Return to GameVerse Hub (works in all games)
- **Game-specific**: Each game shows its controls on screen

## 🛠️ Requirements

- **Python**: 3.7 or higher
- **Pygame**: 2.0+ (auto-installed by run_gameverse.py)
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 512 MB available
- **Storage**: 50 MB free space

## 🚀 Multiple Ways to Run

```bash
# Method 1: Auto-installer (Recommended)
python run_gameverse.py

# Method 2: Direct launch
python main_menu.py

# Method 3: Platform launchers
./start_gameverse.sh      # Linux/macOS
start_gameverse.bat       # Windows (double-click)

# Method 4: With virtual environment
python -m venv gameverse_env
source gameverse_env/bin/activate  # Linux/macOS
gameverse_env\Scripts\activate     # Windows
pip install -r requirements.txt
python main_menu.py
```

## 🔍 Troubleshooting

### Common Issues
```bash
# "No module named 'pygame'"
pip install pygame

# "Python is not recognized"  
# Install Python from python.org, check "Add to PATH"

# Games won't launch
# Make sure you're in the gameverse_hub directory
cd gameverse_hub
python main_menu.py
```

### Need Help?
- 📖 **New users**: Start with [QUICK_START.md](QUICK_START.md)
- ⚙️ **Setup issues**: Check [INSTALLATION.md](INSTALLATION.md)  
- 🎮 **Usage questions**: See [USAGE.md](USAGE.md)
- 🔧 **Customization**: Read [CONFIGURATION.md](CONFIGURATION.md)
- 👨‍💻 **Development**: Study [DEVELOPMENT.md](DEVELOPMENT.md)

## 🏆 Features Showcase

✅ **Animated UI** - Pulsing title, hover effects, smooth transitions  
✅ **Modular Design** - Add games by dropping files in folder  
✅ **JSON Configuration** - Easy game management  
✅ **Process Isolation** - Games run independently  
✅ **Cross-Platform** - Windows, macOS, Linux support  
✅ **Sound System** - Audio feedback (placeholder implementation)  
✅ **Auto-Setup** - Automatic dependency installation  
✅ **Multiple Launchers** - Various ways to start the hub  
✅ **Comprehensive Docs** - Detailed guides for all skill levels  
✅ **Example Games** - 5 complete games included  

## 🎯 Perfect For

- **Game Developers** - Showcase your Python games
- **Students** - Learn game development with working examples  
- **Educators** - Teach programming with interactive projects
- **Hobbyists** - Build your personal game collection
- **Teams** - Organize multiple game projects

## 🤝 Contributing

GameVerse Hub is designed to be extended! Contributions welcome:

1. **Add Games** - Create new games for the collection
2. **Improve Hub** - Enhance the menu system and features  
3. **Documentation** - Help improve guides and examples
4. **Bug Fixes** - Report and fix issues
5. **Features** - Suggest and implement new capabilities

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute!

---

**🎮 Ready to start your gaming adventure? Choose your path:**

- **Just want to play?** → [QUICK_START.md](QUICK_START.md)
- **Want to customize?** → [CONFIGURATION.md](CONFIGURATION.md)  
- **Want to develop?** → [DEVELOPMENT.md](DEVELOPMENT.md)
- **Need help?** → [DOCUMENTATION.md](DOCUMENTATION.md)

**Welcome to GameVerse Hub - Where Python Games Come Together! 🚀**
