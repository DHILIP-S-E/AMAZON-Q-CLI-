#!/usr/bin/env python3
"""
GameVerse Hub - Comprehensive Game Testing & Demo Script
Tests games by analyzing code structure and provides detailed reports
"""

import ast
import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple

class GameTester:
    """Comprehensive game testing without requiring pygame execution"""
    
    def __init__(self, games_folder: str = "games"):
        self.games_folder = Path(games_folder)
        self.results = {}
        
    def test_all_games(self):
        """Test all games comprehensively"""
        print("🎮 GameVerse Hub - Comprehensive Game Testing")
        print("=" * 60)
        
        game_files = list(self.games_folder.glob("*.py"))
        game_files = [f for f in game_files if not f.name.startswith("__")]
        
        print(f"Testing {len(game_files)} games...\n")
        
        # Categorize games
        full_games = []
        placeholder_games = []
        broken_games = []
        
        for game_file in sorted(game_files):
            print(f"🔍 Analyzing {game_file.name}...")
            result = self._comprehensive_test(game_file)
            self.results[game_file.name] = result
            
            if result['status'] == 'FULL':
                full_games.append(result)
            elif result['status'] == 'PLACEHOLDER':
                placeholder_games.append(result)
            else:
                broken_games.append(result)
        
        # Print detailed results
        self._print_detailed_results(full_games, placeholder_games, broken_games)
        
        return full_games, placeholder_games, broken_games
    
    def _comprehensive_test(self, game_file: Path) -> Dict:
        """Perform comprehensive testing on a single game"""
        result = {
            'name': game_file.stem,
            'file': game_file.name,
            'title': '',
            'description': '',
            'category': 'unknown',
            'status': 'UNKNOWN',
            'file_size': game_file.stat().st_size,
            'line_count': 0,
            'syntax_valid': False,
            'pygame_integration': False,
            'game_loop_present': False,
            'event_handling': False,
            'classes': [],
            'functions': [],
            'game_features': [],
            'complexity_score': 0,
            'estimated_playtime': '5-15 min',
            'issues': [],
            'recommendations': []
        }
        
        try:
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result['line_count'] = len(content.split('\n'))
            
            # Test syntax
            try:
                tree = ast.parse(content)
                result['syntax_valid'] = True
            except SyntaxError as e:
                result['issues'].append(f"Syntax error: {e}")
                result['status'] = 'BROKEN'
                return result
            
            # Extract metadata
            result['title'] = self._extract_title(content, game_file.stem)
            result['description'] = self._extract_description(content)
            result['category'] = self._detect_category(content)
            
            # Analyze code structure
            self._analyze_code_structure(tree, content, result)
            
            # Determine game status
            result['status'] = self._determine_status(content, result)
            
            # Calculate complexity
            result['complexity_score'] = self._calculate_complexity(result)
            
            # Generate recommendations
            self._generate_recommendations(result)
            
        except Exception as e:
            result['issues'].append(f"Analysis error: {str(e)}")
            result['status'] = 'BROKEN'
        
        return result
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract game title from various sources"""
        lines = content.split('\n')
        
        # Check docstring first
        if '"""' in content:
            try:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    docstring = content[start:end].strip()
                    first_line = docstring.split('\n')[0].strip()
                    if first_line and len(first_line) > 3 and 'placeholder' not in first_line.lower():
                        return first_line
            except:
                pass
        
        # Check comments
        for line in lines[:20]:
            line = line.strip()
            if line.startswith('#') and any(word in line.lower() for word in ['title', 'name']):
                if ':' in line or '-' in line:
                    title = line.split(':', 1)[-1].split('-', 1)[-1].strip()
                    if title and len(title) > 3:
                        return title
        
        # Check pygame.display.set_caption
        if 'pygame.display.set_caption' in content:
            try:
                start = content.find('pygame.display.set_caption(') + 27
                end = content.find(')', start)
                caption = content[start:end].strip().strip('"\'')
                if caption and len(caption) > 3:
                    return caption
            except:
                pass
        
        return filename.replace('_', ' ').title()
    
    def _extract_description(self, content: str) -> str:
        """Extract game description"""
        if '"""' in content:
            try:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    docstring = content[start:end].strip()
                    lines = docstring.split('\n')
                    if len(lines) > 1:
                        desc = ' '.join(lines[1:]).strip()
                        if desc and 'placeholder' not in desc.lower():
                            return desc
            except:
                pass
        
        return "A Python game built with Pygame"
    
    def _detect_category(self, content: str) -> str:
        """Detect game category based on content analysis"""
        content_lower = content.lower()
        
        # Keyword-based detection with weights
        categories = {
            'platformer': ['platform', 'jump', 'gravity', 'player', 'ground', 'runner'],
            'shooter': ['shoot', 'bullet', 'enemy', 'alien', 'laser', 'weapon', 'storm'],
            'puzzle': ['puzzle', 'solve', 'brain', 'logic', 'number', 'maze', 'quiz'],
            'racing': ['race', 'car', 'speed', 'lap', 'track', 'vehicle', 'racer'],
            'arcade': ['break', 'brick', 'ball', 'paddle', 'score', 'level', 'breakout'],
            'clicker': ['click', 'increment', 'upgrade', 'idle', 'cookie', 'clicker'],
            'board': ['board', 'chess', 'checkers', 'turn', 'tic', 'tac', 'toe'],
            'typing': ['type', 'typing', 'keyboard', 'word', 'text', 'wpm'],
            'simulation': ['build', 'city', 'simulation', 'sim', 'manage', 'economy']
        }
        
        category_scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return 'arcade'
    
    def _analyze_code_structure(self, tree: ast.AST, content: str, result: Dict):
        """Analyze code structure and features"""
        # Find classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result['classes'].append(node.name)
        
        # Find functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result['functions'].append(node.name)
        
        # Check pygame integration
        pygame_features = {
            'pygame_init': 'pygame.init()',
            'display_setup': 'pygame.display.set_mode',
            'event_handling': 'pygame.event.get',
            'game_loop': 'while',
            'clock_control': 'pygame.time.Clock',
            'sprite_system': 'pygame.sprite',
            'collision_detection': 'collide',
            'sound_system': 'pygame.mixer'
        }
        
        for feature, pattern in pygame_features.items():
            if pattern in content:
                result['game_features'].append(feature)
        
        result['pygame_integration'] = 'pygame_init' in result['game_features']
        result['game_loop_present'] = 'game_loop' in result['game_features']
        result['event_handling'] = 'event_handling' in result['game_features']
        
        # Check for advanced features
        advanced_features = {
            'high_scores': ['score', 'high_score', 'best'],
            'levels': ['level', 'stage'],
            'power_ups': ['power', 'upgrade', 'bonus'],
            'ai_enemies': ['ai', 'enemy', 'bot'],
            'animations': ['animation', 'frame'],
            'particle_effects': ['particle', 'effect'],
            'save_system': ['save', 'load', 'file'],
            'settings_menu': ['settings', 'options', 'config']
        }
        
        for feature, keywords in advanced_features.items():
            if any(keyword in content.lower() for keyword in keywords):
                result['game_features'].append(feature)
    
    def _determine_status(self, content: str, result: Dict) -> str:
        """Determine if game is full, placeholder, or broken"""
        # Check for placeholder indicators
        if ('placeholder' in content.lower() or 
            'demo' in content.lower() or
            result['file_size'] < 2000):
            return 'PLACEHOLDER'
        
        # Check for broken game indicators
        if not result['syntax_valid']:
            return 'BROKEN'
        
        # Check for minimal game requirements
        if (result['pygame_integration'] and 
            result['game_loop_present'] and 
            result['event_handling'] and
            len(result['classes']) > 0):
            return 'FULL'
        
        # If it has some structure but not complete
        if result['pygame_integration'] or len(result['functions']) > 5:
            return 'PARTIAL'
        
        return 'PLACEHOLDER'
    
    def _calculate_complexity(self, result: Dict) -> int:
        """Calculate complexity score (0-100)"""
        score = 0
        
        # File size (0-20 points)
        score += min(20, result['file_size'] // 500)
        
        # Code structure (0-30 points)
        score += min(15, len(result['classes']) * 5)
        score += min(15, len(result['functions']) * 2)
        
        # Game features (0-30 points)
        score += min(30, len(result['game_features']) * 3)
        
        # Integration quality (0-20 points)
        if result['pygame_integration']:
            score += 5
        if result['game_loop_present']:
            score += 5
        if result['event_handling']:
            score += 5
        if 'collision_detection' in result['game_features']:
            score += 5
        
        return min(100, score)
    
    def _generate_recommendations(self, result: Dict):
        """Generate improvement recommendations"""
        if result['status'] == 'PLACEHOLDER':
            result['recommendations'].append("Implement core game mechanics")
            result['recommendations'].append("Add player interaction")
            result['recommendations'].append("Create game objectives")
        
        elif result['status'] == 'PARTIAL':
            if not result['pygame_integration']:
                result['recommendations'].append("Add proper pygame initialization")
            if not result['game_loop_present']:
                result['recommendations'].append("Implement main game loop")
            if not result['event_handling']:
                result['recommendations'].append("Add event handling system")
        
        elif result['status'] == 'FULL':
            if 'high_scores' not in result['game_features']:
                result['recommendations'].append("Add high score system")
            if 'sound_system' not in result['game_features']:
                result['recommendations'].append("Add sound effects and music")
            if 'save_system' not in result['game_features']:
                result['recommendations'].append("Implement save/load functionality")
    
    def _print_detailed_results(self, full_games: List, placeholder_games: List, broken_games: List):
        """Print comprehensive results"""
        total = len(full_games) + len(placeholder_games) + len(broken_games)
        
        print("\n" + "="*60)
        print("🎯 COMPREHENSIVE TEST RESULTS")
        print("="*60)
        
        print(f"\n📊 SUMMARY")
        print(f"Total Games: {total}")
        print(f"✅ Full Games: {len(full_games)} ({len(full_games)/total*100:.1f}%)")
        print(f"🔧 Placeholder Games: {len(placeholder_games)} ({len(placeholder_games)/total*100:.1f}%)")
        print(f"❌ Broken Games: {len(broken_games)} ({len(broken_games)/total*100:.1f}%)")
        
        # Full Games Section
        if full_games:
            print(f"\n🎮 FULL GAMES ({len(full_games)} games)")
            print("-" * 50)
            for game in sorted(full_games, key=lambda x: x['complexity_score'], reverse=True):
                self._print_game_details(game)
        
        # Placeholder Games Section
        if placeholder_games:
            print(f"\n🔧 PLACEHOLDER GAMES ({len(placeholder_games)} games)")
            print("-" * 50)
            for game in placeholder_games:
                self._print_game_summary(game)
        
        # Broken Games Section
        if broken_games:
            print(f"\n❌ BROKEN GAMES ({len(broken_games)} games)")
            print("-" * 50)
            for game in broken_games:
                self._print_game_summary(game, show_issues=True)
        
        # Quick Launch Guide
        if full_games:
            print(f"\n🚀 QUICK LAUNCH GUIDE")
            print("-" * 50)
            print("To test these games (requires pygame):")
            for game in full_games:
                print(f"python3 games/{game['file']} # {game['title']}")
    
    def _print_game_details(self, game: Dict):
        """Print detailed game information"""
        complexity_bar = "●" * (game['complexity_score'] // 20)
        
        print(f"✅ {game['title']}")
        print(f"   📁 {game['file']} ({game['file_size']:,} bytes)")
        print(f"   🎯 Category: {game['category'].title()}")
        print(f"   📊 Complexity: {complexity_bar} ({game['complexity_score']}/100)")
        print(f"   ⏱️  Est. Playtime: {game['estimated_playtime']}")
        print(f"   📝 {game['description']}")
        
        if game['classes']:
            print(f"   🏗️  Classes: {', '.join(game['classes'])}")
        
        if game['game_features']:
            features = [f.replace('_', ' ').title() for f in game['game_features']]
            print(f"   ⚡ Features: {', '.join(features)}")
        
        if game['recommendations']:
            print(f"   💡 Suggestions: {'; '.join(game['recommendations'])}")
        
        print()
    
    def _print_game_summary(self, game: Dict, show_issues: bool = False):
        """Print brief game summary"""
        status_icon = {"FULL": "✅", "PLACEHOLDER": "🔧", "BROKEN": "❌", "PARTIAL": "⚠️"}
        icon = status_icon.get(game['status'], "❓")
        
        print(f"{icon} {game['title']} ({game['file']})")
        print(f"   📊 {game['file_size']:,} bytes, {game['line_count']} lines")
        
        if show_issues and game['issues']:
            for issue in game['issues']:
                print(f"   ❌ {issue}")
        
        print()

def main():
    """Main testing function"""
    tester = GameTester()
    full_games, placeholder_games, broken_games = tester.test_all_games()
    
    # Return appropriate exit code
    if broken_games:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
