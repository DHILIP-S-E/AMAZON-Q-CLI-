#!/usr/bin/env python3
"""
Cookie Clicker - Addictive incremental clicking game
Part of GameVerse Hub
"""

import pygame
import sys
import math

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GREEN = (64, 255, 64)
BLUE = (64, 128, 255)
GOLD = (255, 215, 0)

class Cookie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 80
        self.click_scale = 1.0
        self.target_scale = 1.0
        self.pulse = 0
    
    def update(self, dt):
        # Update click animation
        scale_diff = self.target_scale - self.click_scale
        self.click_scale += scale_diff * dt * 10
        
        # Reset scale
        if abs(scale_diff) < 0.01:
            self.target_scale = 1.0
        
        # Pulse animation
        self.pulse += dt * 3
    
    def click(self):
        self.target_scale = 1.2
    
    def is_clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx * dx + dy * dy <= (self.radius * self.click_scale) ** 2
    
    def draw(self, screen):
        # Calculate scaled radius
        scaled_radius = int(self.radius * self.click_scale)
        
        # Draw cookie shadow
        pygame.draw.circle(screen, (50, 25, 0), 
                         (self.x + 3, self.y + 3), scaled_radius)
        
        # Draw cookie base
        pygame.draw.circle(screen, BROWN, (self.x, self.y), scaled_radius)
        
        # Draw chocolate chips
        chip_positions = [
            (-20, -15), (15, -20), (-10, 10), (20, 15), (0, -5), (-25, 20), (10, -30)
        ]
        
        for chip_x, chip_y in chip_positions:
            chip_x = int(chip_x * self.click_scale)
            chip_y = int(chip_y * self.click_scale)
            pygame.draw.circle(screen, (40, 20, 10), 
                             (self.x + chip_x, self.y + chip_y), 
                             max(3, int(6 * self.click_scale)))
        
        # Draw highlight
        highlight_offset = int(15 * self.click_scale)
        pygame.draw.circle(screen, (180, 120, 60), 
                         (self.x - highlight_offset, self.y - highlight_offset), 
                         max(8, int(15 * self.click_scale)))

class Upgrade:
    def __init__(self, name, cost, cps_increase, description):
        self.name = name
        self.cost = cost
        self.base_cost = cost
        self.cps_increase = cps_increase
        self.description = description
        self.count = 0
    
    def buy(self):
        self.count += 1
        self.cost = int(self.base_cost * (1.15 ** self.count))
    
    def can_afford(self, cookies):
        return cookies >= self.cost

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cookie Clicker")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.cookies = 0
        self.cookies_per_second = 0
        self.cookies_per_click = 1
        self.total_cookies = 0
        
        # Cookie object
        self.cookie = Cookie(200, 300)
        
        # Upgrades
        self.upgrades = [
            Upgrade("Cursor", 15, 0.1, "Clicks for you"),
            Upgrade("Grandma", 100, 1, "Bakes cookies"),
            Upgrade("Farm", 1100, 8, "Grows cookie plants"),
            Upgrade("Mine", 12000, 47, "Mines cookie dough"),
            Upgrade("Factory", 130000, 260, "Mass produces cookies"),
            Upgrade("Bank", 1400000, 1400, "Generates cookie interest")
        ]
        
        self.selected_upgrade = 0
        
        # Fonts
        self.big_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Floating numbers for clicks
        self.floating_numbers = []
        
        # Auto-save timer
        self.auto_save_timer = 0
    
    def add_floating_number(self, x, y, value):
        self.floating_numbers.append({
            'x': x,
            'y': y,
            'value': value,
            'timer': 60,
            'vel_y': -2
        })
    
    def update_floating_numbers(self):
        for number in self.floating_numbers[:]:
            number['y'] += number['vel_y']
            number['timer'] -= 1
            number['vel_y'] *= 0.98  # Slow down
            
            if number['timer'] <= 0:
                self.floating_numbers.remove(number)
    
    def format_number(self, num):
        if num >= 1e12:
            return f"{num/1e12:.1f}T"
        elif num >= 1e9:
            return f"{num/1e9:.1f}B"
        elif num >= 1e6:
            return f"{num/1e6:.1f}M"
        elif num >= 1e3:
            return f"{num/1e3:.1f}K"
        else:
            return str(int(num))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.selected_upgrade = max(0, self.selected_upgrade - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_upgrade = min(len(self.upgrades) - 1, self.selected_upgrade + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.buy_upgrade(self.selected_upgrade)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.cookie.is_clicked(event.pos):
                        self.click_cookie(event.pos)
                    else:
                        # Check upgrade clicks
                        upgrade_y = 50
                        for i, upgrade in enumerate(self.upgrades):
                            upgrade_rect = pygame.Rect(450, upgrade_y + i * 80, 320, 70)
                            if upgrade_rect.collidepoint(event.pos):
                                self.buy_upgrade(i)
                                break
    
    def click_cookie(self, pos):
        self.cookie.click()
        cookies_gained = self.cookies_per_click
        self.cookies += cookies_gained
        self.total_cookies += cookies_gained
        self.add_floating_number(pos[0], pos[1], f"+{cookies_gained}")
    
    def buy_upgrade(self, index):
        upgrade = self.upgrades[index]
        if upgrade.can_afford(self.cookies):
            self.cookies -= upgrade.cost
            upgrade.buy()
            self.cookies_per_second += upgrade.cps_increase
            
            # Special upgrades that affect clicking
            if upgrade.name == "Cursor" and upgrade.count == 1:
                self.cookies_per_click += 1
    
    def update(self, dt):
        self.cookie.update(dt)
        self.update_floating_numbers()
        
        # Generate cookies from CPS
        if self.cookies_per_second > 0:
            self.cookies += self.cookies_per_second * dt
            self.total_cookies += self.cookies_per_second * dt
        
        # Auto-save (placeholder)
        self.auto_save_timer += dt
        if self.auto_save_timer >= 10:  # Every 10 seconds
            self.auto_save_timer = 0
            # In a real implementation, you'd save to a file
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw cookie
        self.cookie.draw(self.screen)
        
        # Draw stats
        cookies_text = self.big_font.render(f"Cookies: {self.format_number(self.cookies)}", True, WHITE)
        self.screen.blit(cookies_text, (10, 10))
        
        if self.cookies_per_second > 0:
            cps_text = self.font.render(f"per second: {self.format_number(self.cookies_per_second)}", True, GREEN)
            self.screen.blit(cps_text, (10, 50))
        
        total_text = self.small_font.render(f"Total baked: {self.format_number(self.total_cookies)}", True, WHITE)
        self.screen.blit(total_text, (10, 80))
        
        # Draw upgrades
        upgrade_title = self.font.render("Upgrades:", True, WHITE)
        self.screen.blit(upgrade_title, (450, 10))
        
        for i, upgrade in enumerate(self.upgrades):
            y = 50 + i * 80
            
            # Highlight selected upgrade
            if i == self.selected_upgrade:
                pygame.draw.rect(self.screen, (40, 40, 40), (450, y, 320, 70))
            
            # Upgrade background
            color = GREEN if upgrade.can_afford(self.cookies) else (60, 60, 60)
            pygame.draw.rect(self.screen, color, (450, y, 320, 70), 2)
            
            # Upgrade info
            name_text = self.font.render(f"{upgrade.name} ({upgrade.count})", True, WHITE)
            self.screen.blit(name_text, (460, y + 5))
            
            cost_text = self.small_font.render(f"Cost: {self.format_number(upgrade.cost)}", True, YELLOW)
            self.screen.blit(cost_text, (460, y + 30))
            
            cps_text = self.small_font.render(f"+{upgrade.cps_increase} CPS", True, GREEN)
            self.screen.blit(cps_text, (460, y + 50))
        
        # Draw floating numbers
        for number in self.floating_numbers:
            alpha = min(255, number['timer'] * 4)
            color = (*WHITE, alpha) if alpha < 255 else WHITE
            
            try:
                text = self.small_font.render(str(number['value']), True, color[:3])
                self.screen.blit(text, (number['x'], number['y']))
            except:
                # Fallback for older pygame versions
                text = self.small_font.render(str(number['value']), True, WHITE)
                self.screen.blit(text, (number['x'], number['y']))
        
        # Instructions
        instructions = [
            "Click the cookie to bake!",
            "Use arrow keys + Enter to buy upgrades",
            "ESC: Return to GameVerse Hub"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 20))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
