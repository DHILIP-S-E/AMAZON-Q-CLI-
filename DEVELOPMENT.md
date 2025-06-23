# GameVerse Hub - Development Guide

## Architecture Overview

GameVerse Hub uses a modular, object-oriented architecture designed for easy extension and maintenance.

### Core Components

```
GameVerse Hub Architecture
├── main_menu.py (Hub Controller)
│   ├── GameHub (Main Application)
│   ├── MenuItem (UI Elements)
│   ├── GameLauncher (Process Management)
│   └── SoundManager (Audio System)
├── games_config.json (Configuration)
└── games/ (Individual Game Modules)
```

### Class Structure

#### GameHub Class
```python
class GameHub:
    - screen: pygame.Surface
    - menu_items: List[MenuItem]
    - game_launcher: GameLauncher
    - sound_manager: SoundManager
    - state: GameState (MAIN_MENU, CREDITS, LOADING)
```

#### MenuItem Class
```python
class MenuItem:
    - text: str
    - position: (x, y, width, height)
    - action: str
    - hover_effects: animation properties
```

#### GameLauncher Class
```python
class GameLauncher:
    - games_folder: str
    - launch_game(filename): subprocess management
    - create_placeholder_game(): auto-generation
```

## Adding New Games

### Step 1: Create Your Game File

Create a new Python file in the `games/` directory:

```python
#!/usr/bin/env python3
"""
Your Game Name - Brief Description
Part of GameVerse Hub
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

class YourGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Your Game Name")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False  # Return to hub
    
    def update(self):
        # Game logic here
        pass
    
    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        # Draw your game here
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    game = YourGame()
    game.run()

if __name__ == "__main__":
    main()
```

### Step 2: Update Configuration

Add your game to `games_config.json`:

```json
{
  "games": [
    {
      "title": "Your Game Name",
      "file": "your_game.py",
      "description": "Brief description of your game"
    }
  ]
}
```

### Step 3: Test Integration

1. Restart GameVerse Hub
2. Your game should appear in the menu
3. Click to test launching
4. Verify ESC key returns to hub

## Game Development Guidelines

### Required Features

#### ESC Key Handling
Every game MUST handle the ESC key to return to the hub:

```python
def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
```

#### Window Management
```python
# Standard window setup
self.screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Title")
```

#### Clean Exit
```python
def run(self):
    while self.running:
        # Game loop
        pass
    pygame.quit()  # Clean shutdown
```

### Recommended Patterns

#### Game State Management
```python
from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class Game:
    def __init__(self):
        self.state = GameState.MENU
    
    def update(self):
        if self.state == GameState.PLAYING:
            self.update_gameplay()
        elif self.state == GameState.MENU:
            self.update_menu()
```

#### Resource Management
```python
class Game:
    def __init__(self):
        self.load_assets()
    
    def load_assets(self):
        try:
            self.font = pygame.font.Font(None, 36)
            # Load images, sounds, etc.
        except Exception as e:
            print(f"Asset loading error: {e}")
            # Provide fallbacks
```

#### Error Handling
```python
def safe_operation(self):
    try:
        # Risky operation
        pass
    except Exception as e:
        print(f"Error in {self.__class__.__name__}: {e}")
        # Graceful fallback
```

## Hub Customization

### Modifying the Main Menu

#### Changing Colors
```python
# In main_menu.py, modify color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)  # Customize these
```

#### Adjusting Layout
```python
# In create_menu_items() method
items_per_row = 3  # Change grid layout
item_width = 250   # Adjust tile size
spacing_x = 30     # Modify spacing
```

#### Adding New Menu Options
```python
# Add to create_menu_items()
new_item = MenuItem(
    "Settings", x, y, width, height,
    self.menu_font, action='show_settings'
)
self.menu_items.append(new_item)

# Handle in handle_click()
elif item.action == 'show_settings':
    self.show_settings_screen()
```

### Sound System Enhancement

#### Adding Real Audio Files
```python
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        try:
            self.sounds['hover'] = pygame.mixer.Sound('assets/music/hover.wav')
            self.sounds['select'] = pygame.mixer.Sound('assets/music/select.wav')
        except:
            self.create_placeholder_sounds()  # Fallback
```

#### Background Music
```python
def start_background_music(self):
    try:
        pygame.mixer.music.load('assets/music/background.ogg')
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except:
        print("Background music not available")
```

## Advanced Features

### Save System Integration

#### Game Progress Tracking
```python
import json
import os

class SaveManager:
    def __init__(self):
        self.save_file = "gameverse_save.json"
        self.data = self.load_save()
    
    def load_save(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return {"games": {}, "settings": {}}
    
    def save_game_progress(self, game_name, progress):
        self.data["games"][game_name] = progress
        self.save_data()
```

### Analytics and Statistics

#### Play Time Tracking
```python
import time

class GameAnalytics:
    def __init__(self):
        self.start_time = time.time()
        self.game_sessions = {}
    
    def track_game_launch(self, game_name):
        self.game_sessions[game_name] = {
            'launches': self.game_sessions.get(game_name, {}).get('launches', 0) + 1,
            'last_played': time.time()
        }
```

### Plugin System

#### Dynamic Game Loading
```python
import importlib.util
import os

class PluginManager:
    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = plugins_dir
        self.loaded_plugins = {}
    
    def load_plugins(self):
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith('.py'):
                self.load_plugin(filename)
    
    def load_plugin(self, filename):
        spec = importlib.util.spec_from_file_location(
            filename[:-3], 
            os.path.join(self.plugins_dir, filename)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.loaded_plugins[filename] = module
```

## Testing and Debugging

### Unit Testing Games

```python
import unittest
import pygame

class TestYourGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = YourGame()
    
    def test_initialization(self):
        self.assertIsNotNone(self.game.screen)
        self.assertTrue(self.game.running)
    
    def test_esc_handling(self):
        # Simulate ESC key press
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        self.game.handle_events()
        # Test that game responds appropriately
```

### Debug Mode

```python
class GameHub:
    def __init__(self, debug=False):
        self.debug = debug
        if debug:
            self.setup_debug_features()
    
    def setup_debug_features(self):
        # Add debug overlays, logging, etc.
        self.show_fps = True
        self.log_events = True
```

### Performance Profiling

```python
import cProfile
import pstats

def profile_game():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run game
    game = YourGame()
    game.run()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

## Best Practices

### Code Organization
1. **One class per file** for complex games
2. **Separate game logic** from rendering
3. **Use constants** for magic numbers
4. **Comment complex algorithms**
5. **Handle exceptions gracefully**

### Performance Optimization
1. **Limit frame rate** appropriately (30-60 FPS)
2. **Cache expensive operations**
3. **Use sprite groups** for collision detection
4. **Optimize drawing calls**
5. **Profile bottlenecks**

### User Experience
1. **Consistent controls** across games
2. **Clear visual feedback**
3. **Appropriate difficulty curves**
4. **Save progress** when possible
5. **Responsive UI**

## Deployment and Distribution

### Packaging for Distribution

#### Using PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main_menu.py
```

#### Creating Installer
```bash
# Windows (using NSIS)
makensis gameverse_installer.nsi

# macOS (using create-dmg)
create-dmg GameVerse.app

# Linux (using AppImage)
python -m appimage GameVerse
```

### Version Management

```python
# version.py
VERSION = "1.0.0"
BUILD_DATE = "2024-06-22"
AUTHOR = "Your Name"

# In main_menu.py
from version import VERSION
pygame.display.set_caption(f"GameVerse Hub v{VERSION}")
```

## Contributing Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add docstrings to classes and functions
- Keep functions focused and small

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-game

# Make changes and commit
git add .
git commit -m "Add new puzzle game"

# Push and create pull request
git push origin feature/new-game
```

### Documentation
- Update README.md for new features
- Add docstrings to new classes/methods
- Include usage examples
- Document configuration options

This development guide provides the foundation for extending GameVerse Hub with new games and features. The modular architecture makes it easy to add functionality without breaking existing code.
