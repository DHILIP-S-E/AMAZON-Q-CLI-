# GameVerse Hub - Configuration Guide

## Configuration Files Overview

GameVerse Hub uses several configuration files to customize behavior:

- `games_config.json` - Game definitions and metadata
- `main_menu.py` - Hub appearance and behavior settings
- `assets/` - Media files (fonts, sounds, icons)

## Game Configuration (games_config.json)

### Basic Structure

```json
{
  "games": [
    {
      "title": "Display Name",
      "file": "script_filename.py",
      "description": "Brief game description"
    }
  ]
}
```

### Complete Example

```json
{
  "games": [
    {
      "title": "Super Pixel Runner",
      "file": "super_pixel_runner.py",
      "description": "A side-scrolling platformer with enemies and power-ups",
      "category": "platformer",
      "difficulty": "medium",
      "author": "GameVerse Team",
      "version": "1.0",
      "icon": "runner_icon.png",
      "screenshot": "runner_screenshot.png"
    },
    {
      "title": "Retro Breakout",
      "file": "retro_breakout.py", 
      "description": "Classic brick-breaking arcade action",
      "category": "arcade",
      "difficulty": "easy",
      "author": "GameVerse Team",
      "version": "1.2",
      "controls": ["Arrow Keys", "A/D Keys"],
      "features": ["Multiple Levels", "Power-ups", "High Scores"]
    }
  ],
  "settings": {
    "auto_create_missing": true,
    "show_placeholders": true,
    "default_window_size": [800, 600]
  }
}
```

### Configuration Fields

#### Required Fields
- **title**: Display name in the menu
- **file**: Python script filename (must exist in games/ folder)
- **description**: Brief description shown on hover

#### Optional Fields
- **category**: Game genre (platformer, arcade, puzzle, etc.)
- **difficulty**: easy, medium, hard
- **author**: Game creator name
- **version**: Game version number
- **icon**: Icon filename (in assets/icons/)
- **screenshot**: Screenshot filename (in assets/icons/)
- **controls**: Array of control descriptions
- **features**: Array of game features
- **min_python**: Minimum Python version required
- **dependencies**: Additional Python packages needed

### Advanced Configuration

#### Conditional Game Loading
```json
{
  "title": "Advanced Game",
  "file": "advanced_game.py",
  "description": "Requires Python 3.9+",
  "min_python": "3.9",
  "dependencies": ["numpy", "scipy"],
  "enabled": true,
  "platform": ["windows", "linux"]
}
```

#### Game Categories
```json
{
  "categories": {
    "arcade": {
      "color": [255, 128, 0],
      "icon": "arcade_icon.png"
    },
    "puzzle": {
      "color": [128, 255, 128],
      "icon": "puzzle_icon.png"
    }
  }
}
```

## Hub Appearance Configuration

### Color Schemes

Edit the color constants in `main_menu.py`:

```python
# Default Color Scheme
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)
DARK_BLUE = (32, 64, 128)
GREEN = (64, 255, 64)
RED = (255, 64, 64)
PURPLE = (128, 64, 255)
GOLD = (255, 215, 0)

# Dark Theme Example
BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
BLUE = (100, 150, 255)
DARK_BLUE = (50, 80, 150)
```

### Layout Configuration

```python
# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Menu layout
ITEMS_PER_ROW = 2
ITEM_WIDTH = 300
ITEM_HEIGHT = 80
SPACING_X = 50
SPACING_Y = 20
```

### Animation Settings

```python
# Animation speeds
TITLE_PULSE_SPEED = 2.0
BACKGROUND_SCROLL_SPEED = 20.0
HOVER_SCALE_SPEED = 8.0
MENU_TRANSITION_SPEED = 5.0

# Effects
ENABLE_PARTICLES = True
ENABLE_SOUND = True
ENABLE_ANIMATIONS = True
```

## Sound Configuration

### Audio Settings

```python
# In SoundManager class
AUDIO_FREQUENCY = 22050
AUDIO_SIZE = -16
AUDIO_CHANNELS = 2
AUDIO_BUFFER = 512

# Volume levels (0.0 to 1.0)
MASTER_VOLUME = 0.8
SFX_VOLUME = 0.6
MUSIC_VOLUME = 0.4
```

### Sound File Configuration

Create a `sound_config.json`:

```json
{
  "sounds": {
    "hover": {
      "file": "assets/music/hover.wav",
      "volume": 0.5
    },
    "select": {
      "file": "assets/music/select.wav", 
      "volume": 0.7
    },
    "background": {
      "file": "assets/music/background.ogg",
      "volume": 0.3,
      "loop": true
    }
  }
}
```

## Font Configuration

### Custom Fonts

```python
# Font loading
def load_fonts(self):
    try:
        self.title_font = pygame.font.Font("assets/fonts/title.ttf", 72)
        self.menu_font = pygame.font.Font("assets/fonts/menu.ttf", 36)
        self.small_font = pygame.font.Font("assets/fonts/small.ttf", 24)
    except:
        # Fallback to system fonts
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
```

### Font Configuration File

Create `font_config.json`:

```json
{
  "fonts": {
    "title": {
      "file": "assets/fonts/orbitron-bold.ttf",
      "size": 72,
      "fallback": "Arial"
    },
    "menu": {
      "file": "assets/fonts/roboto-regular.ttf",
      "size": 36,
      "fallback": "Helvetica"
    },
    "small": {
      "file": "assets/fonts/roboto-light.ttf",
      "size": 24,
      "fallback": "Arial"
    }
  }
}
```

## Performance Configuration

### Optimization Settings

```python
# Performance tuning
class PerformanceConfig:
    # Rendering
    VSYNC_ENABLED = True
    HARDWARE_ACCELERATION = True
    DOUBLE_BUFFERING = True
    
    # Animation
    REDUCE_ANIMATIONS_ON_LOW_FPS = True
    MIN_FPS_THRESHOLD = 30
    
    # Memory
    PRELOAD_ASSETS = True
    CACHE_RENDERED_TEXT = True
    MAX_CACHE_SIZE = 100
    
    # Background processes
    BACKGROUND_MUSIC_ENABLED = True
    PARTICLE_EFFECTS_ENABLED = True
    SOUND_EFFECTS_ENABLED = True
```

### Debug Configuration

```python
# Debug settings
class DebugConfig:
    SHOW_FPS = False
    SHOW_MEMORY_USAGE = False
    LOG_EVENTS = False
    ENABLE_PROFILING = False
    VERBOSE_LOGGING = False
    
    # Development features
    RELOAD_CONFIG_ON_CHANGE = True
    SHOW_COLLISION_BOXES = False
    ENABLE_CONSOLE_COMMANDS = False
```

## Environment Configuration

### Platform-Specific Settings

```python
import platform

class PlatformConfig:
    SYSTEM = platform.system()
    
    if SYSTEM == "Windows":
        DEFAULT_FONT_PATH = "C:/Windows/Fonts/"
        SOUND_DRIVER = "directsound"
    elif SYSTEM == "Darwin":  # macOS
        DEFAULT_FONT_PATH = "/System/Library/Fonts/"
        SOUND_DRIVER = "coreaudio"
    else:  # Linux
        DEFAULT_FONT_PATH = "/usr/share/fonts/"
        SOUND_DRIVER = "alsa"
```

### User Preferences

Create `user_config.json`:

```json
{
  "preferences": {
    "fullscreen": false,
    "resolution": [1024, 768],
    "master_volume": 0.8,
    "show_fps": false,
    "auto_launch_last_game": false,
    "theme": "default",
    "language": "en"
  },
  "controls": {
    "menu_up": "UP",
    "menu_down": "DOWN", 
    "menu_select": "RETURN",
    "menu_back": "ESCAPE"
  },
  "accessibility": {
    "high_contrast": false,
    "large_text": false,
    "reduce_motion": false,
    "screen_reader": false
  }
}
```

## Configuration Loading System

### Dynamic Configuration Loader

```python
import json
import os

class ConfigManager:
    def __init__(self):
        self.config_dir = "config"
        self.configs = {}
        self.load_all_configs()
    
    def load_all_configs(self):
        config_files = [
            "games_config.json",
            "sound_config.json", 
            "font_config.json",
            "user_config.json"
        ]
        
        for config_file in config_files:
            self.load_config(config_file)
    
    def load_config(self, filename):
        filepath = os.path.join(self.config_dir, filename)
        try:
            with open(filepath, 'r') as f:
                self.configs[filename] = json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {filename}")
            self.configs[filename] = {}
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {filename}: {e}")
            self.configs[filename] = {}
    
    def get(self, config_file, key, default=None):
        return self.configs.get(config_file, {}).get(key, default)
    
    def save_config(self, filename, data):
        filepath = os.path.join(self.config_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
```

## Configuration Validation

### Schema Validation

```python
def validate_game_config(game_data):
    required_fields = ['title', 'file', 'description']
    
    for field in required_fields:
        if field not in game_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate file exists
    game_file = os.path.join("games", game_data['file'])
    if not os.path.exists(game_file):
        print(f"Warning: Game file not found: {game_file}")
    
    # Validate optional fields
    if 'difficulty' in game_data:
        valid_difficulties = ['easy', 'medium', 'hard']
        if game_data['difficulty'] not in valid_difficulties:
            print(f"Warning: Invalid difficulty: {game_data['difficulty']}")
    
    return True
```

## Configuration Examples

### Minimal Configuration

```json
{
  "games": [
    {
      "title": "My Game",
      "file": "my_game.py",
      "description": "A simple game"
    }
  ]
}
```

### Full-Featured Configuration

```json
{
  "games": [
    {
      "title": "Epic Adventure",
      "file": "epic_adventure.py",
      "description": "An epic RPG adventure with quests and battles",
      "category": "rpg",
      "difficulty": "hard",
      "author": "Game Studio",
      "version": "2.1.0",
      "icon": "epic_icon.png",
      "screenshot": "epic_screenshot.png",
      "controls": ["WASD", "Mouse", "Space"],
      "features": ["Save System", "Multiplayer", "Achievements"],
      "min_python": "3.8",
      "dependencies": ["pygame", "numpy"],
      "tags": ["fantasy", "adventure", "story-driven"],
      "rating": "T",
      "playtime": "10-20 hours",
      "last_updated": "2024-06-01"
    }
  ],
  "settings": {
    "auto_create_missing": true,
    "show_placeholders": false,
    "sort_by": "title",
    "filter_by_category": false,
    "max_games_per_page": 10
  }
}
```

## Troubleshooting Configuration

### Common Issues

1. **JSON Syntax Errors**: Use a JSON validator
2. **Missing Files**: Check file paths are correct
3. **Invalid Values**: Verify data types match expectations
4. **Encoding Issues**: Save files as UTF-8

### Configuration Backup

```python
import shutil
import datetime

def backup_config():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"config_backup_{timestamp}"
    shutil.copytree("config", backup_dir)
    print(f"Configuration backed up to: {backup_dir}")
```

This configuration guide provides comprehensive control over GameVerse Hub's appearance, behavior, and game management. Use these settings to customize the hub to your preferences and requirements.
