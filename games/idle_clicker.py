#!/usr/bin/env python3
"""
Idle Clicker - Cookie Clicker Style Game
Part of GameVerse Hub
"""

import pygame
import math
import sys
import time
import random

pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (64, 255, 64)
BLUE = (64, 128, 255)
RED = (255, 64, 64)
PURPLE = (128, 64, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class Upgrade:
    def __init__(self, name, base_cost, cps, description):
        self.name = name
        self.base_cost = base_cost
        self.current_cost = base_cost
        self.cps = cps  # Cookies per second
        self.count = 0
        self.description = description
    
    def buy(self):
        """Buy one upgrade"""
        self.count += 1
        self.current_cost = int(self.base_cost * (1.15 ** self.count))
    
    def get_total_cps(self):
        """Get total CPS from this upgrade"""
        return self.cps * self.count

class ClickerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Idle Clicker - Cookie Empire!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.big_font = pygame.font.Font(None, 48)
        self.ui_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.cookies = 0
        self.total_cookies = 0
        self.cookies_per_click = 1
        self.cookies_per_second = 0
        
        # Timing
        self.last_auto_time = time.time()
        
        # Click animation
        self.click_animations = []
        
        # Cookie button
        self.cookie_button = pygame.Rect(100, 200, 200, 200)
        
        # Upgrades
        self.upgrades = [
            Upgrade("Cursor", 15, 0.1, "Auto-clicks the cookie"),
            Upgrade("Grandma", 100, 1, "A nice grandma to bake cookies"),
            Upgrade("Farm", 1100, 8, "Grows cookie plants"),
            Upgrade("Mine", 12000, 47, "Mines cookie dough"),
            Upgrade("Factory", 130000, 260, "Mass produces cookies"),
            Upgrade("Bank", 1400000, 1400, "Generates cookie interest"),
            Upgrade("Temple", 20000000, 7800, "Summons cookie spirits"),
            Upgrade("Wizard", 330000000, 44000, "Casts cookie spells")
        ]
        
        # Click upgrades
        self.click_upgrades = [
            {"name": "Reinforced Cursor", "cost": 100, "multiplier": 2, "bought": False},
            {"name": "Steel Cursor", "cost": 500, "multiplier": 2, "bought": False},
            {"name": "Diamond Cursor", "cost": 10000, "multiplier": 2, "bought": False},
            {"name": "Quantum Cursor", "cost": 100000, "multiplier": 5, "bought": False}
        ]
        
        # UI setup
        self.setup_ui()
        
        # Statistics
        self.start_time = time.time()
        self.total_clicks = 0
    
    def setup_ui(self):
        """Setup UI elements"""
        # Upgrade panel
        self.upgrade_panel = pygame.Rect(400, 100, 600, 600)
        
        # Upgrade buttons
        self.upgrade_buttons = []
        button_height = 60
        for i, upgrade in enumerate(self.upgrades):
            button_rect = pygame.Rect(420, 120 + i * (button_height + 10), 560, button_height)
            self.upgrade_buttons.append(button_rect)
        
        # Click upgrade buttons
        self.click_upgrade_buttons = []
        for i, upgrade in enumerate(self.click_upgrades):
            button_rect = pygame.Rect(50, 450 + i * 40, 300, 35)
            self.click_upgrade_buttons.append(button_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.click_cookie()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        # Cookie click
        if self.cookie_button.collidepoint(pos):
            self.click_cookie()
        
        # Upgrade purchases
        for i, button in enumerate(self.upgrade_buttons):
            if button.collidepoint(pos):
                self.buy_upgrade(i)
        
        # Click upgrade purchases
        for i, button in enumerate(self.click_upgrade_buttons):
            if button.collidepoint(pos):
                self.buy_click_upgrade(i)
    
    def click_cookie(self):
        """Handle cookie clicking"""
        self.cookies += self.cookies_per_click
        self.total_cookies += self.cookies_per_click
        self.total_clicks += 1
        
        # Add click animation
        self.click_animations.append({
            'x': self.cookie_button.centerx + random.randint(-20, 20),
            'y': self.cookie_button.centery,
            'value': self.cookies_per_click,
            'time': time.time()
        })
    
    def buy_upgrade(self, index):
        """Buy an upgrade"""
        upgrade = self.upgrades[index]
        if self.cookies >= upgrade.current_cost:
            self.cookies -= upgrade.current_cost
            upgrade.buy()
            self.update_cps()
    
    def buy_click_upgrade(self, index):
        """Buy a click upgrade"""
        upgrade = self.click_upgrades[index]
        if not upgrade["bought"] and self.cookies >= upgrade["cost"]:
            self.cookies -= upgrade["cost"]
            upgrade["bought"] = True
            self.cookies_per_click *= upgrade["multiplier"]
    
    def update_cps(self):
        """Update cookies per second"""
        self.cookies_per_second = sum(upgrade.get_total_cps() for upgrade in self.upgrades)
    
    def update(self):
        """Update game state"""
        current_time = time.time()
        
        # Auto-generate cookies
        time_passed = current_time - self.last_auto_time
        if time_passed >= 0.1:  # Update every 0.1 seconds
            auto_cookies = self.cookies_per_second * time_passed
            self.cookies += auto_cookies
            self.total_cookies += auto_cookies
            self.last_auto_time = current_time
        
        # Update click animations
        self.click_animations = [
            anim for anim in self.click_animations 
            if current_time - anim['time'] < 1.0
        ]
    
    def format_number(self, num):
        """Format large numbers"""
        if num < 1000:
            return str(int(num))
        elif num < 1000000:
            return f"{num/1000:.1f}K"
        elif num < 1000000000:
            return f"{num/1000000:.1f}M"
        elif num < 1000000000000:
            return f"{num/1000000000:.1f}B"
        else:
            return f"{num/1000000000000:.1f}T"
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.title_font.render("Cookie Clicker", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Cookie count
        cookie_text = self.big_font.render(f"Cookies: {self.format_number(self.cookies)}", True, WHITE)
        self.screen.blit(cookie_text, (50, 100))
        
        # CPS
        if self.cookies_per_second > 0:
            cps_text = self.ui_font.render(f"per second: {self.format_number(self.cookies_per_second)}", True, GREEN)
            self.screen.blit(cps_text, (50, 140))
        
        # Cookie button
        pygame.draw.circle(self.screen, (139, 69, 19), self.cookie_button.center, 100)
        pygame.draw.circle(self.screen, WHITE, self.cookie_button.center, 100, 3)
        
        # Cookie details
        cookie_details = [
            f"Click Power: {self.format_number(self.cookies_per_click)}",
            f"Total Clicks: {self.total_clicks}",
            f"Total Cookies: {self.format_number(self.total_cookies)}"
        ]
        
        for i, detail in enumerate(cookie_details):
            text = self.small_font.render(detail, True, WHITE)
            self.screen.blit(text, (50, 420 + i * 20))
        
        # Click animations
        for anim in self.click_animations:
            alpha = max(0, 255 - int((time.time() - anim['time']) * 255))
            y_offset = int((time.time() - anim['time']) * 50)
            
            anim_text = self.ui_font.render(f"+{self.format_number(anim['value'])}", True, GOLD)
            anim_text.set_alpha(alpha)
            self.screen.blit(anim_text, (anim['x'], anim['y'] - y_offset))
        
        # Draw upgrades
        self.draw_upgrades()
        
        # Draw click upgrades
        self.draw_click_upgrades()
        
        # Instructions
        instruction_text = self.small_font.render("Click cookie or press SPACE! ESC to exit", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def draw_upgrades(self):
        """Draw upgrade panel"""
        # Panel background
        pygame.draw.rect(self.screen, DARK_GRAY, self.upgrade_panel)
        pygame.draw.rect(self.screen, WHITE, self.upgrade_panel, 2)
        
        # Panel title
        panel_title = self.ui_font.render("Upgrades", True, WHITE)
        self.screen.blit(panel_title, (self.upgrade_panel.x + 10, self.upgrade_panel.y + 10))
        
        # Upgrade buttons
        for i, (upgrade, button) in enumerate(zip(self.upgrades, self.upgrade_buttons)):
            # Button color based on affordability
            if self.cookies >= upgrade.current_cost:
                color = GREEN
            else:
                color = RED
            
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, WHITE, button, 2)
            
            # Upgrade info
            name_text = self.small_font.render(f"{upgrade.name} ({upgrade.count})", True, WHITE)
            cost_text = self.small_font.render(f"Cost: {self.format_number(upgrade.current_cost)}", True, WHITE)
            cps_text = self.small_font.render(f"CPS: {self.format_number(upgrade.cps)}", True, WHITE)
            
            self.screen.blit(name_text, (button.x + 5, button.y + 5))
            self.screen.blit(cost_text, (button.x + 5, button.y + 25))
            self.screen.blit(cps_text, (button.x + 5, button.y + 45))
    
    def draw_click_upgrades(self):
        """Draw click upgrades"""
        click_title = self.ui_font.render("Click Upgrades", True, WHITE)
        self.screen.blit(click_title, (50, 420))
        
        for i, (upgrade, button) in enumerate(zip(self.click_upgrades, self.click_upgrade_buttons)):
            if upgrade["bought"]:
                color = GRAY
                text_color = DARK_GRAY
            elif self.cookies >= upgrade["cost"]:
                color = BLUE
                text_color = WHITE
            else:
                color = RED
                text_color = WHITE
            
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, WHITE, button, 1)
            
            # Upgrade text
            if not upgrade["bought"]:
                upgrade_text = self.small_font.render(f"{upgrade['name']} - {self.format_number(upgrade['cost'])}", True, text_color)
            else:
                upgrade_text = self.small_font.render(f"{upgrade['name']} - OWNED", True, text_color)
            
            self.screen.blit(upgrade_text, (button.x + 5, button.y + 8))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    import random  # Import here to avoid issues
    game = ClickerGame()
    game.run()

if __name__ == "__main__":
    main()
