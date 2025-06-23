#!/usr/bin/env python3
"""
Sim City Clone - Basic Idle Economy Simulation
Part of GameVerse Hub
"""

import pygame
import random
import sys
import time

pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (64, 255, 64)
BLUE = (64, 128, 255)
RED = (255, 64, 64)
YELLOW = (255, 255, 64)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GREEN = (144, 238, 144)

class Building:
    def __init__(self, x, y, building_type, cost, income_rate):
        self.x = x
        self.y = y
        self.type = building_type
        self.cost = cost
        self.income_rate = income_rate  # Money per second
        self.level = 1
        self.width = 60
        self.height = 60
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.last_income_time = time.time()
    
    def get_color(self):
        colors = {
            'house': BLUE,
            'shop': GREEN,
            'factory': GRAY,
            'office': YELLOW
        }
        return colors.get(self.type, WHITE)
    
    def upgrade(self):
        upgrade_cost = self.cost * self.level
        self.level += 1
        self.income_rate *= 1.5
        return upgrade_cost
    
    def generate_income(self):
        current_time = time.time()
        time_passed = current_time - self.last_income_time
        income = self.income_rate * time_passed
        self.last_income_time = current_time
        return income
    
    def draw(self, screen):
        # Building base
        pygame.draw.rect(screen, self.get_color(), self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Level indicator
        font = pygame.font.Font(None, 20)
        level_text = font.render(str(self.level), True, WHITE)
        level_rect = level_text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(level_text, level_rect)

class CitySimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sim City Clone - Build Your Economy!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.ui_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.money = 1000
        self.population = 0
        self.happiness = 100
        self.buildings = []
        self.selected_building_type = 'house'
        
        # Building types and costs
        self.building_types = {
            'house': {'cost': 100, 'income': 2, 'population': 4},
            'shop': {'cost': 250, 'income': 5, 'population': 0},
            'factory': {'cost': 500, 'income': 10, 'population': 0},
            'office': {'cost': 750, 'income': 15, 'population': 0}
        }
        
        # UI elements
        self.setup_ui()
        
        # Auto-save timer
        self.last_save_time = time.time()
    
    def setup_ui(self):
        """Setup UI button rectangles"""
        self.ui_panel = pygame.Rect(0, 0, 200, SCREEN_HEIGHT)
        
        # Building selection buttons
        self.building_buttons = {}
        button_height = 50
        start_y = 100
        
        for i, building_type in enumerate(self.building_types.keys()):
            button_rect = pygame.Rect(10, start_y + i * (button_height + 10), 180, button_height)
            self.building_buttons[building_type] = button_rect
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.selected_building_type = 'house'
                elif event.key == pygame.K_2:
                    self.selected_building_type = 'shop'
                elif event.key == pygame.K_3:
                    self.selected_building_type = 'factory'
                elif event.key == pygame.K_4:
                    self.selected_building_type = 'office'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
    
    def handle_mouse_click(self, pos):
        # Check UI button clicks
        for building_type, button_rect in self.building_buttons.items():
            if button_rect.collidepoint(pos):
                self.selected_building_type = building_type
                return
        
        # Check building placement
        if pos[0] > 200:  # Outside UI panel
            self.place_building(pos)
        
        # Check building upgrades
        for building in self.buildings:
            if building.rect.collidepoint(pos):
                self.upgrade_building(building)
                return
    
    def place_building(self, pos):
        """Place a new building at the given position"""
        building_data = self.building_types[self.selected_building_type]
        cost = building_data['cost']
        
        if self.money >= cost:
            # Check if position is valid (not overlapping)
            new_rect = pygame.Rect(pos[0] - 30, pos[1] - 30, 60, 60)
            
            # Make sure it's not overlapping with existing buildings
            for building in self.buildings:
                if new_rect.colliderect(building.rect):
                    return  # Can't place here
            
            # Create new building
            new_building = Building(
                pos[0] - 30, pos[1] - 30,
                self.selected_building_type,
                cost,
                building_data['income']
            )
            
            self.buildings.append(new_building)
            self.money -= cost
            
            # Update population
            if self.selected_building_type == 'house':
                self.population += building_data['population']
    
    def upgrade_building(self, building):
        """Upgrade a building"""
        upgrade_cost = building.cost * building.level
        if self.money >= upgrade_cost:
            self.money -= upgrade_cost
            building.upgrade()
    
    def update(self):
        """Update game state"""
        # Generate income from buildings
        total_income = 0
        for building in self.buildings:
            income = building.generate_income()
            total_income += income
        
        self.money += total_income
        
        # Update happiness based on city balance
        house_count = sum(1 for b in self.buildings if b.type == 'house')
        other_count = len(self.buildings) - house_count
        
        if house_count > 0:
            ratio = other_count / house_count
            if ratio < 0.5:
                self.happiness = min(100, self.happiness + 0.1)
            elif ratio > 2:
                self.happiness = max(0, self.happiness - 0.2)
        
        # Clamp values
        self.money = max(0, self.money)
        self.happiness = max(0, min(100, self.happiness))
    
    def draw(self):
        self.screen.fill(LIGHT_GREEN)
        
        # Draw buildings
        for building in self.buildings:
            building.draw(self.screen)
        
        # Draw UI panel
        pygame.draw.rect(self.screen, DARK_GRAY, self.ui_panel)
        pygame.draw.rect(self.screen, WHITE, self.ui_panel, 2)
        
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Title
        title_text = self.title_font.render("City Sim", True, WHITE)
        self.screen.blit(title_text, (10, 10))
        
        # Stats
        stats_y = 50
        stats = [
            f"Money: ${int(self.money)}",
            f"Population: {self.population}",
            f"Happiness: {int(self.happiness)}%"
        ]
        
        for i, stat in enumerate(stats):
            color = WHITE
            if i == 2:  # Happiness color coding
                if self.happiness > 70:
                    color = GREEN
                elif self.happiness < 30:
                    color = RED
                else:
                    color = YELLOW
            
            stat_text = self.small_font.render(stat, True, color)
            self.screen.blit(stat_text, (10, stats_y + i * 25))
        
        # Building selection buttons
        for building_type, button_rect in self.building_buttons.items():
            building_data = self.building_types[building_type]
            
            # Button color
            if building_type == self.selected_building_type:
                color = BLUE
            elif self.money >= building_data['cost']:
                color = GREEN
            else:
                color = RED
            
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Button text
            button_text = self.small_font.render(building_type.title(), True, WHITE)
            cost_text = self.small_font.render(f"${building_data['cost']}", True, WHITE)
            income_text = self.small_font.render(f"+${building_data['income']}/s", True, WHITE)
            
            self.screen.blit(button_text, (button_rect.x + 5, button_rect.y + 5))
            self.screen.blit(cost_text, (button_rect.x + 5, button_rect.y + 20))
            self.screen.blit(income_text, (button_rect.x + 5, button_rect.y + 35))
        
        # Instructions
        instructions = [
            "Click buttons or use 1-4 keys",
            "Click to place buildings",
            "Click buildings to upgrade",
            "Balance houses with businesses",
            "ESC to exit"
        ]
        
        start_y = SCREEN_HEIGHT - len(instructions) * 20 - 20
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, start_y + i * 20))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    game = CitySimulation()
    game.run()

if __name__ == "__main__":
    main()
