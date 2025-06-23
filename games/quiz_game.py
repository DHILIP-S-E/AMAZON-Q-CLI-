#!/usr/bin/env python3
"""
Quiz Game - Multiple Choice Questions with Score Tracking
Part of GameVerse Hub
"""

import pygame
import random
import sys
import json

pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)
GREEN = (64, 255, 64)
RED = (255, 64, 64)
YELLOW = (255, 255, 64)
PURPLE = (128, 64, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class QuizGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quiz Master - Test Your Knowledge!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.question_font = pygame.font.Font(None, 36)
        self.answer_font = pygame.font.Font(None, 28)
        self.score_font = pygame.font.Font(None, 32)
        
        # Game state
        self.current_question = 0
        self.score = 0
        self.total_questions = 0
        self.selected_answer = -1
        self.show_result = False
        self.correct_answer = -1
        self.game_over = False
        
        # Load questions
        self.questions = self.load_questions()
        self.total_questions = len(self.questions)
        random.shuffle(self.questions)
        
        # Answer buttons
        self.answer_buttons = []
        self.setup_answer_buttons()
    
    def load_questions(self):
        """Load quiz questions - mix of categories"""
        questions = [
            {
                "question": "What is the capital of France?",
                "answers": ["London", "Berlin", "Paris", "Madrid"],
                "correct": 2
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "answers": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1
            },
            {
                "question": "What is 15 × 8?",
                "answers": ["120", "125", "115", "130"],
                "correct": 0
            },
            {
                "question": "Who painted the Mona Lisa?",
                "answers": ["Van Gogh", "Picasso", "Da Vinci", "Monet"],
                "correct": 2
            },
            {
                "question": "What is the largest ocean on Earth?",
                "answers": ["Atlantic", "Indian", "Arctic", "Pacific"],
                "correct": 3
            },
            {
                "question": "In which year did World War II end?",
                "answers": ["1944", "1945", "1946", "1947"],
                "correct": 1
            },
            {
                "question": "What is the chemical symbol for gold?",
                "answers": ["Go", "Gd", "Au", "Ag"],
                "correct": 2
            },
            {
                "question": "Which programming language is known for AI?",
                "answers": ["Python", "Java", "C++", "JavaScript"],
                "correct": 0
            },
            {
                "question": "What is the square root of 144?",
                "answers": ["11", "12", "13", "14"],
                "correct": 1
            },
            {
                "question": "Which country invented pizza?",
                "answers": ["France", "Spain", "Italy", "Greece"],
                "correct": 2
            }
        ]
        return questions
    
    def setup_answer_buttons(self):
        """Setup answer button rectangles"""
        button_width = 400
        button_height = 60
        start_x = (SCREEN_WIDTH - button_width) // 2
        start_y = 350
        spacing = 80
        
        self.answer_buttons = []
        for i in range(4):
            rect = pygame.Rect(start_x, start_y + i * spacing, button_width, button_height)
            self.answer_buttons.append(rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and (self.show_result or self.game_over):
                    self.next_question()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
    
    def handle_mouse_click(self, pos):
        if self.show_result or self.game_over:
            return
        
        # Check answer button clicks
        for i, button in enumerate(self.answer_buttons):
            if button.collidepoint(pos):
                self.selected_answer = i
                self.check_answer()
                break
    
    def check_answer(self):
        if self.current_question < len(self.questions):
            self.correct_answer = self.questions[self.current_question]["correct"]
            if self.selected_answer == self.correct_answer:
                self.score += 1
            self.show_result = True
    
    def next_question(self):
        if self.game_over:
            return
        
        self.current_question += 1
        self.selected_answer = -1
        self.show_result = False
        self.correct_answer = -1
        
        if self.current_question >= len(self.questions):
            self.game_over = True
    
    def restart_game(self):
        self.current_question = 0
        self.score = 0
        self.selected_answer = -1
        self.show_result = False
        self.correct_answer = -1
        self.game_over = False
        random.shuffle(self.questions)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.title_font.render("Quiz Master", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Score and progress
        score_text = self.score_font.render(f"Score: {self.score}/{self.current_question}", True, WHITE)
        self.screen.blit(score_text, (50, 100))
        
        progress_text = self.score_font.render(f"Question {self.current_question + 1}/{self.total_questions}", True, WHITE)
        progress_rect = progress_text.get_rect(topright=(SCREEN_WIDTH - 50, 100))
        self.screen.blit(progress_text, progress_rect)
        
        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_question()
        
        # Instructions
        if self.show_result:
            instruction = "Press SPACE to continue"
        elif self.game_over:
            instruction = "Press R to restart, ESC to exit"
        else:
            instruction = "Click an answer, ESC to exit"
        
        instruction_text = self.answer_font.render(instruction, True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def draw_question(self):
        if self.current_question >= len(self.questions):
            return
        
        question_data = self.questions[self.current_question]
        
        # Question text
        question_text = self.question_font.render(question_data["question"], True, WHITE)
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(question_text, question_rect)
        
        # Answer buttons
        for i, (button, answer) in enumerate(zip(self.answer_buttons, question_data["answers"])):
            # Button color logic
            if self.show_result:
                if i == self.correct_answer:
                    color = GREEN
                elif i == self.selected_answer and i != self.correct_answer:
                    color = RED
                else:
                    color = DARK_GRAY
            else:
                color = BLUE if i != self.selected_answer else PURPLE
            
            # Draw button
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, WHITE, button, 2)
            
            # Answer text
            answer_text = self.answer_font.render(f"{chr(65 + i)}. {answer}", True, WHITE)
            text_rect = answer_text.get_rect(center=button.center)
            self.screen.blit(answer_text, text_rect)
    
    def draw_game_over(self):
        # Final score
        percentage = (self.score / self.total_questions) * 100
        
        final_score_text = self.title_font.render("Quiz Complete!", True, YELLOW)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(final_score_text, final_score_rect)
        
        score_text = self.question_font.render(f"Final Score: {self.score}/{self.total_questions}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(score_text, score_rect)
        
        percentage_text = self.question_font.render(f"Percentage: {percentage:.1f}%", True, WHITE)
        percentage_rect = percentage_text.get_rect(center=(SCREEN_WIDTH // 2, 370))
        self.screen.blit(percentage_text, percentage_rect)
        
        # Performance message
        if percentage >= 90:
            message = "Excellent! You're a quiz master!"
            color = GREEN
        elif percentage >= 70:
            message = "Great job! Well done!"
            color = BLUE
        elif percentage >= 50:
            message = "Good effort! Keep practicing!"
            color = YELLOW
        else:
            message = "Keep studying and try again!"
            color = RED
        
        message_text = self.answer_font.render(message, True, color)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(message_text, message_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    game = QuizGame()
    game.run()

if __name__ == "__main__":
    main()
