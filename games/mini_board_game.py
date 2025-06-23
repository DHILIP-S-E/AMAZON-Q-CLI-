#!/usr/bin/env python3
"""
Mini Board Game - Tic-Tac-Toe with AI
Part of GameVerse Hub
"""

import pygame
import random
import sys

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
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini Board Game - Tic-Tac-Toe!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.game_font = pygame.font.Font(None, 128)
        self.ui_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X is human, O is AI
        self.game_over = False
        self.winner = None
        self.player_score = 0
        self.ai_score = 0
        self.ties = 0
        
        # Board setup
        self.board_size = 450
        self.cell_size = self.board_size // 3
        self.board_x = (SCREEN_WIDTH - self.board_size) // 2
        self.board_y = (SCREEN_HEIGHT - self.board_size) // 2
        
        # AI difficulty
        self.ai_difficulty = 'medium'  # easy, medium, hard
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_1:
                    self.ai_difficulty = 'easy'
                elif event.key == pygame.K_2:
                    self.ai_difficulty = 'medium'
                elif event.key == pygame.K_3:
                    self.ai_difficulty = 'hard'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over and self.current_player == 'X':
                    self.handle_mouse_click(event.pos)
    
    def handle_mouse_click(self, pos):
        """Handle player moves"""
        # Check if click is within the board
        if (self.board_x <= pos[0] <= self.board_x + self.board_size and
            self.board_y <= pos[1] <= self.board_y + self.board_size):
            
            # Calculate grid position
            col = (pos[0] - self.board_x) // self.cell_size
            row = (pos[1] - self.board_y) // self.cell_size
            
            # Make move if cell is empty
            if self.board[row][col] == '':
                self.make_move(row, col, 'X')
    
    def make_move(self, row, col, player):
        """Make a move on the board"""
        self.board[row][col] = player
        
        # Check for win or tie
        if self.check_winner():
            self.game_over = True
            self.winner = player
            if player == 'X':
                self.player_score += 1
            else:
                self.ai_score += 1
        elif self.is_board_full():
            self.game_over = True
            self.winner = 'Tie'
            self.ties += 1
        else:
            # Switch players
            self.current_player = 'O' if player == 'X' else 'X'
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        
        return False
    
    def is_board_full(self):
        """Check if board is full"""
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def get_empty_cells(self):
        """Get list of empty cells"""
        empty = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    empty.append((row, col))
        return empty
    
    def ai_move(self):
        """AI makes a move based on difficulty"""
        if self.ai_difficulty == 'easy':
            self.ai_move_easy()
        elif self.ai_difficulty == 'medium':
            self.ai_move_medium()
        else:
            self.ai_move_hard()
    
    def ai_move_easy(self):
        """Easy AI - random moves"""
        empty_cells = self.get_empty_cells()
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col, 'O')
    
    def ai_move_medium(self):
        """Medium AI - block player wins, otherwise random"""
        # First, try to win
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'O'
            if self.check_winner():
                self.make_move(row, col, 'O')
                return
            self.board[row][col] = ''
        
        # Then, try to block player
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'X'
            if self.check_winner():
                self.board[row][col] = ''
                self.make_move(row, col, 'O')
                return
            self.board[row][col] = ''
        
        # Otherwise, random move
        self.ai_move_easy()
    
    def ai_move_hard(self):
        """Hard AI - minimax algorithm"""
        best_score = float('-inf')
        best_move = None
        
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'O'
            score = self.minimax(self.board, 0, False)
            self.board[row][col] = ''
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        if best_move:
            self.make_move(best_move[0], best_move[1], 'O')
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm for AI"""
        # Check terminal states
        if self.check_winner():
            if is_maximizing:
                return -1
            else:
                return 1
        elif self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for row, col in self.get_empty_cells():
                board[row][col] = 'O'
                score = self.minimax(board, depth + 1, False)
                board[row][col] = ''
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in self.get_empty_cells():
                board[row][col] = 'X'
                score = self.minimax(board, depth + 1, True)
                board[row][col] = ''
                best_score = min(score, best_score)
            return best_score
    
    def reset_game(self):
        """Reset the game board"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def update(self):
        """Update game state"""
        if not self.game_over and self.current_player == 'O':
            # AI turn with small delay
            pygame.time.wait(500)
            self.ai_move()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.title_font.render("Tic-Tac-Toe", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw board
        self.draw_board()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_board(self):
        """Draw the game board"""
        # Board background
        board_rect = pygame.Rect(self.board_x, self.board_y, self.board_size, self.board_size)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        
        # Grid lines
        for i in range(1, 3):
            # Vertical lines
            x = self.board_x + i * self.cell_size
            pygame.draw.line(self.screen, BLACK, (x, self.board_y), (x, self.board_y + self.board_size), 3)
            
            # Horizontal lines
            y = self.board_y + i * self.cell_size
            pygame.draw.line(self.screen, BLACK, (self.board_x, y), (self.board_x + self.board_size, y), 3)
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != '':
                    x = self.board_x + col * self.cell_size + self.cell_size // 2
                    y = self.board_y + row * self.cell_size + self.cell_size // 2
                    
                    color = BLUE if self.board[row][col] == 'X' else RED
                    symbol_text = self.game_font.render(self.board[row][col], True, color)
                    symbol_rect = symbol_text.get_rect(center=(x, y))
                    self.screen.blit(symbol_text, symbol_rect)
    
    def draw_ui(self):
        """Draw UI elements"""
        # Current player or game result
        if self.game_over:
            if self.winner == 'Tie':
                result_text = "It's a Tie!"
                color = YELLOW
            elif self.winner == 'X':
                result_text = "You Win!"
                color = GREEN
            else:
                result_text = "AI Wins!"
                color = RED
        else:
            if self.current_player == 'X':
                result_text = "Your Turn (X)"
                color = BLUE
            else:
                result_text = "AI Turn (O)"
                color = RED
        
        status_text = self.ui_font.render(result_text, True, color)
        status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(status_text, status_rect)
        
        # Score
        score_text = self.ui_font.render(f"You: {self.player_score}  AI: {self.ai_score}  Ties: {self.ties}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(score_text, score_rect)
        
        # AI Difficulty
        difficulty_text = self.small_font.render(f"AI Difficulty: {self.ai_difficulty.title()}", True, WHITE)
        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
        self.screen.blit(difficulty_text, difficulty_rect)
        
        # Instructions
        instructions = [
            "Click to place X",
            "R: New Game",
            "1/2/3: AI Difficulty",
            "ESC: Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (20, 150 + i * 25))
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    game = TicTacToe()
    game.run()

if __name__ == "__main__":
    main()
