#!/usr/bin/env python3
"""
Simple Racer - Top-down Racing Game
Part of GameVerse Hub
"""

import pygame
import math
import random
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 64, 64)
BLUE = (64, 128, 255)
GREEN = (64, 255, 64)
YELLOW = (255, 255, 64)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class Car:
    def __init__(self, x, y, color=RED):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.max_speed = 8
        self.acceleration = 0.3
        self.friction = 0.1
        self.turn_speed = 4
        self.color = color
        self.width = 20
        self.height = 40
        
    def update(self, keys_pressed):
        # Handle input
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed * 0.5)
        else:
            # Apply friction
            if self.speed > 0:
                self.speed = max(0, self.speed - self.friction)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.friction)
        
        # Turning (only when moving)
        if abs(self.speed) > 0.1:
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                self.angle -= self.turn_speed * (abs(self.speed) / self.max_speed)
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                self.angle += self.turn_speed * (abs(self.speed) / self.max_speed)
        
        # Update position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
        # Keep car on screen
        self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x))
        self.y = max(self.height // 2, min(SCREEN_HEIGHT - self.height // 2, self.y))
    
    def draw(self, screen):
        # Create car surface
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))
        pygame.draw.rect(car_surface, WHITE, (0, 0, self.width, self.height), 2)
        
        # Add direction indicator
        pygame.draw.rect(car_surface, WHITE, (self.width // 2 - 2, 0, 4, 8))
        
        # Rotate and blit
        rotated_car = pygame.transform.rotate(car_surface, -self.angle)
        car_rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, car_rect)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Checkpoint:
    def __init__(self, x, y, width=100, height=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False
    
    def draw(self, screen):
        color = GREEN if not self.collected else DARK_GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class RacingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Racer - Top-Down Racing!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.ui_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game objects
        self.car = Car(100, 100)
        self.obstacles = []
        self.checkpoints = []
        
        # Game state
        self.lap_time = 0
        self.best_time = float('inf')
        self.current_checkpoint = 0
        self.laps_completed = 0
        self.game_started = False
        
        self.setup_track()
    
    def setup_track(self):
        """Create a simple track with obstacles and checkpoints"""
        # Track boundaries (walls)
        self.obstacles = [
            # Outer walls
            Obstacle(0, 0, SCREEN_WIDTH, 20),  # Top
            Obstacle(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Bottom
            Obstacle(0, 0, 20, SCREEN_HEIGHT),  # Left
            Obstacle(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),  # Right
            
            # Inner obstacles
            Obstacle(200, 150, 100, 20),
            Obstacle(400, 250, 20, 150),
            Obstacle(600, 100, 20, 200),
            Obstacle(300, 400, 200, 20),
            Obstacle(700, 450, 100, 20),
            Obstacle(150, 500, 20, 100),
        ]
        
        # Checkpoints for lap counting
        self.checkpoints = [
            Checkpoint(50, 300),  # Start/Finish
            Checkpoint(300, 100),
            Checkpoint(600, 350),
            Checkpoint(800, 200),
        ]
    
    def check_collisions(self):
        """Check if car collides with obstacles"""
        car_rect = pygame.Rect(self.car.x - self.car.width // 2, 
                              self.car.y - self.car.height // 2,
                              self.car.width, self.car.height)
        
        for obstacle in self.obstacles:
            if car_rect.colliderect(obstacle.rect):
                # Simple collision response - stop the car
                self.car.speed = 0
                # Push car away from obstacle
                if car_rect.centerx < obstacle.rect.centerx:
                    self.car.x = obstacle.rect.left - self.car.width // 2
                else:
                    self.car.x = obstacle.rect.right + self.car.width // 2
                
                if car_rect.centery < obstacle.rect.centery:
                    self.car.y = obstacle.rect.top - self.car.height // 2
                else:
                    self.car.y = obstacle.rect.bottom + self.car.height // 2
    
    def check_checkpoints(self):
        """Check if car passes through checkpoints"""
        car_rect = pygame.Rect(self.car.x - self.car.width // 2, 
                              self.car.y - self.car.height // 2,
                              self.car.width, self.car.height)
        
        if self.current_checkpoint < len(self.checkpoints):
            checkpoint = self.checkpoints[self.current_checkpoint]
            if car_rect.colliderect(checkpoint.rect) and not checkpoint.collected:
                checkpoint.collected = True
                self.current_checkpoint += 1
                
                # Complete lap
                if self.current_checkpoint >= len(self.checkpoints):
                    self.complete_lap()
    
    def complete_lap(self):
        """Handle lap completion"""
        self.laps_completed += 1
        if self.lap_time < self.best_time:
            self.best_time = self.lap_time
        
        # Reset for next lap
        self.current_checkpoint = 0
        self.lap_time = 0
        for checkpoint in self.checkpoints:
            checkpoint.collected = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.game_started = True
                elif event.key == pygame.K_r:
                    self.restart_game()
    
    def restart_game(self):
        """Reset the game"""
        self.car = Car(100, 100)
        self.lap_time = 0
        self.current_checkpoint = 0
        self.laps_completed = 0
        self.game_started = False
        for checkpoint in self.checkpoints:
            checkpoint.collected = False
    
    def update(self):
        if not self.game_started:
            return
        
        keys_pressed = pygame.key.get_pressed()
        self.car.update(keys_pressed)
        self.check_collisions()
        self.check_checkpoints()
        
        # Update lap time
        self.lap_time += 1 / FPS
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw track elements
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        for checkpoint in self.checkpoints:
            checkpoint.draw(self.screen)
        
        # Draw car
        self.car.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Title
        title_text = self.title_font.render("Simple Racer", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Game stats
        lap_text = self.ui_font.render(f"Laps: {self.laps_completed}", True, WHITE)
        self.screen.blit(lap_text, (20, 100))
        
        time_text = self.ui_font.render(f"Time: {self.lap_time:.1f}s", True, WHITE)
        self.screen.blit(time_text, (20, 130))
        
        if self.best_time != float('inf'):
            best_text = self.ui_font.render(f"Best: {self.best_time:.1f}s", True, GREEN)
            self.screen.blit(best_text, (20, 160))
        
        checkpoint_text = self.ui_font.render(f"Checkpoint: {self.current_checkpoint + 1}/{len(self.checkpoints)}", True, WHITE)
        self.screen.blit(checkpoint_text, (20, 190))
        
        # Speed indicator
        speed_text = self.ui_font.render(f"Speed: {abs(self.car.speed):.1f}", True, WHITE)
        speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 20, 100))
        self.screen.blit(speed_text, speed_rect)
        
        # Instructions
        if not self.game_started:
            start_text = self.ui_font.render("Press SPACE to start racing!", True, YELLOW)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(start_text, start_rect)
        
        instructions = [
            "WASD or Arrow Keys to drive",
            "R to restart, ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60 + i * 25))
            self.screen.blit(text, text_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    game = RacingGame()
    game.run()

if __name__ == "__main__":
    main()
