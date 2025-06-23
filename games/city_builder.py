#!/usr/bin/env python3
"""
Placeholder for city_builder.py
This is a demo game that shows how the GameVerse Hub launches games.
"""

import pygame
import sys

pygame.init()

# Game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("City Builder")
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
    
    game_text = small_font.render("This would be: City Builder", True, BLUE)
    game_rect = game_text.get_rect(center=(400, 250))
    screen.blit(game_text, game_rect)
    
    instruction_text = small_font.render("Press ESC to return to GameVerse Hub", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(400, 350))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
