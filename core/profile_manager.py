"""
GameVerse Hub 2.0 - Profile & Statistics Manager
Handles user profiles, game statistics, achievements, and preferences
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

class ProfileManager:
    """Manage user profiles, statistics, and achievements"""
    
    def __init__(self, profile_name: str = "default"):
        self.profile_name = profile_name
        self.data_dir = Path("data/profiles")
        self.profile_file = self.data_dir / f"{profile_name}.json"
        self.stats_file = self.data_dir / f"{profile_name}_stats.json"
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create profile
        self.profile_data = self._load_profile()
        self.stats_data = self._load_stats()
    
    def _load_profile(self) -> Dict:
        """Load user profile data"""
        if self.profile_file.exists():
            with open(self.profile_file, 'r') as f:
                return json.load(f)
        else:
            # Create default profile
            default_profile = {
                "name": self.profile_name,
                "created_date": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "preferences": {
                    "theme": "retro",
                    "layout": "grid",
                    "sound_enabled": True,
                    "music_enabled": True,
                    "volume": 0.7,
                    "auto_save": True,
                    "show_fps": False,
                    "difficulty_preference": "medium"
                },
                "achievements": {},
                "favorites": [],
                "blocked_games": [],
                "parental_settings": {
                    "enabled": False,
                    "time_limit_minutes": 0,
                    "allowed_categories": []
                }
            }
            self._save_profile(default_profile)
            return default_profile
    
    def _load_stats(self) -> Dict:
        """Load user statistics data"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        else:
            # Create default stats
            default_stats = {
                "total_playtime": 0,
                "games_played": 0,
                "favorite_category": "arcade",
                "achievement_count": 0,
                "high_scores": {},
                "game_stats": {},
                "daily_stats": {},
                "weekly_stats": {},
                "monthly_stats": {}
            }
            self._save_stats(default_stats)
            return default_stats
    
    def _save_profile(self, data: Dict = None):
        """Save profile data to file"""
        if data is None:
            data = self.profile_data
        
        data["last_active"] = datetime.now().isoformat()
        
        with open(self.profile_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_stats(self, data: Dict = None):
        """Save statistics data to file"""
        if data is None:
            data = self.stats_data
            
        with open(self.stats_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Profile Management
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference value"""
        return self.profile_data.get("preferences", {}).get(key, default)
    
    def set_preference(self, key: str, value: Any):
        """Set user preference value"""
        if "preferences" not in self.profile_data:
            self.profile_data["preferences"] = {}
        
        self.profile_data["preferences"][key] = value
        self._save_profile()
    
    def add_favorite(self, game_id: str):
        """Add game to favorites"""
        if game_id not in self.profile_data["favorites"]:
            self.profile_data["favorites"].append(game_id)
            self._save_profile()
    
    def remove_favorite(self, game_id: str):
        """Remove game from favorites"""
        if game_id in self.profile_data["favorites"]:
            self.profile_data["favorites"].remove(game_id)
            self._save_profile()
    
    def is_favorite(self, game_id: str) -> bool:
        """Check if game is in favorites"""
        return game_id in self.profile_data.get("favorites", [])
    
    # Statistics Tracking
    def record_game_session(self, game_id: str, duration_seconds: int, score: int = 0):
        """Record a game session"""
        # Update total stats
        self.stats_data["total_playtime"] += duration_seconds
        self.stats_data["games_played"] += 1
        
        # Update game-specific stats
        if game_id not in self.stats_data["game_stats"]:
            self.stats_data["game_stats"][game_id] = {
                "playtime": 0,
                "sessions": 0,
                "high_score": 0,
                "average_score": 0,
                "last_played": None,
                "completion_rate": 0.0
            }
        
        game_stats = self.stats_data["game_stats"][game_id]
        game_stats["playtime"] += duration_seconds
        game_stats["sessions"] += 1
        game_stats["last_played"] = datetime.now().isoformat()
        
        # Update high score
        if score > game_stats["high_score"]:
            game_stats["high_score"] = score
            self.stats_data["high_scores"][game_id] = score
        
        # Update average score
        if score > 0:
            current_avg = game_stats.get("average_score", 0)
            sessions = game_stats["sessions"]
            game_stats["average_score"] = ((current_avg * (sessions - 1)) + score) / sessions
        
        # Update daily/weekly/monthly stats
        self._update_time_based_stats(game_id, duration_seconds, score)
        
        self._save_stats()
    
    def _update_time_based_stats(self, game_id: str, duration: int, score: int):
        """Update daily, weekly, and monthly statistics"""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        this_week = now.strftime("%Y-W%U")
        this_month = now.strftime("%Y-%m")
        
        # Daily stats
        if today not in self.stats_data["daily_stats"]:
            self.stats_data["daily_stats"][today] = {"playtime": 0, "games": [], "scores": {}}
        
        daily = self.stats_data["daily_stats"][today]
        daily["playtime"] += duration
        if game_id not in daily["games"]:
            daily["games"].append(game_id)
        if game_id not in daily["scores"]:
            daily["scores"][game_id] = []
        daily["scores"][game_id].append(score)
        
        # Weekly stats
        if this_week not in self.stats_data["weekly_stats"]:
            self.stats_data["weekly_stats"][this_week] = {"playtime": 0, "games": set(), "sessions": 0}
        
        weekly = self.stats_data["weekly_stats"][this_week]
        weekly["playtime"] += duration
        weekly["games"] = list(set(weekly.get("games", [])) | {game_id})
        weekly["sessions"] = weekly.get("sessions", 0) + 1
        
        # Monthly stats
        if this_month not in self.stats_data["monthly_stats"]:
            self.stats_data["monthly_stats"][this_month] = {"playtime": 0, "games": set(), "sessions": 0}
        
        monthly = self.stats_data["monthly_stats"][this_month]
        monthly["playtime"] += duration
        monthly["games"] = list(set(monthly.get("games", [])) | {game_id})
        monthly["sessions"] = monthly.get("sessions", 0) + 1
    
    def get_game_stats(self, game_id: str) -> Dict:
        """Get statistics for a specific game"""
        return self.stats_data.get("game_stats", {}).get(game_id, {
            "playtime": 0,
            "sessions": 0,
            "high_score": 0,
            "average_score": 0,
            "last_played": None,
            "completion_rate": 0.0
        })
    
    def get_top_games(self, limit: int = 5, sort_by: str = "playtime") -> List[Dict]:
        """Get top games by playtime or sessions"""
        game_stats = self.stats_data.get("game_stats", {})
        
        # Sort games by specified criteria
        sorted_games = sorted(
            game_stats.items(),
            key=lambda x: x[1].get(sort_by, 0),
            reverse=True
        )
        
        return [{"game_id": game_id, **stats} for game_id, stats in sorted_games[:limit]]
    
    def get_daily_playtime(self, days: int = 7) -> Dict[str, int]:
        """Get playtime for the last N days"""
        daily_stats = {}
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            playtime = self.stats_data.get("daily_stats", {}).get(date, {}).get("playtime", 0)
            daily_stats[date] = playtime
        
        return daily_stats
    
    # Achievement System
    def unlock_achievement(self, achievement_id: str, game_id: str = None, description: str = ""):
        """Unlock an achievement"""
        if achievement_id not in self.profile_data["achievements"]:
            self.profile_data["achievements"][achievement_id] = {
                "unlocked_date": datetime.now().isoformat(),
                "game_id": game_id,
                "description": description
            }
            self.stats_data["achievement_count"] += 1
            self._save_profile()
            self._save_stats()
            return True
        return False
    
    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked"""
        return achievement_id in self.profile_data.get("achievements", {})
    
    def get_achievements(self, game_id: str = None) -> Dict:
        """Get achievements, optionally filtered by game"""
        achievements = self.profile_data.get("achievements", {})
        
        if game_id:
            return {k: v for k, v in achievements.items() if v.get("game_id") == game_id}
        
        return achievements
    
    # Recommendations
    def get_recommended_games(self, all_games: List[Dict], limit: int = 3) -> List[Dict]:
        """Get game recommendations based on play history"""
        if not self.stats_data.get("game_stats"):
            # No play history, recommend popular categories
            return all_games[:limit]
        
        # Analyze play patterns
        played_categories = {}
        for game_id, stats in self.stats_data["game_stats"].items():
            # Find game category from all_games
            game_info = next((g for g in all_games if g["id"] == game_id), None)
            if game_info:
                category = game_info.get("category", "arcade")
                played_categories[category] = played_categories.get(category, 0) + stats["playtime"]
        
        # Find favorite category
        if played_categories:
            favorite_category = max(played_categories, key=played_categories.get)
            self.stats_data["favorite_category"] = favorite_category
            self._save_stats()
        else:
            favorite_category = "arcade"
        
        # Recommend unplayed games from favorite category
        played_game_ids = set(self.stats_data["game_stats"].keys())
        unplayed_games = [g for g in all_games if g["id"] not in played_game_ids]
        
        # Prioritize games from favorite category
        category_games = [g for g in unplayed_games if g.get("category") == favorite_category]
        other_games = [g for g in unplayed_games if g.get("category") != favorite_category]
        
        recommended = category_games[:limit]
        if len(recommended) < limit:
            recommended.extend(other_games[:limit - len(recommended)])
        
        return recommended[:limit]
    
    # Export/Import
    def export_profile(self, export_path: str):
        """Export profile data to file"""
        export_data = {
            "profile": self.profile_data,
            "stats": self.stats_data,
            "export_date": datetime.now().isoformat(),
            "version": "2.0.0"
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_profile(self, import_path: str):
        """Import profile data from file"""
        with open(import_path, 'r') as f:
            import_data = json.load(f)
        
        if "profile" in import_data:
            self.profile_data = import_data["profile"]
            self._save_profile()
        
        if "stats" in import_data:
            self.stats_data = import_data["stats"]
            self._save_stats()

# Example usage
if __name__ == "__main__":
    profile = ProfileManager("test_user")
    
    # Record some game sessions
    profile.record_game_session("super_pixel_runner", 300, 1500)  # 5 minutes, score 1500
    profile.record_game_session("retro_breakout", 600, 2300)      # 10 minutes, score 2300
    
    # Check stats
    print("Total playtime:", profile.stats_data["total_playtime"], "seconds")
    print("Games played:", profile.stats_data["games_played"])
    print("Top games:", profile.get_top_games(3))
    
    # Unlock achievement
    profile.unlock_achievement("first_game", "super_pixel_runner", "Played your first game!")
    print("Achievements:", len(profile.get_achievements()))
