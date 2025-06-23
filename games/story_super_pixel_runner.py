#!/usr/bin/env python3
"""
Super Pixel Runner - Story Enhanced Version
Memory Lane Protocol: Navigate through fragmented memories of simpler times

STORY CONTEXT:
This simulation represents Commander Nova's earliest memory fragments - 
childhood dreams of endless running through digital landscapes. Each level 
recovered helps rebuild neural pathways and unlock deeper memories.
"""

import pygame
import random
import sys
import math
import json
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Enhanced Colors with story theming
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)
RED = (255, 64, 64)
GREEN = (64, 255, 64)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
PURPLE = (128, 64, 255)
CYAN = (64, 255, 255)

# Memory-themed colors
MEMORY_BLUE = (100, 200, 255)
FRAGMENT_GOLD = (255, 200, 100)
CORRUPTION_RED = (200, 50, 50)

class MemoryFragment:
    """Collectible story elements that unlock narrative"""
    
    def __init__(self, x, y, fragment_type="memory"):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.fragment_type = fragment_type
        self.collected = False
        self.pulse_timer = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Story data
        self.story_text = {
            "memory": "A fragment of childhood joy...",
            "skill": "Motor coordination improving...",
            "awareness": "Something feels... artificial..."
        }
    
    def update(self, dt):
        self.pulse_timer += dt * 5
    
    def draw(self, screen, camera_x):
        if not self.collected:
            # Pulsing effect
            pulse = 1.0 + 0.3 * math.sin(self.pulse_timer)
            size = int(self.width * pulse)
            
            # Draw glow
            glow_color = FRAGMENT_GOLD if self.fragment_type == "memory" else CYAN
            pygame.draw.circle(screen, glow_color, 
                             (int(self.x - camera_x + self.width//2), 
                              int(self.y + self.height//2)), size + 5)
            
            # Draw fragment
            pygame.draw.circle(screen, WHITE, 
                             (int(self.x - camera_x + self.width//2), 
                              int(self.y + self.height//2)), size)

class StoryPlayer:
    """Enhanced player with story progression tracking"""
    
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
        
        # Story progression
        self.memories_collected = 0
        self.skills_gained = 0
        self.awareness_level = 0
        self.corruption_resistance = 100
        
        # Visual effects
        self.trail_particles = []
        self.aura_intensity = 0
    
    def update(self, platforms, dt):
        # Handle input with story context
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        # Movement feels more responsive as skills improve
        speed_multiplier = 1.0 + (self.skills_gained * 0.1)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed * speed_multiplier
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed * speed_multiplier
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_power * (1.0 + self.skills_gained * 0.05)
            self.on_ground = False
        
        # Apply gravity
        self.vel_y += 0.8
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
            self.rect.x = self.x
        
        # Update visual effects
        self.update_effects(dt)
    
    def update_effects(self, dt):
        """Update visual effects based on story progression"""
        # Aura intensity based on memories collected
        target_aura = min(1.0, self.memories_collected / 10.0)
        self.aura_intensity += (target_aura - self.aura_intensity) * dt * 3
        
        # Add trail particles
        if len(self.trail_particles) < 20:
            self.trail_particles.append({
                'x': self.x + self.width//2,
                'y': self.y + self.height//2,
                'life': 30,
                'color': MEMORY_BLUE if self.memories_collected > 0 else WHITE
            })
        
        # Update particles
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
    
    def collect_memory(self, fragment):
        """Collect a memory fragment and gain story progression"""
        if fragment.fragment_type == "memory":
            self.memories_collected += 1
        elif fragment.fragment_type == "skill":
            self.skills_gained += 1
        elif fragment.fragment_type == "awareness":
            self.awareness_level += 1
        
        fragment.collected = True
    
    def draw(self, screen, camera_x):
        # Draw trail particles
        for particle in self.trail_particles:
            alpha = int(255 * (particle['life'] / 30))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x'] - camera_x), int(particle['y'])), 3)
        
        # Draw aura if memories collected
        if self.aura_intensity > 0:
            aura_size = int(40 * self.aura_intensity)
            aura_color = (*MEMORY_BLUE, int(50 * self.aura_intensity))
            pygame.draw.circle(screen, MEMORY_BLUE, 
                             (int(self.x - camera_x + self.width//2), 
                              int(self.y + self.height//2)), aura_size)
        
        # Draw player
        player_color = WHITE
        if self.memories_collected > 5:
            player_color = MEMORY_BLUE
        elif self.awareness_level > 3:
            player_color = CYAN
        
        pygame.draw.rect(screen, player_color, 
                        (int(self.x - camera_x), int(self.y), self.width, self.height))
        
        # Draw eyes (more detailed as awareness increases)
        eye_size = 4 + self.awareness_level
        pygame.draw.circle(screen, BLACK, 
                         (int(self.x - camera_x + 8), int(self.y + 8)), eye_size)
        pygame.draw.circle(screen, BLACK, 
                         (int(self.x - camera_x + 24), int(self.y + 8)), eye_size)

class CorruptedEnemy:
    """Enemies representing memory corruption"""
    
    def __init__(self, x, y, corruption_type="glitch"):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.speed = random.uniform(1, 3)
        self.corruption_type = corruption_type
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.glitch_timer = 0
        self.phase_shift = random.uniform(0, math.pi * 2)
    
    def update(self, dt):
        # Erratic movement representing corruption
        self.glitch_timer += dt * 8
        
        if self.corruption_type == "glitch":
            # Jittery movement
            self.x += self.speed + random.uniform(-1, 1)
            self.y += math.sin(self.glitch_timer + self.phase_shift) * 2
        elif self.corruption_type == "virus":
            # Aggressive pursuit behavior
            self.x += self.speed * 1.5
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen, camera_x):
        # Glitchy visual effects
        colors = [CORRUPTION_RED, BLACK, WHITE]
        color = random.choice(colors) if random.random() < 0.3 else CORRUPTION_RED
        
        # Draw with distortion
        offset_x = random.randint(-2, 2) if self.corruption_type == "glitch" else 0
        offset_y = random.randint(-2, 2) if self.corruption_type == "glitch" else 0
        
        pygame.draw.rect(screen, color, 
                        (int(self.x - camera_x + offset_x), 
                         int(self.y + offset_y), self.width, self.height))

class StoryHUD:
    """Enhanced HUD showing story progression"""
    
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.story_messages = []
        self.message_timer = 0
    
    def add_story_message(self, message, duration=3.0):
        """Add a story message to display"""
        self.story_messages.append({
            'text': message,
            'timer': duration,
            'alpha': 255
        })
    
    def update(self, dt):
        """Update story messages"""
        for message in self.story_messages[:]:
            message['timer'] -= dt
            if message['timer'] <= 0:
                self.story_messages.remove(message)
            elif message['timer'] < 1.0:
                message['alpha'] = int(255 * message['timer'])
    
    def draw(self, screen, player):
        # Story progression panel
        panel_width = 300
        panel_height = 120
        panel_x = 10
        panel_y = 10
        
        # Background
        pygame.draw.rect(screen, (0, 0, 0, 180), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, MEMORY_BLUE, (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Title
        title_text = self.font.render("Memory Recovery", True, FRAGMENT_GOLD)
        screen.blit(title_text, (panel_x + 10, panel_y + 10))
        
        # Stats
        stats = [
            f"Memories: {player.memories_collected}",
            f"Skills: {player.skills_gained}",
            f"Awareness: {player.awareness_level}",
            f"Integrity: {player.corruption_resistance}%"
        ]
        
        y_offset = 35
        for stat in stats:
            color = WHITE
            if "Memories" in stat and player.memories_collected > 0:
                color = FRAGMENT_GOLD
            elif "Awareness" in stat and player.awareness_level > 0:
                color = CYAN
            
            stat_surface = self.small_font.render(stat, True, color)
            screen.blit(stat_surface, (panel_x + 10, panel_y + y_offset))
            y_offset += 20
        
        # Story messages
        message_y = SCREEN_HEIGHT - 100
        for message in self.story_messages:
            text_surface = self.font.render(message['text'], True, WHITE)
            # Create surface with alpha
            alpha_surface = pygame.Surface(text_surface.get_size())
            alpha_surface.set_alpha(message['alpha'])
            alpha_surface.blit(text_surface, (0, 0))
            
            text_rect = alpha_surface.get_rect(center=(SCREEN_WIDTH // 2, message_y))
            screen.blit(alpha_surface, text_rect)
            message_y -= 30

class MemoryLaneGame:
    """Main game class with story integration"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Memory Lane Protocol - GameVerse Hub")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = StoryPlayer(100, 500)
        self.platforms = self.create_platforms()
        self.memory_fragments = self.create_memory_fragments()
        self.enemies = []
        self.camera_x = 0
        
        # Story system
        self.story_hud = StoryHUD()
        self.level_progress = 0
        self.story_triggered = set()
        
        # Background
        self.background_scroll = 0
        
        # Initialize story
        self.story_hud.add_story_message("Memory Lane Protocol Initiated...")
        self.story_hud.add_story_message("Recover fragments to rebuild your past...")
    
    def create_platforms(self):
        """Create platforms with story-themed design"""
        platforms = []
        
        # Ground platforms
        for x in range(0, 3000, 200):
            platforms.append(Platform(x, SCREEN_HEIGHT - 50, 200, 50))
        
        # Floating memory platforms
        for i in range(10):
            x = 300 + i * 250
            y = SCREEN_HEIGHT - 200 - random.randint(0, 200)
            platforms.append(Platform(x, y, 150, 20))
        
        return platforms
    
    def create_memory_fragments(self):
        """Create collectible memory fragments"""
        fragments = []
        
        # Distribute fragments across the level
        for i in range(15):
            x = 200 + i * 180 + random.randint(-50, 50)
            y = SCREEN_HEIGHT - 300 - random.randint(0, 200)
            
            # Different types of fragments
            if i % 5 == 0:
                fragment_type = "awareness"
            elif i % 3 == 0:
                fragment_type = "skill"
            else:
                fragment_type = "memory"
            
            fragments.append(MemoryFragment(x, y, fragment_type))
        
        return fragments
    
    def spawn_corruption(self):
        """Spawn corrupted enemies based on story progression"""
        if len(self.enemies) < 5 and random.random() < 0.02:
            x = self.camera_x + SCREEN_WIDTH + 50
            y = SCREEN_HEIGHT - 100
            
            corruption_type = "glitch"
            if self.player.awareness_level > 3:
                corruption_type = "virus"
            
            self.enemies.append(CorruptedEnemy(x, y, corruption_type))
    
    def update_story_triggers(self):
        """Check for story progression triggers"""
        # First memory collected
        if self.player.memories_collected == 1 and "first_memory" not in self.story_triggered:
            self.story_hud.add_story_message("Memory fragment recovered... images of childhood...")
            self.story_triggered.add("first_memory")
        
        # Skill development
        if self.player.skills_gained == 2 and "skill_growth" not in self.story_triggered:
            self.story_hud.add_story_message("Motor functions improving... you feel more agile...")
            self.story_triggered.add("skill_growth")
        
        # Awareness awakening
        if self.player.awareness_level == 1 and "awareness_dawn" not in self.story_triggered:
            self.story_hud.add_story_message("Something's wrong... this world feels artificial...")
            self.story_triggered.add("awareness_dawn")
        
        # High awareness
        if self.player.awareness_level >= 3 and "reality_doubt" not in self.story_triggered:
            self.story_hud.add_story_message("The corruption spreads... you're trapped in a simulation!")
            self.story_triggered.add("reality_doubt")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_progress()
                    self.running = False
                elif event.key == pygame.K_r:
                    # Reset for testing
                    self.__init__()
    
    def update(self, dt):
        """Update game state"""
        # Update player
        self.player.update(self.platforms, dt)
        
        # Update camera to follow player
        target_camera_x = self.player.x - SCREEN_WIDTH // 3
        self.camera_x += (target_camera_x - self.camera_x) * dt * 5
        
        # Update memory fragments
        for fragment in self.memory_fragments:
            fragment.update(dt)
            
            # Check collection
            if not fragment.collected and self.player.rect.colliderect(fragment.rect):
                self.player.collect_memory(fragment)
                self.story_hud.add_story_message(fragment.story_text[fragment.fragment_type])
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt)
            
            # Remove off-screen enemies
            if enemy.x < self.camera_x - 100:
                self.enemies.remove(enemy)
            
            # Check collision with player
            if self.player.rect.colliderect(enemy.rect):
                self.player.corruption_resistance -= 10
                self.enemies.remove(enemy)
                self.story_hud.add_story_message("Corruption detected! Memory integrity compromised!")
        
        # Spawn new corruption
        self.spawn_corruption()
        
        # Update story system
        self.story_hud.update(dt)
        self.update_story_triggers()
        
        # Update background
        self.background_scroll += dt * 20
        
        # Check win condition
        if self.player.memories_collected >= 10:
            self.complete_simulation()
    
    def complete_simulation(self):
        """Complete the memory lane simulation"""
        self.story_hud.add_story_message("Memory Lane Protocol Complete!")
        self.story_hud.add_story_message("Neural pathways restored... new memories unlocked...")
        self.save_progress()
        
        # Wait a moment then exit
        pygame.time.wait(3000)
        self.running = False
    
    def save_progress(self):
        """Save story progress"""
        progress_data = {
            'memories_collected': self.player.memories_collected,
            'skills_gained': self.player.skills_gained,
            'awareness_level': self.player.awareness_level,
            'completed': self.player.memories_collected >= 10
        }
        
        try:
            with open('super_pixel_runner_progress.json', 'w') as f:
                json.dump(progress_data, f)
        except Exception as e:
            print(f"Could not save progress: {e}")
    
    def draw_background(self):
        """Draw story-themed background"""
        # Memory-themed gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(20 + 30 * ratio)
            g = int(50 + 100 * ratio)
            b = int(100 + 155 * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Floating memory particles
        particle_offset = int(self.background_scroll) % 100
        for x in range(-100, SCREEN_WIDTH + 100, 100):
            for y in range(0, SCREEN_HEIGHT, 150):
                alpha = 50 + 30 * math.sin((x + y + self.background_scroll) * 0.01)
                color = (*MEMORY_BLUE[:3], int(alpha))
                pygame.draw.circle(self.screen, MEMORY_BLUE, 
                                 (x + particle_offset, y), 2)
    
    def draw(self):
        """Main draw method"""
        self.draw_background()
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)
        
        # Draw memory fragments
        for fragment in self.memory_fragments:
            fragment.draw(self.screen, self.camera_x)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)
        
        # Draw player
        self.player.draw(self.screen, self.camera_x)
        
        # Draw HUD
        self.story_hud.draw(self.screen, self.player)
        
        # Draw story overlay if corruption is high
        if self.player.corruption_resistance < 50:
            # Red overlay for corruption
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(int(100 * (1 - self.player.corruption_resistance / 100)))
            overlay.fill(CORRUPTION_RED)
            self.screen.blit(overlay, (0, 0))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("🧠 Memory Lane Protocol - Initializing...")
        print("Story Context: Navigate through fragmented memories to rebuild your past")
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

class Platform:
    """Simple platform class"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen, camera_x):
        # Memory-themed platform appearance
        platform_color = GRAY
        if random.random() < 0.1:  # Occasional memory glints
            platform_color = FRAGMENT_GOLD
        
        pygame.draw.rect(screen, platform_color, 
                        (int(self.x - camera_x), int(self.y), self.width, self.height))
        pygame.draw.rect(screen, WHITE, 
                        (int(self.x - camera_x), int(self.y), self.width, self.height), 2)

def main():
    """Main entry point"""
    try:
        game = MemoryLaneGame()
        game.run()
    except Exception as e:
        print(f"Error running Memory Lane Protocol: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
