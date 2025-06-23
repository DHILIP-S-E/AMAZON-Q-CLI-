"""
GameVerse Hub 2.0 - Enhanced Main Menu
Integrates auto-discovery, themes, profiles, and advanced features
"""

import pygame
import sys
import time
import subprocess
import json
from pathlib import Path

# Import our new core modules
from core.game_discovery import GameDiscovery
from core.profile_manager import ProfileManager
from core.ui_manager import UIManager

class EnhancedGameHub:
    """Enhanced GameVerse Hub with 2.0 features"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("GameVerse Hub 2.0")
        
        # Core managers
        self.game_discovery = GameDiscovery()
        self.profile_manager = ProfileManager()
        self.ui_manager = UIManager()
        
        # Load user preferences
        self._load_user_preferences()
        
        # Game data
        self.games = []
        self.filtered_games = []
        self.selected_game_index = 0
        self.hovered_game_index = -1
        
        # UI state
        self.search_text = ""
        self.current_filter = "all"
        self.show_settings = False
        self.show_stats = False
        
        # Animation
        self.pulse_time = 0
        self.transition_alpha = 0
        
        # Load games
        self._refresh_games()
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        self.running = True
        
        print("GameVerse Hub 2.0 initialized!")
        print(f"Loaded {len(self.games)} games")
        print(f"Theme: {self.ui_manager.current_theme}")
        print(f"Layout: {self.ui_manager.current_layout}")
    
    def _load_user_preferences(self):
        """Load user preferences and apply them"""
        theme = self.profile_manager.get_preference("theme", "retro")
        layout = self.profile_manager.get_preference("layout", "grid")
        
        self.ui_manager.set_theme(theme)
        self.ui_manager.set_layout(layout)
    
    def _refresh_games(self):
        """Refresh game list using auto-discovery"""
        # Auto-discover games
        discovered = self.game_discovery.scan_games_folder()
        
        # Merge with existing config and save
        self.game_discovery.save_updated_config()
        
        # Load the merged configuration
        with open("games_config.json", 'r') as f:
            config = json.load(f)
        
        self.games = config.get("games", [])
        self.filtered_games = self.games.copy()
        
        print(f"Refreshed games: {len(self.games)} total")
    
    def _filter_games(self, category: str = "all", search: str = ""):
        """Filter games by category and search term"""
        filtered = self.games.copy()
        
        # Filter by category
        if category != "all":
            filtered = [g for g in filtered if g.get("category", "arcade") == category]
        
        # Filter by search term
        if search:
            search_lower = search.lower()
            filtered = [g for g in filtered if 
                       search_lower in g.get("title", "").lower() or
                       search_lower in g.get("description", "").lower() or
                       search_lower in g.get("tags", [])]
        
        self.filtered_games = filtered
        self.selected_game_index = 0
        self.hovered_game_index = -1
    
    def _get_categories(self) -> list:
        """Get unique categories from games"""
        categories = set()
        for game in self.games:
            categories.add(game.get("category", "arcade"))
        return sorted(list(categories))
    
    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_settings or self.show_stats:
                        self.show_settings = False
                        self.show_stats = False
                    else:
                        self.running = False
                
                elif event.key == pygame.K_RETURN:
                    if self.filtered_games and self.selected_game_index < len(self.filtered_games):
                        self._launch_game(self.filtered_games[self.selected_game_index])
                
                elif event.key == pygame.K_UP:
                    layout_config = self.ui_manager.get_layout_config()
                    items_per_row = layout_config["items_per_row"]
                    if self.selected_game_index >= items_per_row:
                        self.selected_game_index -= items_per_row
                
                elif event.key == pygame.K_DOWN:
                    layout_config = self.ui_manager.get_layout_config()
                    items_per_row = layout_config["items_per_row"]
                    if self.selected_game_index + items_per_row < len(self.filtered_games):
                        self.selected_game_index += items_per_row
                
                elif event.key == pygame.K_LEFT:
                    if self.selected_game_index > 0:
                        self.selected_game_index -= 1
                
                elif event.key == pygame.K_RIGHT:
                    if self.selected_game_index < len(self.filtered_games) - 1:
                        self.selected_game_index += 1
                
                elif event.key == pygame.K_F1:
                    self.show_stats = not self.show_stats
                    self.show_settings = False
                
                elif event.key == pygame.K_F2:
                    self.show_settings = not self.show_settings
                    self.show_stats = False
                
                elif event.key == pygame.K_F5:
                    self._refresh_games()
                
                elif event.key == pygame.K_t:
                    # Cycle through themes
                    themes = list(self.ui_manager.themes.keys())
                    current_index = themes.index(self.ui_manager.current_theme)
                    next_index = (current_index + 1) % len(themes)
                    self.ui_manager.set_theme(themes[next_index])
                    self.profile_manager.set_preference("theme", themes[next_index])
                
                elif event.key == pygame.K_l:
                    # Cycle through layouts
                    layouts = list(self.ui_manager.layouts.keys())
                    current_index = layouts.index(self.ui_manager.current_layout)
                    next_index = (current_index + 1) % len(layouts)
                    self.ui_manager.set_layout(layouts[next_index])
                    self.profile_manager.set_preference("layout", layouts[next_index])
            
            elif event.type == pygame.MOUSEMOTION:
                # Handle mouse hover
                mouse_pos = pygame.mouse.get_pos()
                self._handle_mouse_hover(mouse_pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    self._handle_mouse_click(mouse_pos)
    
    def _handle_mouse_hover(self, mouse_pos):
        """Handle mouse hover over game tiles"""
        if self.show_settings or self.show_stats:
            return
        
        positions = self.ui_manager.calculate_grid_positions(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT, len(self.filtered_games)
        )
        
        self.hovered_game_index = -1
        for i, rect in enumerate(positions):
            if rect.collidepoint(mouse_pos):
                self.hovered_game_index = i
                self.selected_game_index = i
                break
    
    def _handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks"""
        if self.show_settings or self.show_stats:
            return
        
        positions = self.ui_manager.calculate_grid_positions(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT, len(self.filtered_games)
        )
        
        for i, rect in enumerate(positions):
            if rect.collidepoint(mouse_pos):
                self._launch_game(self.filtered_games[i])
                break
    
    def _launch_game(self, game):
        """Launch selected game"""
        game_file = Path("games") / game["file"]
        
        if not game_file.exists():
            print(f"Game file not found: {game_file}")
            return
        
        print(f"Launching {game['title']}...")
        
        # Record session start time
        session_start = time.time()
        
        try:
            # Launch game in subprocess
            result = subprocess.run([sys.executable, str(game_file)], 
                                  capture_output=False, text=True)
            
            # Calculate session duration
            session_duration = int(time.time() - session_start)
            
            # Record the session (with placeholder score)
            self.profile_manager.record_game_session(game["id"], session_duration, 0)
            
            print(f"Game session recorded: {session_duration} seconds")
            
        except Exception as e:
            print(f"Error launching game: {e}")
    
    def _draw_title(self):
        """Draw animated title"""
        title_font = self.ui_manager.create_font("title")
        title_color = self.ui_manager.get_color("text")
        
        title_text = "GameVerse Hub 2.0"
        title_pos = (self.SCREEN_WIDTH // 2 - 200, 30)
        
        if self.ui_manager.has_effect("glow"):
            self.ui_manager.draw_glow_text(self.screen, title_text, title_font, title_pos, title_color)
        else:
            title_surface = title_font.render(title_text, True, title_color)
            self.screen.blit(title_surface, title_pos)
        
        # Draw subtitle with current theme/layout info
        subtitle_font = self.ui_manager.create_font("small")
        subtitle_color = self.ui_manager.get_color("text_secondary")
        subtitle_text = f"Theme: {self.ui_manager.current_theme.title()} | Layout: {self.ui_manager.current_layout.title()} | Games: {len(self.filtered_games)}"
        subtitle_pos = (self.SCREEN_WIDTH // 2 - 150, 80)
        subtitle_surface = subtitle_font.render(subtitle_text, True, subtitle_color)
        self.screen.blit(subtitle_surface, subtitle_pos)
    
    def _draw_controls_help(self):
        """Draw controls help"""
        help_font = self.ui_manager.create_font("small")
        help_color = self.ui_manager.get_color("text_secondary")
        
        controls = [
            "Arrow Keys: Navigate | Enter: Launch Game | ESC: Exit",
            "T: Change Theme | L: Change Layout | F1: Stats | F2: Settings | F5: Refresh"
        ]
        
        y_pos = self.SCREEN_HEIGHT - 50
        for control_text in controls:
            help_surface = help_font.render(control_text, True, help_color)
            help_pos = (10, y_pos)
            self.screen.blit(help_surface, help_pos)
            y_pos += 20
    
    def _draw_games(self):
        """Draw game tiles"""
        if not self.filtered_games:
            # No games message
            font = self.ui_manager.create_font("subtitle")
            color = self.ui_manager.get_color("text_secondary")
            text = "No games found. Press F5 to refresh."
            text_surface = font.render(text, True, color)
            text_pos = (self.SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 
                       self.SCREEN_HEIGHT // 2)
            self.screen.blit(text_surface, text_pos)
            return
        
        positions = self.ui_manager.calculate_grid_positions(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT, len(self.filtered_games)
        )
        
        for i, (game, rect) in enumerate(zip(self.filtered_games, positions)):
            is_selected = (i == self.selected_game_index)
            is_hovered = (i == self.hovered_game_index)
            
            self.ui_manager.draw_game_tile(
                self.screen, game, rect, is_hovered, is_selected, self.pulse_time
            )
    
    def _draw_stats_overlay(self):
        """Draw statistics overlay"""
        if not self.show_stats:
            return
        
        # Semi-transparent background
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Stats panel
        panel_width = 600
        panel_height = 400
        panel_x = (self.SCREEN_WIDTH - panel_width) // 2
        panel_y = (self.SCREEN_HEIGHT - panel_height) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, self.ui_manager.get_color("background"), panel_rect)
        pygame.draw.rect(self.screen, self.ui_manager.get_color("border"), panel_rect, 2)
        
        # Stats content
        font = self.ui_manager.create_font("body")
        title_font = self.ui_manager.create_font("subtitle")
        color = self.ui_manager.get_color("text")
        
        # Title
        title_surface = title_font.render("Gaming Statistics", True, color)
        self.screen.blit(title_surface, (panel_x + 20, panel_y + 20))
        
        # Stats data
        stats = [
            f"Total Playtime: {self.profile_manager.stats_data['total_playtime'] // 60} minutes",
            f"Games Played: {self.profile_manager.stats_data['games_played']}",
            f"Achievements: {self.profile_manager.stats_data['achievement_count']}",
            f"Favorite Category: {self.profile_manager.stats_data.get('favorite_category', 'None')}"
        ]
        
        y_offset = 70
        for stat in stats:
            stat_surface = font.render(stat, True, color)
            self.screen.blit(stat_surface, (panel_x + 20, panel_y + y_offset))
            y_offset += 30
        
        # Top games
        top_games = self.profile_manager.get_top_games(3)
        if top_games:
            title_surface = title_font.render("Top Games:", True, color)
            self.screen.blit(title_surface, (panel_x + 20, panel_y + y_offset + 20))
            y_offset += 60
            
            for i, game_stat in enumerate(top_games):
                game_text = f"{i+1}. {game_stat['game_id']} - {game_stat['playtime']//60}min"
                game_surface = font.render(game_text, True, color)
                self.screen.blit(game_surface, (panel_x + 40, panel_y + y_offset))
                y_offset += 25
    
    def _draw_settings_overlay(self):
        """Draw settings overlay"""
        if not self.show_settings:
            return
        
        # Semi-transparent background
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Settings panel
        panel_width = 500
        panel_height = 350
        panel_x = (self.SCREEN_WIDTH - panel_width) // 2
        panel_y = (self.SCREEN_HEIGHT - panel_height) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, self.ui_manager.get_color("background"), panel_rect)
        pygame.draw.rect(self.screen, self.ui_manager.get_color("border"), panel_rect, 2)
        
        # Settings content
        font = self.ui_manager.create_font("body")
        title_font = self.ui_manager.create_font("subtitle")
        color = self.ui_manager.get_color("text")
        
        # Title
        title_surface = title_font.render("Settings", True, color)
        self.screen.blit(title_surface, (panel_x + 20, panel_y + 20))
        
        # Available themes
        y_offset = 70
        themes_title = font.render("Available Themes:", True, color)
        self.screen.blit(themes_title, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        for theme in self.ui_manager.get_available_themes():
            prefix = "→ " if theme["id"] == self.ui_manager.current_theme else "  "
            theme_text = f"{prefix}{theme['name']}"
            theme_surface = font.render(theme_text, True, color)
            self.screen.blit(theme_surface, (panel_x + 40, panel_y + y_offset))
            y_offset += 25
        
        # Available layouts
        y_offset += 20
        layouts_title = font.render("Available Layouts:", True, color)
        self.screen.blit(layouts_title, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        for layout in self.ui_manager.get_available_layouts():
            prefix = "→ " if layout["id"] == self.ui_manager.current_layout else "  "
            layout_text = f"{prefix}{layout['name']}"
            layout_surface = font.render(layout_text, True, color)
            self.screen.blit(layout_surface, (panel_x + 40, panel_y + y_offset))
            y_offset += 25
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self._handle_events()
            
            # Update animations
            self.pulse_time += 0.016  # Assuming 60 FPS
            
            # Clear screen
            self.screen.fill(self.ui_manager.get_color("background"))
            
            # Draw UI elements
            self._draw_title()
            self._draw_games()
            self._draw_controls_help()
            self._draw_stats_overlay()
            self._draw_settings_overlay()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    try:
        hub = EnhancedGameHub()
        hub.run()
    except Exception as e:
        print(f"Error running GameVerse Hub 2.0: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
