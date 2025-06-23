#!/usr/bin/env python3
"""
Alien Storm - Space shooter with waves of alien enemies
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
CYAN = (64, 255, 255)

class Player:
    def __init__(self):
        self.width = 40
        self.height = 30
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 80
        self.speed = 7
        self.health = 100
        self.max_health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shoot_cooldown = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Keep player on screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def can_shoot(self):
        return self.shoot_cooldown <= 0
    
    def shoot(self):
        if self.can_shoot():
            self.shoot_cooldown = 10
            return Bullet(self.x + self.width // 2, self.y, -8, CYAN, True)
        return None
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        # Draw ship body
        pygame.draw.polygon(screen, BLUE, [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 4, self.y + self.height - 5),
            (self.x + 3 * self.width // 4, self.y + self.height - 5),
            (self.x + self.width, self.y + self.height)
        ])
        
        # Draw engines
        pygame.draw.rect(screen, RED, (self.x + 5, self.y + self.height - 8, 8, 8))
        pygame.draw.rect(screen, RED, (self.x + self.width - 13, self.y + self.height - 8, 8, 8))

class Alien:
    def __init__(self, x, y, alien_type=0):
        self.width = 30
        self.height = 25
        self.x = x
        self.y = y
        self.type = alien_type
        self.speed = 2 + alien_type
        self.health = 1 + alien_type
        self.max_health = self.health
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.shoot_cooldown = random.randint(60, 180)
        self.move_pattern = random.choice(['straight', 'zigzag', 'circle'])
        self.move_timer = 0
        
        # Type-specific properties
        if alien_type == 0:  # Basic alien
            self.color = GREEN
            self.points = 10
        elif alien_type == 1:  # Fast alien
            self.color = YELLOW
            self.points = 20
        else:  # Boss alien
            self.color = RED
            self.points = 50
            self.width = 50
            self.height = 40
    
    def update(self):
        self.move_timer += 1
        
        # Movement patterns
        if self.move_pattern == 'straight':
            self.y += self.speed
        elif self.move_pattern == 'zigzag':
            self.y += self.speed
            self.x += math.sin(self.move_timer * 0.1) * 2
        elif self.move_pattern == 'circle':
            self.y += self.speed * 0.5
            self.x += math.cos(self.move_timer * 0.05) * 3
        
        # Keep on screen horizontally
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def can_shoot(self):
        return self.shoot_cooldown <= 0 and random.random() < 0.02
    
    def shoot(self):
        if self.can_shoot():
            self.shoot_cooldown = random.randint(60, 180)
            return Bullet(self.x + self.width // 2, self.y + self.height, 5, RED, False)
        return None
    
    def take_damage(self):
        self.health -= 1
        return self.health <= 0
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
    
    def draw(self, screen):
        # Draw alien body
        pygame.draw.ellipse(screen, self.color, self.rect)
        pygame.draw.ellipse(screen, WHITE, self.rect, 2)
        
        # Draw eyes
        eye_size = 4 if self.type < 2 else 6
        pygame.draw.circle(screen, WHITE, 
                         (int(self.x + self.width // 3), int(self.y + self.height // 3)), 
                         eye_size)
        pygame.draw.circle(screen, WHITE, 
                         (int(self.x + 2 * self.width // 3), int(self.y + self.height // 3)), 
                         eye_size)
        
        # Health bar for damaged aliens
        if self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            health_ratio = self.health / self.max_health
            
            pygame.draw.rect(screen, RED, 
                           (self.x, self.y - 8, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, 
                           (self.x, self.y - 8, bar_width * health_ratio, bar_height))

class Bullet:
    def __init__(self, x, y, vel_y, color, friendly=True):
        self.x = x
        self.y = y
        self.vel_y = vel_y
        self.color = color
        self.friendly = friendly
        self.width = 4
        self.height = 8
        self.rect = pygame.Rect(x - 2, y - 4, self.width, self.height)
    
    def update(self):
        self.y += self.vel_y
        self.rect.y = self.y - 4
    
    def is_off_screen(self):
        return self.y < -10 or self.y > SCREEN_HEIGHT + 10
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 20
        self.max_timer = 20
    
    def update(self):
        self.timer -= 1
    
    def is_finished(self):
        return self.timer <= 0
    
    def draw(self, screen):
        if self.timer > 0:
            size = int((self.max_timer - self.timer) * 3)
            colors = [YELLOW, ORANGE, RED]
            
            for i, color in enumerate(colors):
                radius = max(1, size - i * 5)
                if radius > 0:
                    pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Alien Storm")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player()
        self.aliens = []
        self.bullets = []
        self.explosions = []
        
        # Game state
        self.score = 0
        self.wave = 1
        self.aliens_spawned = 0
        self.aliens_per_wave = 10
        self.spawn_timer = 0
        self.game_over = False
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        # Background stars
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) 
                     for _ in range(100)]
    
    def spawn_alien(self):
        if self.aliens_spawned < self.aliens_per_wave:
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = random.randint(-100, -50)
            
            # Determine alien type based on wave
            if self.wave >= 5 and random.random() < 0.1:
                alien_type = 2  # Boss
            elif self.wave >= 3 and random.random() < 0.3:
                alien_type = 1  # Fast
            else:
                alien_type = 0  # Basic
            
            alien = Alien(x, y, alien_type)
            self.aliens.append(alien)
            self.aliens_spawned += 1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and not self.game_over:
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.append(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def restart_game(self):
        self.player = Player()
        self.aliens = []
        self.bullets = []
        self.explosions = []
        self.score = 0
        self.wave = 1
        self.aliens_spawned = 0
        self.spawn_timer = 0
        self.game_over = False
    
    def update(self):
        if not self.game_over:
            # Update player
            self.player.update()
            
            # Handle continuous shooting
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                bullet = self.player.shoot()
                if bullet:
                    self.bullets.append(bullet)
            
            # Spawn aliens
            self.spawn_timer += 1
            if self.spawn_timer >= max(30 - self.wave * 2, 10):
                self.spawn_alien()
                self.spawn_timer = 0
            
            # Update aliens
            for alien in self.aliens[:]:
                alien.update()
                
                # Alien shooting
                bullet = alien.shoot()
                if bullet:
                    self.bullets.append(bullet)
                
                # Remove off-screen aliens
                if alien.is_off_screen():
                    self.aliens.remove(alien)
                
                # Check collision with player
                if alien.rect.colliderect(self.player.rect):
                    if self.player.take_damage(20):
                        self.game_over = True
                    self.explosions.append(Explosion(alien.x + alien.width // 2, 
                                                   alien.y + alien.height // 2))
                    self.aliens.remove(alien)
            
            # Update bullets
            for bullet in self.bullets[:]:
                bullet.update()
                
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)
                    continue
                
                # Check bullet collisions
                if bullet.friendly:
                    # Player bullet hitting aliens
                    for alien in self.aliens[:]:
                        if bullet.rect.colliderect(alien.rect):
                            if alien.take_damage():
                                self.score += alien.points
                                self.explosions.append(Explosion(alien.x + alien.width // 2, 
                                                               alien.y + alien.height // 2))
                                self.aliens.remove(alien)
                            self.bullets.remove(bullet)
                            break
                else:
                    # Alien bullet hitting player
                    if bullet.rect.colliderect(self.player.rect):
                        if self.player.take_damage(10):
                            self.game_over = True
                        self.bullets.remove(bullet)
            
            # Update explosions
            for explosion in self.explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    self.explosions.remove(explosion)
            
            # Check for wave completion
            if self.aliens_spawned >= self.aliens_per_wave and not self.aliens:
                self.wave += 1
                self.aliens_spawned = 0
                self.aliens_per_wave += 5
                self.player.health = min(self.player.max_health, self.player.health + 20)
    
    def draw_stars(self):
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, star, 1)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_stars()
        
        if not self.game_over:
            # Draw game objects
            self.player.draw(self.screen)
            
            for alien in self.aliens:
                alien.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            for explosion in self.explosions:
                explosion.draw(self.screen)
            
            # Draw UI
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            wave_text = self.font.render(f"Wave: {self.wave}", True, WHITE)
            self.screen.blit(wave_text, (10, 50))
            
            # Health bar
            bar_width = 200
            bar_height = 20
            health_ratio = self.player.health / self.player.max_health
            
            pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH - bar_width - 10, 10, bar_width, bar_height))
            pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - bar_width - 10, 10, bar_width * health_ratio, bar_height))
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - bar_width - 10, 10, bar_width, bar_height), 2)
            
            health_text = self.small_font.render("Health", True, WHITE)
            self.screen.blit(health_text, (SCREEN_WIDTH - bar_width - 10, 35))
            
            # Instructions
            instructions = [
                "WASD/Arrows: Move  |  SPACE: Shoot",
                "ESC: Return to GameVerse Hub"
            ]
            
            for i, instruction in enumerate(instructions):
                text = self.small_font.render(instruction, True, WHITE)
                self.screen.blit(text, (10, SCREEN_HEIGHT - 50 + i * 20))
        
        else:
            # Game over screen
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(final_score_text, score_rect)
            
            wave_text = self.font.render(f"Reached Wave: {self.wave}", True, WHITE)
            wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(wave_text, wave_rect)
            
            restart_text = self.small_font.render("Press R to restart or ESC to return to hub", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
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
