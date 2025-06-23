#!/usr/bin/env python3
"""
Super Pixel Runner - A side-scrolling platformer
Part of GameVerse Hub
"""

import pygame
import random
import sys
import math

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
RED = (255, 64, 64)
GREEN = (64, 255, 64)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.on_ground = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms):
        # Handle input
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
        
        # Apply gravity
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep player on screen horizontally
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.y = platform.rect.bottom
                    self.vel_y = 0
        
        # Ground collision
        if self.y >= SCREEN_HEIGHT - 100 - self.height:
            self.y = SCREEN_HEIGHT - 100 - self.height
            self.vel_y = 0
            self.on_ground = True
        
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        # Draw simple face
        pygame.draw.circle(screen, WHITE, (int(self.x + 8), int(self.y + 8)), 3)
        pygame.draw.circle(screen, WHITE, (int(self.x + 24), int(self.y + 8)), 3)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.speed = 2
        self.direction = 1
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms):
        self.x += self.speed * self.direction
        
        # Bounce off screen edges
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1
        
        self.rect.x = self.x
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
        # Draw simple angry face
        pygame.draw.circle(screen, WHITE, (int(self.x + 6), int(self.y + 6)), 2)
        pygame.draw.circle(screen, WHITE, (int(self.x + 18), int(self.y + 6)), 2)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
        self.pulse = 0
    
    def update(self):
        self.pulse += 0.2
    
    def draw(self, screen):
        if not self.collected:
            pulse_size = 2 + math.sin(self.pulse) * 2
            pygame.draw.rect(screen, GREEN, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, int(pulse_size))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Pixel Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player(100, SCREEN_HEIGHT - 200)
        self.platforms = [
            Platform(200, SCREEN_HEIGHT - 200, 150, 20),
            Platform(400, SCREEN_HEIGHT - 300, 100, 20),
            Platform(600, SCREEN_HEIGHT - 250, 120, 20),
            Platform(800, SCREEN_HEIGHT - 350, 100, 20),
        ]
        self.enemies = [
            Enemy(250, SCREEN_HEIGHT - 230),
            Enemy(650, SCREEN_HEIGHT - 280),
        ]
        self.powerups = [
            PowerUp(450, SCREEN_HEIGHT - 330),
            PowerUp(850, SCREEN_HEIGHT - 380),
        ]
        
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        self.player.update(self.platforms)
        
        for enemy in self.enemies:
            enemy.update(self.platforms)
            
            # Check collision with player
            if self.player.rect.colliderect(enemy.rect):
                # Simple respawn for demo
                self.player.x = 100
                self.player.y = SCREEN_HEIGHT - 200
                self.player.vel_y = 0
        
        for powerup in self.powerups:
            powerup.update()
            
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                self.score += 100
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw ground
        pygame.draw.rect(self.screen, BROWN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Draw game objects
        for platform in self.platforms:
            platform.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        instructions = [
            "Arrow Keys / WASD: Move and Jump",
            "ESC: Return to GameVerse Hub",
            "Collect green power-ups, avoid red enemies!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 20))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
