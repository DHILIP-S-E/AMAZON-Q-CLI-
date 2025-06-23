#!/usr/bin/env python3
"""
Simple test game to verify pygame is working correctly
"""

import pygame
import sys

def main():
    # Initialize pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Game - Working!")
    clock = pygame.time.Clock()
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    
    font = pygame.font.Font(None, 48)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw test content
        title_text = font.render("PYGAME IS WORKING!", True, GREEN)
        title_rect = title_text.get_rect(center=(400, 200))
        screen.blit(title_text, title_rect)
        
        instruction_text = font.render("Press ESC to exit", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(400, 300))
        screen.blit(instruction_text, instruction_rect)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
