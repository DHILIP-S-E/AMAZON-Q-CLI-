"""
GameVerse Hub 2.0 - UI Manager
Handles themes, layouts, and visual effects
"""

import pygame
import json
from typing import Dict, Tuple, List
from pathlib import Path

class UIManager:
    """Manage UI themes, layouts, and visual effects"""
    
    def __init__(self):
        self.current_theme = "retro"
        self.current_layout = "grid"
        self.themes = self._load_themes()
        self.layouts = self._load_layouts()
        
    def _load_themes(self) -> Dict:
        """Load available themes"""
        return {
            "retro": {
                "name": "Retro Gaming",
                "colors": {
                    "background": (20, 20, 40),
                    "primary": (64, 128, 255),
                    "secondary": (255, 64, 128),
                    "accent": (255, 255, 64),
                    "text": (255, 255, 255),
                    "text_secondary": (200, 200, 200),
                    "hover": (100, 150, 255),
                    "selected": (255, 100, 150),
                    "border": (100, 100, 150),
                    "success": (64, 255, 64),
                    "warning": (255, 200, 64),
                    "error": (255, 64, 64)
                },
                "fonts": {
                    "title": ("Arial", 48, True),
                    "subtitle": ("Arial", 24, False),
                    "body": ("Arial", 16, False),
                    "small": ("Arial", 12, False)
                },
                "effects": {
                    "glow": True,
                    "pulse": True,
                    "particles": True,
                    "transitions": "smooth"
                }
            },
            "neon": {
                "name": "Neon Cyberpunk",
                "colors": {
                    "background": (10, 10, 20),
                    "primary": (0, 255, 255),
                    "secondary": (255, 0, 255),
                    "accent": (255, 255, 0),
                    "text": (255, 255, 255),
                    "text_secondary": (180, 255, 255),
                    "hover": (50, 255, 255),
                    "selected": (255, 50, 255),
                    "border": (0, 200, 200),
                    "success": (0, 255, 100),
                    "warning": (255, 255, 0),
                    "error": (255, 50, 100)
                },
                "fonts": {
                    "title": ("Arial", 48, True),
                    "subtitle": ("Arial", 24, False),
                    "body": ("Arial", 16, False),
                    "small": ("Arial", 12, False)
                },
                "effects": {
                    "glow": True,
                    "pulse": True,
                    "particles": True,
                    "transitions": "fast"
                }
            },
            "minimal": {
                "name": "Clean Minimal",
                "colors": {
                    "background": (250, 250, 250),
                    "primary": (50, 50, 50),
                    "secondary": (100, 100, 100),
                    "accent": (0, 120, 200),
                    "text": (30, 30, 30),
                    "text_secondary": (100, 100, 100),
                    "hover": (220, 220, 220),
                    "selected": (200, 200, 200),
                    "border": (200, 200, 200),
                    "success": (0, 150, 0),
                    "warning": (200, 150, 0),
                    "error": (200, 0, 0)
                },
                "fonts": {
                    "title": ("Arial", 48, False),
                    "subtitle": ("Arial", 24, False),
                    "body": ("Arial", 16, False),
                    "small": ("Arial", 12, False)
                },
                "effects": {
                    "glow": False,
                    "pulse": False,
                    "particles": False,
                    "transitions": "smooth"
                }
            },
            "dark": {
                "name": "Dark Mode",
                "colors": {
                    "background": (25, 25, 25),
                    "primary": (200, 200, 200),
                    "secondary": (150, 150, 150),
                    "accent": (100, 150, 255),
                    "text": (255, 255, 255),
                    "text_secondary": (180, 180, 180),
                    "hover": (60, 60, 60),
                    "selected": (80, 80, 80),
                    "border": (100, 100, 100),
                    "success": (100, 200, 100),
                    "warning": (255, 200, 100),
                    "error": (255, 100, 100)
                },
                "fonts": {
                    "title": ("Arial", 48, True),
                    "subtitle": ("Arial", 24, False),
                    "body": ("Arial", 16, False),
                    "small": ("Arial", 12, False)
                },
                "effects": {
                    "glow": False,
                    "pulse": False,
                    "particles": False,
                    "transitions": "smooth"
                }
            }
        }
    
    def _load_layouts(self) -> Dict:
        """Load available layouts"""
        return {
            "grid": {
                "name": "Grid View",
                "items_per_row": 3,
                "item_spacing": 20,
                "item_size": (200, 150),
                "show_descriptions": True,
                "show_thumbnails": True
            },
            "list": {
                "name": "List View", 
                "items_per_row": 1,
                "item_spacing": 10,
                "item_size": (600, 80),
                "show_descriptions": True,
                "show_thumbnails": False
            },
            "carousel": {
                "name": "Carousel View",
                "items_per_row": 5,
                "item_spacing": 15,
                "item_size": (150, 200),
                "show_descriptions": False,
                "show_thumbnails": True
            },
            "cards": {
                "name": "Card View",
                "items_per_row": 2,
                "item_spacing": 25,
                "item_size": (300, 200),
                "show_descriptions": True,
                "show_thumbnails": True
            }
        }
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def set_layout(self, layout_name: str):
        """Set the current layout"""
        if layout_name in self.layouts:
            self.current_layout = layout_name
            return True
        return False
    
    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Get color from current theme"""
        theme = self.themes[self.current_theme]
        return theme["colors"].get(color_name, (255, 255, 255))
    
    def get_font(self, font_type: str) -> Tuple[str, int, bool]:
        """Get font configuration from current theme"""
        theme = self.themes[self.current_theme]
        return theme["fonts"].get(font_type, ("Arial", 16, False))
    
    def create_font(self, font_type: str) -> pygame.font.Font:
        """Create pygame font from theme configuration"""
        font_name, size, bold = self.get_font(font_type)
        return pygame.font.Font(None, size)
    
    def get_layout_config(self) -> Dict:
        """Get current layout configuration"""
        return self.layouts[self.current_layout]
    
    def has_effect(self, effect_name: str) -> bool:
        """Check if current theme has specific effect enabled"""
        theme = self.themes[self.current_theme]
        return theme["effects"].get(effect_name, False)
    
    def draw_glow_text(self, surface: pygame.Surface, text: str, font: pygame.font.Font, 
                      pos: Tuple[int, int], color: Tuple[int, int, int], glow_color: Tuple[int, int, int] = None):
        """Draw text with glow effect if theme supports it"""
        if not self.has_effect("glow"):
            # Simple text without glow
            text_surface = font.render(text, True, color)
            surface.blit(text_surface, pos)
            return
        
        if glow_color is None:
            glow_color = self.get_color("accent")
        
        # Create glow effect by drawing text multiple times with offset
        glow_offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for offset in glow_offsets:
            glow_pos = (pos[0] + offset[0], pos[1] + offset[1])
            glow_surface = font.render(text, True, glow_color)
            surface.blit(glow_surface, glow_pos)
        
        # Draw main text on top
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)
    
    def draw_pulsing_rect(self, surface: pygame.Surface, rect: pygame.Rect, 
                         color: Tuple[int, int, int], pulse_time: float):
        """Draw rectangle with pulsing effect if theme supports it"""
        if not self.has_effect("pulse"):
            pygame.draw.rect(surface, color, rect)
            return
        
        # Calculate pulse intensity (0.7 to 1.0)
        import math
        pulse_intensity = 0.7 + 0.3 * (math.sin(pulse_time * 3) + 1) / 2
        
        # Adjust color brightness
        pulsed_color = tuple(int(c * pulse_intensity) for c in color)
        pygame.draw.rect(surface, pulsed_color, rect)
    
    def draw_game_tile(self, surface: pygame.Surface, game: Dict, rect: pygame.Rect, 
                      is_hovered: bool = False, is_selected: bool = False, pulse_time: float = 0):
        """Draw a game tile with current theme styling"""
        # Determine colors
        if is_selected:
            bg_color = self.get_color("selected")
            border_color = self.get_color("accent")
        elif is_hovered:
            bg_color = self.get_color("hover")
            border_color = self.get_color("primary")
        else:
            bg_color = self.get_color("primary")
            border_color = self.get_color("border")
        
        # Draw background
        if self.has_effect("pulse") and (is_hovered or is_selected):
            self.draw_pulsing_rect(surface, rect, bg_color, pulse_time)
        else:
            pygame.draw.rect(surface, bg_color, rect)
        
        # Draw border
        pygame.draw.rect(surface, border_color, rect, 2)
        
        # Draw title
        title_font = self.create_font("subtitle")
        title_color = self.get_color("text")
        title_pos = (rect.x + 10, rect.y + 10)
        
        if self.has_effect("glow") and is_hovered:
            self.draw_glow_text(surface, game["title"], title_font, title_pos, title_color)
        else:
            title_surface = title_font.render(game["title"], True, title_color)
            surface.blit(title_surface, title_pos)
        
        # Draw description if layout shows it
        layout_config = self.get_layout_config()
        if layout_config.get("show_descriptions", True):
            desc_font = self.create_font("small")
            desc_color = self.get_color("text_secondary")
            desc_text = game.get("description", "")
            
            # Wrap text to fit in tile
            max_width = rect.width - 20
            wrapped_lines = self._wrap_text(desc_text, desc_font, max_width)
            
            y_offset = 40
            for line in wrapped_lines[:3]:  # Show max 3 lines
                desc_pos = (rect.x + 10, rect.y + y_offset)
                desc_surface = desc_font.render(line, True, desc_color)
                surface.blit(desc_surface, desc_pos)
                y_offset += 15
        
        # Draw category tag
        category = game.get("category", "arcade")
        tag_font = self.create_font("small")
        tag_color = self.get_color("accent")
        tag_pos = (rect.x + 10, rect.bottom - 25)
        tag_surface = tag_font.render(f"#{category}", True, tag_color)
        surface.blit(tag_surface, tag_pos)
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def get_available_themes(self) -> List[Dict]:
        """Get list of available themes"""
        return [{"id": theme_id, "name": theme_data["name"]} 
                for theme_id, theme_data in self.themes.items()]
    
    def get_available_layouts(self) -> List[Dict]:
        """Get list of available layouts"""
        return [{"id": layout_id, "name": layout_data["name"]} 
                for layout_id, layout_data in self.layouts.items()]
    
    def calculate_grid_positions(self, screen_width: int, screen_height: int, 
                               num_items: int) -> List[pygame.Rect]:
        """Calculate positions for grid layout"""
        layout_config = self.get_layout_config()
        items_per_row = layout_config["items_per_row"]
        item_spacing = layout_config["item_spacing"]
        item_width, item_height = layout_config["item_size"]
        
        positions = []
        
        # Calculate starting position to center the grid
        total_width = (items_per_row * item_width) + ((items_per_row - 1) * item_spacing)
        start_x = (screen_width - total_width) // 2
        start_y = 150  # Leave space for title
        
        for i in range(num_items):
            row = i // items_per_row
            col = i % items_per_row
            
            x = start_x + col * (item_width + item_spacing)
            y = start_y + row * (item_height + item_spacing)
            
            positions.append(pygame.Rect(x, y, item_width, item_height))
        
        return positions

# Example usage
if __name__ == "__main__":
    ui = UIManager()
    
    print("Available themes:")
    for theme in ui.get_available_themes():
        print(f"- {theme['name']} ({theme['id']})")
    
    print("\nAvailable layouts:")
    for layout in ui.get_available_layouts():
        print(f"- {layout['name']} ({layout['id']})")
    
    # Test theme switching
    ui.set_theme("neon")
    print(f"\nCurrent theme colors: {ui.themes[ui.current_theme]['colors']}")
