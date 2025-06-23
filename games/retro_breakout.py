#!/usr/bin/env python3
"""
Retro Breakout - Classic brick-breaking arcade action
Part of GameVerse Hub
"""

import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)
RED = (255, 64, 64)
GREEN = (64, 255, 64)
YELLOW = (255, 255, 64)
ORANGE = (255, 165, 0)
PURPLE = (128, 64, 255)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        
        # Keep paddle on screen
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        
        self.rect.x = self.x
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLUE, self.rect, 2)

class Ball:
    def __init__(self):
        self.radius = 8
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel_x = random.choice([-5, 5])
        self.vel_y = 5
        self.max_speed = 10
    
    def update(self, paddle, bricks):
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Wall collisions
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.vel_x = -self.vel_x
        
        if self.y - self.radius <= 0:
            self.vel_y = -self.vel_y
        
        # Paddle collision
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                               self.radius * 2, self.radius * 2)
        
        if ball_rect.colliderect(paddle.rect) and self.vel_y > 0:
            # Calculate hit position on paddle for angle variation
            hit_pos = (self.x - paddle.x) / paddle.width
            hit_pos = max(0, min(1, hit_pos))  # Clamp to 0-1
            
            # Adjust angle based on hit position
            angle_factor = (hit_pos - 0.5) * 2  # -1 to 1
            self.vel_x = angle_factor * 6
            self.vel_y = -abs(self.vel_y)
        
        # Brick collisions
        for brick in bricks[:]:  # Copy list to avoid modification during iteration
            if brick.active and ball_rect.colliderect(brick.rect):
                brick.hit()
                
                # Simple collision response
                if abs(ball_rect.centerx - brick.rect.centerx) > abs(ball_rect.centery - brick.rect.centery):
                    self.vel_x = -self.vel_x
                else:
                    self.vel_y = -self.vel_y
                
                return brick.points
        
        return 0
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel_x = random.choice([-5, 5])
        self.vel_y = 5
    
    def is_out_of_bounds(self):
        return self.y > SCREEN_HEIGHT
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius - 2)

class Brick:
    def __init__(self, x, y, color, points=10):
        self.width = 75
        self.height = 25
        self.x = x
        self.y = y
        self.color = color
        self.points = points
        self.active = True
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def hit(self):
        self.active = False
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Breakout")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        
        # Game state
        self.score = 0
        self.lives = 3
        self.level = 1
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        self.create_bricks()
    
    def create_bricks(self):
        self.bricks = []
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        
        rows = 6
        cols = 10
        brick_width = 75
        brick_height = 25
        spacing = 5
        
        start_x = (SCREEN_WIDTH - (cols * brick_width + (cols - 1) * spacing)) // 2
        start_y = 80
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + spacing)
                y = start_y + row * (brick_height + spacing)
                color = colors[row % len(colors)]
                points = (rows - row) * 10  # Higher rows worth more points
                
                brick = Brick(x, y, color, points)
                self.bricks.append(brick)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.lives <= 0:
                    self.restart_game()
    
    def restart_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.ball.reset()
        self.create_bricks()
    
    def update(self):
        if self.lives > 0:
            self.paddle.update()
            points = self.ball.update(self.paddle, self.bricks)
            self.score += points
            
            # Check if ball is out of bounds
            if self.ball.is_out_of_bounds():
                self.lives -= 1
                if self.lives > 0:
                    self.ball.reset()
            
            # Check if all bricks are destroyed
            active_bricks = [brick for brick in self.bricks if brick.active]
            if not active_bricks:
                self.level += 1
                self.ball.reset()
                self.create_bricks()
                # Increase ball speed slightly
                self.ball.max_speed = min(15, self.ball.max_speed + 1)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.lives > 0:
            # Draw game objects
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            
            for brick in self.bricks:
                brick.draw(self.screen)
            
            # Draw UI
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            self.screen.blit(lives_text, (10, 50))
            
            level_text = self.font.render(f"Level: {self.level}", True, WHITE)
            self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
            
            # Instructions
            instructions = [
                "Arrow Keys / A,D: Move Paddle",
                "ESC: Return to GameVerse Hub"
            ]
            
            for i, instruction in enumerate(instructions):
                text = self.small_font.render(instruction, True, WHITE)
                self.screen.blit(text, (10, SCREEN_HEIGHT - 60 + i * 20))
        
        else:
            # Game over screen
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.small_font.render("Press SPACE to restart or ESC to return to hub", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
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
