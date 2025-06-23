#!/usr/bin/env python3
"""
Speed Typing Game - Type falling words and test your WPM
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
RED = (255, 64, 64)
BLUE = (64, 128, 255)
YELLOW = (255, 255, 64)
PURPLE = (128, 64, 255)
GRAY = (128, 128, 128)

class FallingWord:
    def __init__(self, word, x, y, speed):
        self.word = word
        self.x = x
        self.y = y
        self.speed = speed
        self.font = pygame.font.Font(None, 32)
        self.typed_chars = 0
        self.completed = False
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen):
        # Draw typed part in green, untyped in white
        typed_part = self.word[:self.typed_chars]
        untyped_part = self.word[self.typed_chars:]
        
        # Typed part
        if typed_part:
            typed_text = self.font.render(typed_part, True, GREEN)
            screen.blit(typed_text, (self.x, self.y))
            typed_width = typed_text.get_width()
        else:
            typed_width = 0
        
        # Untyped part
        if untyped_part:
            untyped_text = self.font.render(untyped_part, True, WHITE)
            screen.blit(untyped_text, (self.x + typed_width, self.y))
    
    def type_char(self, char):
        if self.typed_chars < len(self.word) and self.word[self.typed_chars] == char:
            self.typed_chars += 1
            if self.typed_chars == len(self.word):
                self.completed = True
            return True
        return False
    
    def get_next_char(self):
        if self.typed_chars < len(self.word):
            return self.word[self.typed_chars]
        return None

class TypingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Speed Typing - Test Your WPM!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.ui_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.input_font = pygame.font.Font(None, 36)
        
        # Game state
        self.falling_words = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.words_typed = 0
        self.chars_typed = 0
        self.game_started = False
        self.game_over = False
        
        # Timing
        self.start_time = None
        self.last_word_spawn = 0
        self.spawn_delay = 2000  # milliseconds
        
        # Input
        self.current_input = ""
        self.active_word = None
        
        # Word lists
        self.word_lists = {
            1: ["cat", "dog", "run", "jump", "fast", "slow", "big", "small"],
            2: ["house", "water", "light", "music", "happy", "quick", "green", "table"],
            3: ["computer", "keyboard", "monitor", "program", "function", "variable", "python", "gaming"],
            4: ["programming", "development", "algorithm", "structure", "interface", "application", "framework", "database"],
            5: ["extraordinary", "magnificent", "revolutionary", "sophisticated", "implementation", "optimization", "architecture", "methodology"]
        }
        
        # Statistics
        self.total_chars = 0
        self.correct_chars = 0
        self.start_time_stats = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and not self.game_started:
                    self.start_game()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif self.game_started and not self.game_over:
                    self.handle_typing(event)
    
    def handle_typing(self, event):
        if event.key == pygame.K_BACKSPACE:
            if self.current_input:
                self.current_input = self.current_input[:-1]
                if self.active_word:
                    self.active_word.typed_chars = len(self.current_input)
        elif event.unicode.isprintable():
            char = event.unicode.lower()
            self.current_input += char
            self.total_chars += 1
            
            # Find or set active word
            if not self.active_word:
                for word in self.falling_words:
                    if word.word.startswith(self.current_input) and not word.completed:
                        self.active_word = word
                        break
            
            # Type character in active word
            if self.active_word:
                if self.active_word.type_char(char):
                    self.correct_chars += 1
                    if self.active_word.completed:
                        self.complete_word(self.active_word)
                else:
                    # Wrong character, reset
                    self.current_input = ""
                    self.active_word.typed_chars = 0
                    self.active_word = None
    
    def complete_word(self, word):
        """Handle word completion"""
        self.score += len(word.word) * 10 * self.level
        self.words_typed += 1
        self.chars_typed += len(word.word)
        self.falling_words.remove(word)
        self.current_input = ""
        self.active_word = None
        
        # Level up every 10 words
        if self.words_typed % 10 == 0:
            self.level = min(5, self.level + 1)
            self.spawn_delay = max(800, self.spawn_delay - 200)
    
    def start_game(self):
        """Start the game"""
        self.game_started = True
        self.start_time = pygame.time.get_ticks()
        self.start_time_stats = time.time()
        self.last_word_spawn = self.start_time
    
    def restart_game(self):
        """Restart the game"""
        self.falling_words = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.words_typed = 0
        self.chars_typed = 0
        self.game_started = False
        self.game_over = False
        self.current_input = ""
        self.active_word = None
        self.spawn_delay = 2000
        self.total_chars = 0
        self.correct_chars = 0
    
    def spawn_word(self):
        """Spawn a new falling word"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_word_spawn > self.spawn_delay:
            word_list = self.word_lists.get(self.level, self.word_lists[5])
            word = random.choice(word_list)
            x = random.randint(50, SCREEN_WIDTH - 200)
            speed = 1 + (self.level - 1) * 0.5
            
            new_word = FallingWord(word, x, 0, speed)
            self.falling_words.append(new_word)
            self.last_word_spawn = current_time
    
    def update(self):
        if not self.game_started or self.game_over:
            return
        
        # Spawn new words
        self.spawn_word()
        
        # Update falling words
        words_to_remove = []
        for word in self.falling_words:
            word.update()
            
            # Check if word reached bottom
            if word.y > SCREEN_HEIGHT - 100:
                if not word.completed:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                words_to_remove.append(word)
        
        # Remove words that reached bottom
        for word in words_to_remove:
            if word in self.falling_words:
                self.falling_words.remove(word)
            if word == self.active_word:
                self.active_word = None
                self.current_input = ""
    
    def calculate_wpm(self):
        """Calculate words per minute"""
        if not self.start_time_stats:
            return 0
        
        elapsed_time = time.time() - self.start_time_stats
        if elapsed_time < 1:
            return 0
        
        # Standard WPM calculation: (characters typed / 5) / minutes
        minutes = elapsed_time / 60
        wpm = (self.correct_chars / 5) / minutes
        return int(wpm)
    
    def calculate_accuracy(self):
        """Calculate typing accuracy"""
        if self.total_chars == 0:
            return 100
        return int((self.correct_chars / self.total_chars) * 100)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.title_font.render("Speed Typing", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        if not self.game_started:
            self.draw_start_screen()
        elif self.game_over:
            self.draw_game_over()
        else:
            self.draw_game()
        
        pygame.display.flip()
    
    def draw_start_screen(self):
        """Draw start screen"""
        start_text = self.ui_font.render("Press SPACE to start typing!", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        instructions = [
            "Type the falling words before they reach the bottom!",
            "Complete words to score points and advance levels",
            "You have 3 lives - don't let words fall!",
            "ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_game(self):
        """Draw main game"""
        # Draw falling words
        for word in self.falling_words:
            word.draw(self.screen)
        
        # Draw UI
        ui_y = 100
        ui_texts = [
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Lives: {self.lives}",
            f"Words: {self.words_typed}",
            f"WPM: {self.calculate_wpm()}",
            f"Accuracy: {self.calculate_accuracy()}%"
        ]
        
        for i, text in enumerate(ui_texts):
            color = WHITE
            if i == 2 and self.lives <= 1:  # Lives warning
                color = RED
            elif i == 4:  # WPM color coding
                wpm = self.calculate_wpm()
                if wpm >= 60:
                    color = GREEN
                elif wpm >= 40:
                    color = YELLOW
                else:
                    color = WHITE
            
            ui_text = self.ui_font.render(text, True, color)
            self.screen.blit(ui_text, (20, ui_y + i * 35))
        
        # Draw input area
        input_rect = pygame.Rect(50, SCREEN_HEIGHT - 80, SCREEN_WIDTH - 100, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        
        # Current input
        input_text = self.input_font.render(self.current_input, True, GREEN if self.active_word else WHITE)
        self.screen.blit(input_text, (input_rect.x + 10, input_rect.y + 5))
        
        # Instructions
        instruction_text = self.small_font.render("Type the falling words! ESC to exit", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        game_over_text = self.title_font.render("Game Over!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final stats
        stats = [
            f"Final Score: {self.score}",
            f"Words Typed: {self.words_typed}",
            f"Level Reached: {self.level}",
            f"Final WPM: {self.calculate_wpm()}",
            f"Accuracy: {self.calculate_accuracy()}%"
        ]
        
        for i, stat in enumerate(stats):
            color = WHITE
            if i == 3:  # WPM color coding
                wpm = self.calculate_wpm()
                if wpm >= 60:
                    color = GREEN
                elif wpm >= 40:
                    color = YELLOW
            
            stat_text = self.ui_font.render(stat, True, color)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 40))
            self.screen.blit(stat_text, stat_rect)
        
        # Restart instruction
        restart_text = self.ui_font.render("Press R to restart, ESC to exit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    game = TypingGame()
    game.run()

if __name__ == "__main__":
    main()
