"""
GameVerse Hub 2.0 - Auto Game Discovery System
Automatically scans and detects games without manual configuration
"""

import os
import json
import ast
import importlib.util
from typing import Dict, List, Optional
from pathlib import Path

class GameDiscovery:
    """Automatically discover and analyze games in the games folder"""
    
    def __init__(self, games_folder: str = "games"):
        self.games_folder = Path(games_folder)
        self.discovered_games = []
        
    def scan_games_folder(self) -> List[Dict]:
        """Scan games folder and auto-detect game files"""
        discovered = []
        
        if not self.games_folder.exists():
            return discovered
            
        for game_file in self.games_folder.glob("*.py"):
            if game_file.name.startswith("__"):
                continue
                
            game_info = self._analyze_game_file(game_file)
            if game_info:
                discovered.append(game_info)
                
        self.discovered_games = discovered
        return discovered
    
    def _analyze_game_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze a Python file to extract game metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse the AST to find game metadata
            tree = ast.parse(content)
            
            game_info = {
                "id": file_path.stem,
                "title": self._extract_title(content, file_path.stem),
                "file": file_path.name,
                "description": self._extract_description(content),
                "category": self._detect_category(content),
                "difficulty": "medium",  # Default
                "estimated_playtime": "10-20 min",  # Default
                "multiplayer": self._detect_multiplayer(content),
                "requirements": self._extract_requirements(content),
                "version": "1.0.0",  # Default
                "author": "Unknown",
                "tags": self._generate_tags(content),
                "thumbnail": f"assets/thumbnails/{file_path.stem}.png",
                "achievements": [],
                "leaderboard": False,
                "last_played": None,
                "playtime": 0,
                "high_score": 0,
                "completion_rate": 0.0
            }
            
            return game_info
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract game title from comments or variables"""
        lines = content.split('\n')
        
        # Look for title in comments
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line.startswith('#') and ('title' in line.lower() or 'name' in line.lower()):
                # Extract title after colon or dash
                if ':' in line:
                    return line.split(':', 1)[1].strip()
                elif '-' in line:
                    return line.split('-', 1)[1].strip()
        
        # Look for TITLE or GAME_NAME variables
        if 'TITLE' in content:
            try:
                start = content.find('TITLE') 
                line = content[start:start+100].split('\n')[0]
                if '=' in line:
                    title = line.split('=', 1)[1].strip().strip('"\'')
                    return title
            except:
                pass
        
        # Default to formatted filename
        return filename.replace('_', ' ').title()
    
    def _extract_description(self, content: str) -> str:
        """Extract game description from docstrings or comments"""
        lines = content.split('\n')
        
        # Look for module docstring
        in_docstring = False
        docstring_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('"""') or line.startswith("'''"):
                if in_docstring:
                    break
                in_docstring = True
                # Get text after opening quotes
                desc = line[3:].strip()
                if desc and not desc.endswith('"""') and not desc.endswith("'''"):
                    docstring_lines.append(desc)
                continue
            elif in_docstring:
                if line.endswith('"""') or line.endswith("'''"):
                    desc = line[:-3].strip()
                    if desc:
                        docstring_lines.append(desc)
                    break
                docstring_lines.append(line)
        
        if docstring_lines:
            return ' '.join(docstring_lines)
        
        # Look for description in comments
        for line in lines[:30]:
            line = line.strip()
            if line.startswith('#') and ('description' in line.lower() or 'about' in line.lower()):
                if ':' in line:
                    return line.split(':', 1)[1].strip()
        
        return "A Python game"
    
    def _detect_category(self, content: str) -> str:
        """Detect game category based on code patterns"""
        content_lower = content.lower()
        
        # Keyword-based detection
        if any(word in content_lower for word in ['platform', 'jump', 'gravity']):
            return "platformer"
        elif any(word in content_lower for word in ['shoot', 'bullet', 'enemy', 'alien']):
            return "shooter"
        elif any(word in content_lower for word in ['puzzle', 'solve', 'brain', 'logic']):
            return "puzzle"
        elif any(word in content_lower for word in ['race', 'car', 'speed', 'lap']):
            return "racing"
        elif any(word in content_lower for word in ['break', 'brick', 'ball', 'paddle']):
            return "arcade"
        elif any(word in content_lower for word in ['click', 'increment', 'upgrade']):
            return "clicker"
        elif any(word in content_lower for word in ['quiz', 'question', 'answer']):
            return "quiz"
        elif any(word in content_lower for word in ['board', 'chess', 'checkers']):
            return "board"
        elif any(word in content_lower for word in ['type', 'typing', 'keyboard']):
            return "typing"
        elif any(word in content_lower for word in ['build', 'city', 'simulation']):
            return "simulation"
        
        return "arcade"  # Default category
    
    def _detect_multiplayer(self, content: str) -> bool:
        """Detect if game supports multiplayer"""
        multiplayer_keywords = ['multiplayer', 'player2', 'network', 'socket', 'client', 'server']
        return any(keyword in content.lower() for keyword in multiplayer_keywords)
    
    def _extract_requirements(self, content: str) -> List[str]:
        """Extract required packages from imports"""
        requirements = set(['pygame'])  # Default requirement
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                # Extract package names
                if 'import' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        package = parts[1].split('.')[0]
                        if package not in ['os', 'sys', 'random', 'math', 'time']:
                            requirements.add(package)
        
        return list(requirements)
    
    def _generate_tags(self, content: str) -> List[str]:
        """Generate tags based on code analysis"""
        tags = []
        content_lower = content.lower()
        
        # Visual style tags
        if 'retro' in content_lower or 'pixel' in content_lower:
            tags.append('retro')
        if 'neon' in content_lower or 'glow' in content_lower:
            tags.append('neon')
        
        # Gameplay tags
        if 'action' in content_lower or 'fast' in content_lower:
            tags.append('action')
        if 'casual' in content_lower or 'relax' in content_lower:
            tags.append('casual')
        if 'hard' in content_lower or 'difficult' in content_lower:
            tags.append('challenging')
        
        # Technical tags
        if 'pygame' in content_lower:
            tags.append('pygame')
        if 'class' in content_lower:
            tags.append('oop')
        
        return tags[:5]  # Limit to 5 tags
    
    def merge_with_config(self, config_path: str = "games_config.json") -> Dict:
        """Merge discovered games with existing configuration"""
        # Load existing config
        existing_config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                existing_config = json.load(f)
        
        # Create games lookup by filename (for backward compatibility)
        existing_games = {}
        for game in existing_config.get('games', []):
            # Use filename as key for lookup
            filename = game.get('file', '')
            if filename:
                existing_games[filename] = game
        
        # Merge discovered games with existing data
        merged_games = []
        for discovered in self.discovered_games:
            filename = discovered['file']
            if filename in existing_games:
                # Update existing game with discovered metadata
                existing = existing_games[filename].copy()
                # Add ID if missing
                if 'id' not in existing:
                    existing['id'] = discovered['id']
                # Update with discovered data, but preserve user data
                existing.update({k: v for k, v in discovered.items() 
                               if k not in ['playtime', 'high_score', 'last_played', 'completion_rate']})
                merged_games.append(existing)
            else:
                # Add new discovered game
                merged_games.append(discovered)
        
        # Create final config
        final_config = existing_config.copy()
        final_config['games'] = merged_games
        
        # Add default hub settings if not present
        if 'hub_settings' not in final_config:
            final_config['hub_settings'] = {
                "theme": "retro",
                "layout": "grid", 
                "auto_update": True,
                "analytics": False,
                "cloud_sync": False,
                "parental_controls": False
            }
        
        return final_config
    
    def save_updated_config(self, config_path: str = "games_config.json"):
        """Save the merged configuration to file"""
        config = self.merge_with_config(config_path)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Updated configuration saved to {config_path}")
        print(f"Discovered {len(self.discovered_games)} games")

# Example usage
if __name__ == "__main__":
    discovery = GameDiscovery()
    games = discovery.scan_games_folder()
    
    print(f"Discovered {len(games)} games:")
    for game in games:
        print(f"- {game['title']} ({game['category']})")
    
    discovery.save_updated_config()
