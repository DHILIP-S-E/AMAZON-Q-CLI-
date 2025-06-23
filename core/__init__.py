# GameVerse Hub 2.0 Core Module
"""
Core functionality for the enhanced GameVerse Hub
"""

__version__ = "2.0.0"
__author__ = "GameVerse Development Team"

from .game_discovery import GameDiscovery
from .profile_manager import ProfileManager
from .ui_manager import UIManager

__all__ = [
    'GameDiscovery', 
    'ProfileManager',
    'UIManager'
]
