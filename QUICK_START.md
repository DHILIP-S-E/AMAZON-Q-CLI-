# GameVerse Hub - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Python & Pygame
```bash
# Install Python from python.org (if not already installed)
# Then install Pygame:
pip install pygame
```

### Step 2: Download & Extract
```bash
# Extract the gameverse_hub folder to your desired location
# Navigate to the folder:
cd gameverse_hub
```

### Step 3: Run GameVerse Hub
```bash
# Automatic setup (recommended):
python run_gameverse.py

# Or direct launch:
python main_menu.py
```

**That's it! 🎮 The hub should open with a menu of games ready to play.**

---

## 🎯 What You Get

### 5 Playable Games
- **Super Pixel Runner** - Platformer with enemies and power-ups
- **Retro Breakout** - Classic brick-breaking arcade game  
- **Alien Storm** - Space shooter with alien waves
- **Mind Maze** - Number puzzle brain teaser
- **Cookie Clicker** - Addictive incremental clicking game

### 5 Placeholder Games
- Quiz Master, Speed Racer, City Builder, Chess Master, Type Fighter
- Ready for you to replace with your own games!

---

## 🎮 Basic Controls

### Main Menu
- **Mouse**: Hover and click to select games
- **ESC**: Exit the application

### In Any Game
- **ESC**: Return to GameVerse Hub
- **Game-specific controls**: Shown in each game

---

## 🛠️ Quick Customization

### Add Your Own Game
1. Create `your_game.py` in the `games/` folder
2. Add this to `games_config.json`:
   ```json
   {
     "title": "Your Game",
     "file": "your_game.py", 
     "description": "Your game description"
   }
   ```
3. Restart the hub - your game appears!

### Change Hub Colors
Edit the color constants in `main_menu.py`:
```python
BLUE = (64, 128, 255)    # Change to your preferred color
DARK_BLUE = (32, 64, 128)
```

---

## 🔧 Troubleshooting

### "No module named 'pygame'"
```bash
pip install pygame
# If that doesn't work, try:
python -m pip install pygame
```

### "Python is not recognized"
- Install Python from [python.org](https://python.org)
- During installation, check "Add Python to PATH"

### Games won't launch
- Make sure you're in the `gameverse_hub` directory
- Check that game files exist in the `games/` folder

### Need more help?
- Check [INSTALLATION.md](INSTALLATION.md) for detailed setup
- See [USAGE.md](USAGE.md) for complete usage guide
- Read [DEVELOPMENT.md](DEVELOPMENT.md) to add your own games

---

## 📁 File Structure
```
gameverse_hub/
├── main_menu.py          # Main hub application
├── run_gameverse.py      # Auto-installer launcher
├── games_config.json     # Game configuration
├── games/                # Individual game files
│   ├── super_pixel_runner.py
│   ├── retro_breakout.py
│   ├── alien_storm.py
│   └── ...
└── assets/               # Fonts, music, icons
```

---

## 🎉 You're Ready!

GameVerse Hub is designed to be simple to use and easy to extend. Start by playing the included games, then add your own creations to build your personal game collection!

**Happy Gaming! 🎮**
