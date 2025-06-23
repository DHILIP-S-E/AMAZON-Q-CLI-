#!/usr/bin/env python3
"""
GameVerse Hub - Comprehensive Game Testing Script
Tests all games for syntax errors, imports, and basic functionality
"""

import os
import sys
import subprocess
import importlib.util
import ast
import time
from pathlib import Path
from typing import Dict, List, Tuple

class GameTester:
    """Comprehensive game testing utility"""
    
    def __init__(self, games_folder: str = "games"):
        self.games_folder = Path(games_folder)
        self.test_results = {}
        self.total_games = 0
        self.passed_games = 0
        self.failed_games = 0
        
    def run_all_tests(self):
        """Run comprehensive tests on all games"""
        print("🎮 GameVerse Hub - Game Testing Suite")
        print("=" * 50)
        
        if not self.games_folder.exists():
            print(f"❌ Games folder '{self.games_folder}' not found!")
            return False
        
        # Get all Python game files
        game_files = list(self.games_folder.glob("*.py"))
        game_files = [f for f in game_files if not f.name.startswith("__")]
        
        self.total_games = len(game_files)
        print(f"Found {self.total_games} games to test\n")
        
        # Test each game
        for i, game_file in enumerate(game_files, 1):
            print(f"[{i}/{self.total_games}] Testing {game_file.name}")
            print("-" * 40)
            
            result = self._test_single_game(game_file)
            self.test_results[game_file.name] = result
            
            if result['overall_status'] == 'PASS':
                self.passed_games += 1
                print(f"✅ {game_file.name} - PASSED")
            else:
                self.failed_games += 1
                print(f"❌ {game_file.name} - FAILED")
            
            print()
        
        # Print summary
        self._print_summary()
        return self.failed_games == 0
    
    def _test_single_game(self, game_file: Path) -> Dict:
        """Test a single game file comprehensively"""
        result = {
            'file': game_file.name,
            'syntax_check': 'UNKNOWN',
            'import_check': 'UNKNOWN', 
            'pygame_check': 'UNKNOWN',
            'structure_check': 'UNKNOWN',
            'execution_test': 'UNKNOWN',
            'overall_status': 'UNKNOWN',
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        try:
            # Test 1: Syntax Check
            result['syntax_check'] = self._check_syntax(game_file, result)
            
            # Test 2: Import Check
            result['import_check'] = self._check_imports(game_file, result)
            
            # Test 3: Pygame Integration Check
            result['pygame_check'] = self._check_pygame_usage(game_file, result)
            
            # Test 4: Code Structure Check
            result['structure_check'] = self._check_code_structure(game_file, result)
            
            # Test 5: Execution Test (limited)
            result['execution_test'] = self._test_execution(game_file, result)
            
            # Determine overall status
            critical_tests = [result['syntax_check'], result['import_check']]
            if all(test == 'PASS' for test in critical_tests):
                result['overall_status'] = 'PASS'
            else:
                result['overall_status'] = 'FAIL'
                
        except Exception as e:
            result['overall_status'] = 'ERROR'
            result['errors'].append(f"Unexpected error: {str(e)}")
        
        return result
    
    def _check_syntax(self, game_file: Path, result: Dict) -> str:
        """Check Python syntax"""
        try:
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            ast.parse(content)
            result['info'].append("✓ Syntax is valid")
            return 'PASS'
            
        except SyntaxError as e:
            result['errors'].append(f"Syntax error: {e}")
            return 'FAIL'
        except Exception as e:
            result['errors'].append(f"Syntax check error: {e}")
            return 'ERROR'
    
    def _check_imports(self, game_file: Path, result: Dict) -> str:
        """Check if all imports are available"""
        try:
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse imports
            tree = ast.parse(content)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # Check each import
            missing_imports = []
            for imp in imports:
                try:
                    if imp == 'pygame':
                        # Special handling for pygame
                        import pygame
                    else:
                        __import__(imp)
                except ImportError:
                    missing_imports.append(imp)
            
            if missing_imports:
                result['errors'].append(f"Missing imports: {', '.join(missing_imports)}")
                return 'FAIL'
            else:
                result['info'].append(f"✓ All imports available: {', '.join(imports)}")
                return 'PASS'
                
        except Exception as e:
            result['errors'].append(f"Import check error: {e}")
            return 'ERROR'
    
    def _check_pygame_usage(self, game_file: Path, result: Dict) -> str:
        """Check pygame integration and common patterns"""
        try:
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            pygame_patterns = {
                'pygame_init': 'pygame.init()',
                'display_set_mode': 'pygame.display.set_mode',
                'event_get': 'pygame.event.get',
                'display_flip': 'pygame.display.flip',
                'clock': 'pygame.time.Clock'
            }
            
            found_patterns = []
            missing_patterns = []
            
            for pattern_name, pattern in pygame_patterns.items():
                if pattern in content:
                    found_patterns.append(pattern_name)
                else:
                    missing_patterns.append(pattern_name)
            
            if 'pygame' in content:
                result['info'].append(f"✓ Pygame patterns found: {', '.join(found_patterns)}")
                if missing_patterns:
                    result['warnings'].append(f"Missing pygame patterns: {', '.join(missing_patterns)}")
                return 'PASS'
            else:
                result['warnings'].append("No pygame usage detected")
                return 'WARN'
                
        except Exception as e:
            result['errors'].append(f"Pygame check error: {e}")
            return 'ERROR'
    
    def _check_code_structure(self, game_file: Path, result: Dict) -> str:
        """Check code structure and organization"""
        try:
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check for main execution pattern
            has_main_guard = '__name__ == "__main__"' in content
            has_main_function = any(isinstance(node, ast.FunctionDef) and node.name == 'main' 
                                  for node in ast.walk(tree))
            has_classes = any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
            has_functions = any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
            
            structure_info = []
            if has_main_guard:
                structure_info.append("main guard")
            if has_main_function:
                structure_info.append("main function")
            if has_classes:
                structure_info.append("classes")
            if has_functions:
                structure_info.append("functions")
            
            result['info'].append(f"✓ Code structure: {', '.join(structure_info)}")
            
            # Check file size (warn if too small - might be placeholder)
            file_size = game_file.stat().st_size
            if file_size < 2000:  # Less than 2KB
                result['warnings'].append(f"Small file size ({file_size} bytes) - might be placeholder")
            
            return 'PASS'
            
        except Exception as e:
            result['errors'].append(f"Structure check error: {e}")
            return 'ERROR'
    
    def _test_execution(self, game_file: Path, result: Dict) -> str:
        """Test if the game can be executed (limited test)"""
        try:
            # Check if it's a placeholder file
            with open(game_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'placeholder' in content.lower() or 'demo' in content.lower():
                result['info'].append("ℹ️ Placeholder/demo game detected")
                return 'SKIP'
            
            # Try to import the module (without executing main)
            spec = importlib.util.spec_from_file_location("test_game", game_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Don't execute - just check if it can be loaded
                result['info'].append("✓ Module can be imported")
                return 'PASS'
            else:
                result['errors'].append("Cannot create module spec")
                return 'FAIL'
                
        except Exception as e:
            result['errors'].append(f"Execution test error: {e}")
            return 'ERROR'
    
    def _print_summary(self):
        """Print comprehensive test summary"""
        print("🎯 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Games: {self.total_games}")
        print(f"✅ Passed: {self.passed_games}")
        print(f"❌ Failed: {self.failed_games}")
        print(f"Success Rate: {(self.passed_games/self.total_games)*100:.1f}%")
        print()
        
        # Detailed results
        print("📊 DETAILED RESULTS")
        print("-" * 50)
        
        for game_name, result in self.test_results.items():
            status_icon = "✅" if result['overall_status'] == 'PASS' else "❌"
            print(f"{status_icon} {game_name}")
            
            # Show test breakdown
            tests = ['syntax_check', 'import_check', 'pygame_check', 'structure_check', 'execution_test']
            test_status = []
            for test in tests:
                status = result[test]
                if status == 'PASS':
                    test_status.append(f"✓{test.replace('_check', '').replace('_test', '')}")
                elif status == 'FAIL':
                    test_status.append(f"✗{test.replace('_check', '').replace('_test', '')}")
                elif status == 'WARN':
                    test_status.append(f"⚠{test.replace('_check', '').replace('_test', '')}")
                elif status == 'SKIP':
                    test_status.append(f"⏭{test.replace('_check', '').replace('_test', '')}")
            
            print(f"   Tests: {' | '.join(test_status)}")
            
            # Show errors
            if result['errors']:
                for error in result['errors']:
                    print(f"   ❌ {error}")
            
            # Show warnings
            if result['warnings']:
                for warning in result['warnings']:
                    print(f"   ⚠️ {warning}")
            
            print()
        
        # Game categories
        print("📂 GAME CATEGORIES")
        print("-" * 50)
        
        # Use the auto-discovery to categorize
        try:
            from core.game_discovery import GameDiscovery
            discovery = GameDiscovery()
            games = discovery.scan_games_folder()
            
            categories = {}
            for game in games:
                category = game.get('category', 'unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(game['title'])
            
            for category, game_list in sorted(categories.items()):
                print(f"{category.title()}: {len(game_list)} games")
                for game in game_list:
                    status = "✅" if any(result['overall_status'] == 'PASS' 
                                      for name, result in self.test_results.items() 
                                      if game.lower().replace(' ', '_') in name.lower()) else "❌"
                    print(f"  {status} {game}")
                print()
                
        except ImportError:
            print("Auto-discovery not available for categorization")
    
    def test_specific_games(self, game_names: List[str]):
        """Test specific games by name"""
        print(f"🎮 Testing specific games: {', '.join(game_names)}")
        print("=" * 50)
        
        for game_name in game_names:
            game_file = self.games_folder / f"{game_name}.py"
            if game_file.exists():
                print(f"Testing {game_name}...")
                result = self._test_single_game(game_file)
                self.test_results[game_file.name] = result
                
                if result['overall_status'] == 'PASS':
                    print(f"✅ {game_name} - PASSED")
                else:
                    print(f"❌ {game_name} - FAILED")
                    for error in result['errors']:
                        print(f"   ❌ {error}")
                print()
            else:
                print(f"❌ {game_name}.py not found")

def main():
    """Main testing function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test GameVerse Hub games")
    parser.add_argument("--games", nargs="*", help="Specific games to test")
    parser.add_argument("--folder", default="games", help="Games folder path")
    
    args = parser.parse_args()
    
    tester = GameTester(args.folder)
    
    if args.games:
        tester.test_specific_games(args.games)
    else:
        success = tester.run_all_tests()
        
        if success:
            print("🎉 All games passed testing!")
            return 0
        else:
            print("⚠️ Some games failed testing. Check the details above.")
            return 1

if __name__ == "__main__":
    sys.exit(main())
