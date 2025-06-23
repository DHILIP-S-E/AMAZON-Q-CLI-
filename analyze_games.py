#!/usr/bin/env python3
"""
GameVerse Hub - Game Analysis Script
Analyzes all games without requiring pygame installation
"""

import ast
import os
from pathlib import Path
from typing import Dict, List

class GameAnalyzer:
    """Analyze games without executing them"""
    
    def __init__(self, games_folder: str = "games"):
        self.games_folder = Path(games_folder)
        
    def analyze_all_games(self):
        """Analyze all games in the folder"""
        print("🎮 GameVerse Hub - Game Analysis Report")
        print("=" * 60)
        
        game_files = list(self.games_folder.glob("*.py"))
        game_files = [f for f in game_files if not f.name.startswith("__")]
        
        print(f"Found {len(game_files)} games to analyze\n")
        
        # Categorize games
        full_games = []
        placeholder_games = []
        
        for game_file in sorted(game_files):
            analysis = self._analyze_game(game_file)
            
            if analysis['is_placeholder']:
                placeholder_games.append(analysis)
            else:
                full_games.append(analysis)
        
        # Print results
        print("🎯 FULL GAMES (Ready to Play)")
        print("-" * 40)
        for game in full_games:
            self._print_game_analysis(game)
        
        print(f"\n🔧 PLACEHOLDER GAMES ({len(placeholder_games)} games)")
        print("-" * 40)
        for game in placeholder_games:
            self._print_game_analysis(game, brief=True)
        
        print(f"\n📊 SUMMARY")
        print("-" * 40)
        print(f"Total Games: {len(game_files)}")
        print(f"✅ Full Games: {len(full_games)}")
        print(f"🔧 Placeholder Games: {len(placeholder_games)}")
        print(f"Completion Rate: {(len(full_games)/len(game_files))*100:.1f}%")
        
        return full_games, placeholder_games
    
    def _analyze_game(self, game_file: Path) -> Dict:
        """Analyze a single game file"""
        analysis = {
            'name': game_file.stem,
            'file': game_file.name,
            'title': '',
            'description': '',
            'category': 'unknown',
            'file_size': game_file.stat().st_size,
            'line_count': 0,
            'is_placeholder': False,
            'has_classes': False,
            'has_main_loop': False,
            'has_pygame_init': False,
            'has_event_handling': False,
            'complexity_score': 0,
            'features': [],
            'issues': []
        }
        
        try:
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis['line_count'] = len(content.split('\n'))
            
            # Check if it's a placeholder
            if ('placeholder' in content.lower() or 
                'demo' in content.lower() or 
                analysis['file_size'] < 2000):
                analysis['is_placeholder'] = True
            
            # Parse AST
            tree = ast.parse(content)
            
            # Extract title and description
            analysis['title'] = self._extract_title(content, game_file.stem)
            analysis['description'] = self._extract_description(content)
            analysis['category'] = self._detect_category(content)
            
            # Analyze code structure
            self._analyze_structure(tree, content, analysis)
            
            # Calculate complexity score
            analysis['complexity_score'] = self._calculate_complexity(analysis)
            
        except Exception as e:
            analysis['issues'].append(f"Analysis error: {str(e)}")
        
        return analysis
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract game title"""
        lines = content.split('\n')
        
        # Look for title in comments
        for line in lines[:20]:
            line = line.strip()
            if line.startswith('#') and any(word in line.lower() for word in ['title', 'name', 'game']):
                if ':' in line or '-' in line:
                    title = line.split(':', 1)[-1].split('-', 1)[-1].strip()
                    if title and len(title) > 3:
                        return title
        
        # Look for docstring
        if '"""' in content:
            try:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    docstring = content[start:end].strip()
                    first_line = docstring.split('\n')[0].strip()
                    if first_line and len(first_line) > 3:
                        return first_line
            except:
                pass
        
        # Default to formatted filename
        return filename.replace('_', ' ').title()
    
    def _extract_description(self, content: str) -> str:
        """Extract game description"""
        lines = content.split('\n')
        
        # Look for description in comments
        for line in lines[:30]:
            line = line.strip()
            if line.startswith('#') and 'description' in line.lower():
                if ':' in line:
                    return line.split(':', 1)[1].strip()
        
        # Look for docstring
        if '"""' in content:
            try:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    docstring = content[start:end].strip()
                    lines = docstring.split('\n')
                    if len(lines) > 1:
                        return ' '.join(lines[1:]).strip()
                    return lines[0].strip()
            except:
                pass
        
        return "A Python game"
    
    def _detect_category(self, content: str) -> str:
        """Detect game category"""
        content_lower = content.lower()
        
        categories = {
            'platformer': ['platform', 'jump', 'gravity', 'player', 'ground'],
            'shooter': ['shoot', 'bullet', 'enemy', 'alien', 'laser', 'weapon'],
            'puzzle': ['puzzle', 'solve', 'brain', 'logic', 'number', 'maze'],
            'racing': ['race', 'car', 'speed', 'lap', 'track', 'vehicle'],
            'arcade': ['break', 'brick', 'ball', 'paddle', 'score', 'level'],
            'clicker': ['click', 'increment', 'upgrade', 'idle', 'cookie'],
            'quiz': ['quiz', 'question', 'answer', 'trivia'],
            'board': ['board', 'chess', 'checkers', 'turn'],
            'typing': ['type', 'typing', 'keyboard', 'word', 'text'],
            'simulation': ['build', 'city', 'simulation', 'sim', 'manage']
        }
        
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return 'arcade'
    
    def _analyze_structure(self, tree: ast.AST, content: str, analysis: Dict):
        """Analyze code structure"""
        # Check for classes
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        analysis['has_classes'] = len(classes) > 0
        if classes:
            analysis['features'].append(f"{len(classes)} classes")
        
        # Check for functions
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if functions:
            analysis['features'].append(f"{len(functions)} functions")
        
        # Check pygame patterns
        pygame_patterns = {
            'pygame_init': 'pygame.init()',
            'display_mode': 'pygame.display.set_mode',
            'event_loop': 'pygame.event.get',
            'game_loop': 'while',
            'clock': 'pygame.time.Clock',
            'sprites': 'pygame.sprite',
            'surfaces': 'pygame.Surface'
        }
        
        found_patterns = []
        for pattern_name, pattern in pygame_patterns.items():
            if pattern in content:
                found_patterns.append(pattern_name)
        
        analysis['has_pygame_init'] = 'pygame_init' in found_patterns
        analysis['has_main_loop'] = 'game_loop' in found_patterns
        analysis['has_event_handling'] = 'event_loop' in found_patterns
        
        if found_patterns:
            analysis['features'].extend(found_patterns)
        
        # Check for specific game features
        game_features = {
            'collision_detection': ['collide', 'collision', 'rect'],
            'animation': ['animation', 'frame', 'animate'],
            'sound': ['sound', 'music', 'audio'],
            'high_scores': ['score', 'high_score', 'best'],
            'levels': ['level', 'stage'],
            'power_ups': ['power', 'upgrade', 'bonus'],
            'ai_enemies': ['ai', 'enemy', 'bot'],
            'multiplayer': ['player2', 'multiplayer', 'network']
        }
        
        for feature_name, keywords in game_features.items():
            if any(keyword in content.lower() for keyword in keywords):
                analysis['features'].append(feature_name)
    
    def _calculate_complexity(self, analysis: Dict) -> int:
        """Calculate complexity score (0-100)"""
        score = 0
        
        # File size contribution (0-20 points)
        size_score = min(20, analysis['file_size'] // 500)
        score += size_score
        
        # Line count contribution (0-20 points)
        line_score = min(20, analysis['line_count'] // 50)
        score += line_score
        
        # Structure contribution (0-30 points)
        if analysis['has_classes']:
            score += 10
        if analysis['has_main_loop']:
            score += 10
        if analysis['has_event_handling']:
            score += 10
        
        # Features contribution (0-30 points)
        feature_score = min(30, len(analysis['features']) * 3)
        score += feature_score
        
        return min(100, score)
    
    def _print_game_analysis(self, analysis: Dict, brief: bool = False):
        """Print game analysis results"""
        status = "🔧" if analysis['is_placeholder'] else "✅"
        complexity = "●" * (analysis['complexity_score'] // 20)
        
        print(f"{status} {analysis['title']}")
        print(f"   File: {analysis['file']} ({analysis['file_size']} bytes, {analysis['line_count']} lines)")
        print(f"   Category: {analysis['category'].title()}")
        print(f"   Complexity: {complexity} ({analysis['complexity_score']}/100)")
        
        if not brief:
            print(f"   Description: {analysis['description']}")
            if analysis['features']:
                print(f"   Features: {', '.join(analysis['features'])}")
            if analysis['issues']:
                for issue in analysis['issues']:
                    print(f"   ⚠️ {issue}")
        
        print()

def main():
    """Main analysis function"""
    analyzer = GameAnalyzer()
    full_games, placeholder_games = analyzer.analyze_all_games()
    
    # Create a quick reference
    print("\n🎮 QUICK REFERENCE - PLAYABLE GAMES")
    print("-" * 60)
    for game in full_games:
        print(f"python3 games/{game['file']} - {game['title']} ({game['category']})")

if __name__ == "__main__":
    main()
