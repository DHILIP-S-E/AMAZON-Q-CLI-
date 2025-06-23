# GameVerse Hub - Usage Guide

## Starting GameVerse Hub

### Quick Start
```bash
# Navigate to the gameverse_hub directory
cd gameverse_hub

# Run the hub (automatically installs pygame if needed)
python run_gameverse.py
```

### Alternative Methods
```bash
# Direct launch
python main_menu.py

# Using launcher scripts
./start_gameverse.sh    # Linux/macOS
start_gameverse.bat     # Windows (double-click)
```

## Main Menu Navigation

### Mouse Controls
- **Hover**: Move mouse over game tiles to see descriptions
- **Click**: Left-click on any game tile to launch that game
- **Credits**: Click "Credits" button to view information
- **Exit**: Click "Exit" button to close the hub

### Keyboard Controls
- **ESC**: Exit the application or return from credits screen
- **Mouse movement**: Navigate between options

## Game Controls

### Universal Controls (All Games)
- **ESC**: Return to GameVerse Hub from any game

### Super Pixel Runner
- **Arrow Keys** or **WASD**: Move left/right and jump
- **Objective**: Collect green power-ups, avoid red enemies
- **Gameplay**: Side-scrolling platformer with physics

### Retro Breakout
- **Arrow Keys** or **A/D**: Move paddle left/right
- **Objective**: Break all bricks with the ball
- **Gameplay**: Classic breakout with multiple levels

### Alien Storm
- **WASD** or **Arrow Keys**: Move spaceship
- **SPACE**: Shoot bullets (hold for continuous fire)
- **Objective**: Survive waves of alien enemies
- **Gameplay**: Top-down space shooter

### Mind Maze
- **1**: Add 1 to current number
- **2**: Add 2 to current number  
- **3**: Add 3 to current number
- **R**: Reset puzzle
- **Objective**: Reach the target number exactly

### Cookie Clicker
- **Mouse Click**: Click the cookie to bake
- **Arrow Keys**: Navigate upgrade menu
- **Enter/Space**: Buy selected upgrade
- **Objective**: Bake as many cookies as possible

## Features Overview

### Main Hub Features
- **Animated Title**: Pulsing, color-changing title
- **Background Animation**: Moving grid pattern
- **Hover Effects**: Tiles scale and highlight on hover
- **Sound Effects**: Audio feedback for interactions
- **Game Descriptions**: Hover over tiles to see game info
- **Credits Screen**: Information about the hub

### Game Management
- **Automatic Game Detection**: Games are loaded from the games/ folder
- **JSON Configuration**: Games defined in games_config.json
- **Placeholder Creation**: Missing games are created automatically
- **Independent Processes**: Each game runs separately

## Understanding the Interface

### Main Menu Layout
```
┌─────────────────────────────────────┐
│           GameVerse Hub             │
│        Select a game to play        │
├─────────────┬─────────────────────┤
│ Super Pixel │    Retro Breakout   │
│   Runner    │                     │
├─────────────┼─────────────────────┤
│ Alien Storm │     Mind Maze       │
│             │                     │
├─────────────┼─────────────────────┤
│    ...      │        ...          │
├─────────────┼─────────────────────┤
│   Credits   │        Exit         │
└─────────────┴─────────────────────┘
```

### Game Status Indicators
- **Blue Tiles**: Available games
- **Highlighted Tiles**: Hovered games (scaled up)
- **Description Bar**: Shows game info at bottom when hovering

## Tips and Best Practices

### Performance Tips
1. **Close unused games**: Each game runs independently
2. **Monitor system resources**: Multiple games can use CPU/RAM
3. **Adjust game settings**: Some games may have performance options

### Navigation Tips
1. **Use ESC consistently**: Always returns to hub from games
2. **Hover for info**: Game descriptions appear on hover
3. **Try all games**: Each offers different gameplay experiences

### Troubleshooting Gameplay
1. **Game won't start**: Check console for error messages
2. **Game runs slowly**: Close other applications
3. **Controls not working**: Make sure game window has focus
4. **Sound issues**: Check system audio settings

## Game-Specific Tips

### Super Pixel Runner
- **Timing jumps**: Jump just before reaching platforms
- **Power-up strategy**: Green power-ups give points
- **Enemy patterns**: Red enemies move predictably

### Retro Breakout
- **Paddle positioning**: Hit ball with different parts for angle control
- **Brick strategy**: Aim for higher rows (worth more points)
- **Ball speed**: Increases with each level

### Alien Storm
- **Movement**: Stay mobile to avoid enemy fire
- **Shooting**: Hold SPACE for continuous fire
- **Health management**: Avoid enemy collisions
- **Wave progression**: Enemies get stronger each wave

### Cookie Clicker
- **Early game**: Focus on clicking manually
- **Mid game**: Buy cursors and grandmas for automation
- **Late game**: Invest in expensive upgrades for exponential growth
- **Strategy**: Balance clicking and passive income

## Customization Options

### Adding Your Own Games
1. Create a Python game file in the `games/` folder
2. Add entry to `games_config.json`
3. Restart the hub to see your game

### Modifying Existing Games
1. Edit game files in the `games/` folder
2. Games are independent - changes won't affect the hub
3. Always include ESC key handling to return to hub

### Configuration Changes
- Edit `games_config.json` to modify game list
- Modify `main_menu.py` for hub appearance changes
- Add sound files to `assets/music/` folder

## Keyboard Shortcuts Reference

### Main Hub
| Key | Action |
|-----|--------|
| ESC | Exit application |
| Mouse | Navigate and select |

### In Games
| Key | Action |
|-----|--------|
| ESC | Return to hub |
| Game-specific | See individual game sections |

## Frequently Asked Questions

### Q: How do I add a new game?
A: Create a Python file in the games/ folder and add an entry to games_config.json

### Q: Can I run multiple games at once?
A: Yes, each game runs in its own process

### Q: How do I return to the hub from a game?
A: Press the ESC key in any game

### Q: Why don't I hear sound effects?
A: The current version uses placeholder sounds. Add real audio files to enable full sound

### Q: Can I modify the games?
A: Yes, all game files are editable Python scripts

### Q: How do I remove a game from the menu?
A: Remove its entry from games_config.json

### Q: What if a game crashes?
A: The hub will continue running. Restart the specific game from the menu

## Getting More Help

If you need additional assistance:
1. Check error messages in the console/terminal
2. Verify all files are in the correct locations
3. Test individual games by running them directly
4. Review the installation guide for setup issues
5. Check the development guide for customization help
