#!/usr/bin/env python3
"""
GameVerse Hub - A Python-Powered Game Selector
Main menu system with animated UI and game launcher
"""

import pygame
import json
import subprocess
import sys
import os
import math
from typing import List, Dict, Optional
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)
DARK_BLUE = (32, 64, 128)
GREEN = (64, 255, 64)
RED = (255, 64, 64)
PURPLE = (128, 64, 255)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class GameState(Enum):
    MAIN_MENU = 1
    CREDITS = 2
    LOADING = 3

class SoundManager:
    """Manages all sound effects and background music"""
    
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
        # Initialize mixer with safer settings
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Audio initialization failed: {e}")
            # Continue without audio
            pass
        
        # Create placeholder sounds (you can replace with actual sound files)
        self.create_placeholder_sounds()
    
    def create_placeholder_sounds(self):
        """Create simple beep sounds as placeholders"""
        try:
            import numpy as np
            
            # Create simple tones for sound effects
            sample_rate = 22050
            duration = 0.1
            
            # Hover sound (higher pitch)
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            hover_wave = np.sin(2 * np.pi * 800 * t) * 0.3
            hover_sound = pygame.sndarray.make_sound((hover_wave * 32767).astype(np.int16))
            self.sounds['hover'] = hover_sound
            
            # Select sound (lower pitch)
            t = np.linspace(0, duration * 2, int(sample_rate * duration * 2), False)
            select_wave = np.sin(2 * np.pi * 400 * t) * 0.3
            select_sound = pygame.sndarray.make_sound((select_wave * 32767).astype(np.int16))
            self.sounds['select'] = select_sound
            
        except ImportError:
            # Fallback: create silent sounds if numpy not available
            try:
                # Create minimal silent sounds
                silent_array = pygame.sndarray.array(pygame.mixer.Sound(buffer=b'\x00\x00' * 1000))
                self.sounds['hover'] = pygame.sndarray.make_sound(silent_array)
                self.sounds['select'] = pygame.sndarray.make_sound(silent_array)
            except Exception:
                # Ultimate fallback: no sounds
                print("Sound system not available - running without audio")
        except Exception as e:
            print(f"Could not create sounds: {e}")
    
    def play_sound(self, sound_name: str):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Could not play sound {sound_name}: {e}")
    
    def start_background_music(self):
        """Start background music (placeholder)"""
        # In a real implementation, you would load and play a music file
        pass
    
    def stop_background_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()

class MenuItem:
    """Represents a menu item with hover effects and animations"""
    
    def __init__(self, text: str, x: int, y: int, width: int, height: int, 
                 font: pygame.font.Font, action=None, data=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.action = action
        self.data = data
        self.hovered = False
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self, mouse_pos: tuple, dt: float):
        """Update hover state and animations"""
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Return True if hover state changed
        hover_changed = was_hovered != self.hovered
        
        # Update scale animation
        self.target_scale = 1.1 if self.hovered else 1.0
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * dt * 8
        
        return hover_changed
    
    def draw(self, screen: pygame.Surface):
        """Draw the menu item with hover effects"""
        # Calculate scaled dimensions
        scaled_width = int(self.width * self.hover_scale)
        scaled_height = int(self.height * self.hover_scale)
        scaled_x = self.x - (scaled_width - self.width) // 2
        scaled_y = self.y - (scaled_height - self.height) // 2
        
        # Draw background
        color = BLUE if self.hovered else DARK_BLUE
        border_color = WHITE if self.hovered else GRAY
        
        pygame.draw.rect(screen, color, (scaled_x, scaled_y, scaled_width, scaled_height))
        pygame.draw.rect(screen, border_color, (scaled_x, scaled_y, scaled_width, scaled_height), 2)
        
        # Draw text
        text_color = WHITE if self.hovered else GRAY
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

class GameLauncher:
    """Handles launching external game scripts"""
    
    def __init__(self, games_folder: str = "games"):
        self.games_folder = games_folder
        self.ensure_games_folder()
    
    def ensure_games_folder(self):
        """Create games folder if it doesn't exist"""
        if not os.path.exists(self.games_folder):
            os.makedirs(self.games_folder)
    
    def launch_game(self, game_file: str) -> bool:
        """Launch a game script"""
        game_path = os.path.join(self.games_folder, game_file)
        
        if not os.path.exists(game_path):
            print(f"Game file not found: {game_path}")
            self.create_placeholder_game(game_path, game_file)
            return False
        
        try:
            # Quit pygame before launching new game to avoid conflicts
            pygame.quit()
            
            # Launch the game in a new process with proper environment
            env = os.environ.copy()
            env['SDL_VIDEODRIVER'] = 'windib'  # Force Windows video driver
            
            process = subprocess.Popen([sys.executable, game_path], env=env)
            process.wait()  # Wait for game to finish
            
            # Reinitialize pygame after game closes
            pygame.init()
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            
            return True
        except Exception as e:
            print(f"Failed to launch game {game_file}: {e}")
            # Reinitialize pygame even if there was an error
            pygame.init()
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            return False
    
    def create_placeholder_game(self, game_path: str, game_file: str):
        """Create a placeholder game file"""
        game_name = game_file.replace('_', ' ').replace('.py', '').title()
        placeholder_code = f'''#!/usr/bin/env python3
"""
Placeholder for {game_file}
This is a demo game that shows how the GameVerse Hub launches games.
"""

import pygame
import sys

pygame.init()

# Game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("{game_name}")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill(BLACK)
    
    # Draw placeholder content
    title_text = font.render("Game Placeholder", True, WHITE)
    title_rect = title_text.get_rect(center=(400, 200))
    screen.blit(title_text, title_rect)
    
    game_text = small_font.render(f"This would be: {game_name}", True, BLUE)
    game_rect = game_text.get_rect(center=(400, 250))
    screen.blit(game_text, game_rect)
    
    instruction_text = small_font.render("Press ESC to return to GameVerse Hub", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(400, 350))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
'''
        
        try:
            with open(game_path, 'w') as f:
                f.write(placeholder_code)
            print(f"Created placeholder game: {game_path}")
        except Exception as e:
            print(f"Failed to create placeholder game: {e}")

class GameHub:
    """Main game hub class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GameVerse Hub")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MAIN_MENU
        
        # Initialize components
        self.sound_manager = SoundManager()
        self.game_launcher = GameLauncher()
        
        # Load fonts
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load games configuration
        self.games = self.load_games_config()
        
        # Create menu items
        self.menu_items = []
        self.create_menu_items()
        
        # Animation variables
        self.title_pulse = 0
        self.background_scroll = 0
        
        # Start background music
        self.sound_manager.start_background_music()
    
    def load_games_config(self) -> List[Dict]:
        """Load games configuration from JSON file"""
        try:
            with open('games_config.json', 'r') as f:
                config = json.load(f)
                return config.get('games', [])
        except FileNotFoundError:
            print("games_config.json not found, using default games")
            return []
        except Exception as e:
            print(f"Error loading games config: {e}")
            return []
    
    def create_menu_items(self):
        """Create menu items for games and options"""
        self.menu_items = []
        
        # Calculate layout
        items_per_row = 2
        item_width = 300
        item_height = 80
        spacing_x = 50
        spacing_y = 20
        start_x = (SCREEN_WIDTH - (items_per_row * item_width + (items_per_row - 1) * spacing_x)) // 2
        start_y = 200
        
        # Add game items
        for i, game in enumerate(self.games):
            row = i // items_per_row
            col = i % items_per_row
            x = start_x + col * (item_width + spacing_x)
            y = start_y + row * (item_height + spacing_y)
            
            menu_item = MenuItem(
                game['title'], x, y, item_width, item_height,
                self.menu_font, action='launch_game', data=game
            )
            self.menu_items.append(menu_item)
        
        # Add credits button
        credits_y = start_y + ((len(self.games) + 1) // items_per_row) * (item_height + spacing_y) + 40
        credits_item = MenuItem(
            "Credits", start_x, credits_y, item_width, item_height,
            self.menu_font, action='show_credits'
        )
        self.menu_items.append(credits_item)
        
        # Add exit button
        exit_item = MenuItem(
            "Exit", start_x + item_width + spacing_x, credits_y, item_width, item_height,
            self.menu_font, action='exit'
        )
        self.menu_items.append(exit_item)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.CREDITS:
                        self.state = GameState.MAIN_MENU
                    else:
                        self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)
    
    def handle_click(self, pos: tuple):
        """Handle mouse clicks on menu items"""
        for item in self.menu_items:
            if item.rect.collidepoint(pos):
                self.sound_manager.play_sound('select')
                
                if item.action == 'launch_game':
                    self.launch_game(item.data)
                elif item.action == 'show_credits':
                    self.state = GameState.CREDITS
                elif item.action == 'exit':
                    self.running = False
                break
    
    def launch_game(self, game_data: Dict):
        """Launch a selected game"""
        print(f"Launching game: {game_data['title']}")
        success = self.game_launcher.launch_game(game_data['file'])
        
        if not success:
            print(f"Failed to launch {game_data['title']}")
    
    def update(self, dt: float):
        """Update game state"""
        # Update animations
        self.title_pulse += dt * 2
        self.background_scroll += dt * 20
        
        # Update menu items
        mouse_pos = pygame.mouse.get_pos()
        for item in self.menu_items:
            if item.update(mouse_pos, dt):
                if item.hovered:
                    self.sound_manager.play_sound('hover')
    
    def draw_background(self):
        """Draw animated background"""
        self.screen.fill(BLACK)
        
        # Draw moving grid pattern
        grid_size = 50
        offset = int(self.background_scroll) % grid_size
        
        for x in range(-grid_size, SCREEN_WIDTH + grid_size, grid_size):
            for y in range(-grid_size, SCREEN_HEIGHT + grid_size, grid_size):
                pygame.draw.circle(self.screen, DARK_GRAY, 
                                 (x + offset, y + offset), 2)
    
    def draw_main_menu(self):
        """Draw the main menu"""
        self.draw_background()
        
        # Draw animated title
        pulse_scale = 1.0 + 0.1 * math.sin(self.title_pulse)
        title_color = (
            int(255 * (0.8 + 0.2 * math.sin(self.title_pulse * 0.7))),
            int(255 * (0.8 + 0.2 * math.sin(self.title_pulse * 0.5))),
            int(255 * (0.8 + 0.2 * math.sin(self.title_pulse * 0.3)))
        )
        
        title_text = self.title_font.render("GameVerse Hub", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
        # Scale the title
        scaled_title = pygame.transform.scale(title_text, 
                                            (int(title_rect.width * pulse_scale),
                                             int(title_rect.height * pulse_scale)))
        scaled_rect = scaled_title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(scaled_title, scaled_rect)
        
        # Draw subtitle
        subtitle_text = self.small_font.render("Select a game to play", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw menu items
        for item in self.menu_items:
            item.draw(self.screen)
        
        # Draw game descriptions for hovered items
        for item in self.menu_items:
            if item.hovered and item.data and 'description' in item.data:
                desc_text = self.small_font.render(item.data['description'], True, WHITE)
                desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                
                # Draw background for description
                bg_rect = desc_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, DARK_GRAY, bg_rect)
                pygame.draw.rect(self.screen, WHITE, bg_rect, 1)
                
                self.screen.blit(desc_text, desc_rect)
                break
    
    def draw_credits(self):
        """Draw the credits screen"""
        self.draw_background()
        
        # Credits content
        credits_lines = [
            "GameVerse Hub",
            "",
            "Created with Python & Pygame",
            "",
            "Features:",
            "• Modular game launcher",
            "• Animated UI with sound effects",
            "• JSON-based game configuration",
            "• Easy to extend with new games",
            "",
            "Press ESC to return to main menu"
        ]
        
        y_offset = 150
        for line in credits_lines:
            if line == "GameVerse Hub":
                text = self.title_font.render(line, True, GOLD)
            elif line.startswith("•"):
                text = self.small_font.render(line, True, GREEN)
            elif line == "Press ESC to return to main menu":
                text = self.small_font.render(line, True, BLUE)
            else:
                text = self.menu_font.render(line, True, WHITE)
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40 if line else 20
    
    def draw(self):
        """Main draw method"""
        if self.state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.state == GameState.CREDITS:
            self.draw_credits()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting GameVerse Hub...")
        print(f"Loaded {len(self.games)} games from configuration")
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    try:
        hub = GameHub()
        hub.run()
    except Exception as e:
        print(f"Error running GameVerse Hub: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
