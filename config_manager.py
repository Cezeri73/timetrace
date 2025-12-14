"""
Configuration Manager for TimeAudit Application
Handles JSON-based configuration and watchlist management
"""

import json
import os
from typing import List
import threading


class ConfigManager:
    """
    Manages application configuration stored in settings.json.
    Thread-safe configuration access and modification.
    """
    
    def __init__(self, config_path: str = "settings.json"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to JSON configuration file
        """
        self.config_path = config_path
        self.lock = threading.Lock()  # Thread-safe access
        self._init_config()
    
    def _init_config(self):
        """Create default configuration file if it doesn't exist."""
        if not os.path.exists(self.config_path):
            default_config = {
                "watchlist": [],
                "check_interval_seconds": 5,
                "save_interval_seconds": 60,
                "theme": "dark",
                "minimize_to_tray": True
            }
            self._save_config(default_config)
            print(f"[ConfigManager] Created default configuration: {self.config_path}")
        else:
            print(f"[ConfigManager] Loaded existing configuration: {self.config_path}")
    
    def _load_config(self) -> dict:
        """
        Load configuration from JSON file.
        
        Returns:
            Configuration dictionary
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[ConfigManager] Error loading config: {e}")
            # Return default config on error
            return {
                "watchlist": [],
                "check_interval_seconds": 5,
                "save_interval_seconds": 60,
                "theme": "dark",
                "minimize_to_tray": True
            }
    
    def _save_config(self, config: dict):
        """
        Save configuration to JSON file.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")
    
    def get_watchlist(self) -> List[str]:
        """
        Get list of applications to monitor.
        
        Returns:
            List of executable names (e.g., ["chrome.exe", "valorant.exe"])
        """
        with self.lock:
            config = self._load_config()
            return config.get("watchlist", [])
    
    def add_app(self, exe_name: str) -> bool:
        """
        Add an application to the watchlist.
        
        Args:
            exe_name: Executable name (e.g., "notepad.exe")
            
        Returns:
            True if added successfully, False if already exists
        """
        with self.lock:
            config = self._load_config()
            watchlist = config.get("watchlist", [])
            
            # Normalize the exe_name (lowercase for comparison)
            exe_name_lower = exe_name.lower().strip()
            
            # Check if already in watchlist (case-insensitive)
            if exe_name_lower in [app.lower() for app in watchlist]:
                print(f"[ConfigManager] {exe_name} already in watchlist")
                return False
            
            # Add to watchlist
            watchlist.append(exe_name_lower)
            config["watchlist"] = watchlist
            self._save_config(config)
            print(f"[ConfigManager] Added {exe_name_lower} to watchlist")
            return True
    
    def remove_app(self, exe_name: str) -> bool:
        """
        Remove an application from the watchlist.
        
        Args:
            exe_name: Executable name to remove
            
        Returns:
            True if removed successfully, False if not found
        """
        with self.lock:
            config = self._load_config()
            watchlist = config.get("watchlist", [])
            
            # Normalize the exe_name
            exe_name_lower = exe_name.lower().strip()
            
            # Remove from watchlist (case-insensitive)
            original_length = len(watchlist)
            watchlist = [app for app in watchlist if app.lower() != exe_name_lower]
            
            if len(watchlist) == original_length:
                print(f"[ConfigManager] {exe_name} not found in watchlist")
                return False
            
            config["watchlist"] = watchlist
            self._save_config(config)
            print(f"[ConfigManager] Removed {exe_name_lower} from watchlist")
            return True
    
    def get_setting(self, key: str, default=None):
        """
        Get a specific setting value.
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        with self.lock:
            config = self._load_config()
            return config.get(key, default)
    
    def set_setting(self, key: str, value):
        """
        Set a specific setting value.
        
        Args:
            key: Setting key
            value: Value to set
        """
        with self.lock:
            config = self._load_config()
            config[key] = value
            self._save_config(config)
            print(f"[ConfigManager] Updated setting {key} = {value}")
    
    def get_all_settings(self) -> dict:
        """
        Get all configuration settings.
        
        Returns:
            Complete configuration dictionary
        """
        with self.lock:
            return self._load_config()
    
    def clear_watchlist(self):
        """Remove all apps from watchlist."""
        with self.lock:
            config = self._load_config()
            config["watchlist"] = []
            self._save_config(config)
            print("[ConfigManager] Cleared watchlist")


# Testing the configuration manager
if __name__ == "__main__":
    # Create a test configuration
    config = ConfigManager("test_settings.json")
    
    # Test adding apps
    config.add_app("chrome.exe")
    config.add_app("valorant.exe")
    config.add_app("Chrome.exe")  # Should not add duplicate
    
    # Test getting watchlist
    watchlist = config.get_watchlist()
    print("Watchlist:", watchlist)
    
    # Test removing app
    config.remove_app("chrome.exe")
    watchlist = config.get_watchlist()
    print("Watchlist after removal:", watchlist)
    
    # Test settings
    config.set_setting("theme", "light")
    theme = config.get_setting("theme")
    print("Theme:", theme)
    
    # Clean up test file
    if os.path.exists("test_settings.json"):
        os.remove("test_settings.json")
        print("Test config cleaned up")
