"""
Monitor Service for TimeAudit Application
Background monitoring of application usage using psutil
"""

import psutil
import threading
import time
from datetime import datetime
from typing import Dict, Set
from database_manager import DatabaseManager
from config_manager import ConfigManager


class AppMonitor:
    """
    Monitors running processes and tracks usage time for watchlisted applications.
    Runs in a separate thread to avoid blocking the GUI.
    """
    
    def __init__(self, db_manager: DatabaseManager, config_manager: ConfigManager):
        """
        Initialize the application monitor.
        
        Args:
            db_manager: DatabaseManager instance for storing usage data
            config_manager: ConfigManager instance for getting watchlist
        """
        self.db_manager = db_manager
        self.config_manager = config_manager
        
        # Thread control
        self.is_running = False
        self.monitor_thread = None
        self.lock = threading.Lock()
        
        # Tracking data
        self.usage_counters: Dict[str, int] = {}  # app_name -> seconds accumulated
        self.last_save_time = time.time()
        
        # Configuration
        self.check_interval = config_manager.get_setting("check_interval_seconds", 5)
        self.save_interval = config_manager.get_setting("save_interval_seconds", 60)
        
        print("[AppMonitor] Monitor initialized")
    
    def start(self):
        """Start the monitoring thread."""
        with self.lock:
            if self.is_running:
                print("[AppMonitor] Monitor already running")
                return
            
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("[AppMonitor] Monitor started")
    
    def stop(self):
        """Stop the monitoring thread and save any pending data."""
        with self.lock:
            if not self.is_running:
                print("[AppMonitor] Monitor not running")
                return
            
            self.is_running = False
        
        # Wait for thread to finish
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=10)
        
        # Save any remaining data
        self._save_accumulated_time()
        print("[AppMonitor] Monitor stopped")
    
    def _monitor_loop(self):
        """
        Main monitoring loop. Runs in a separate thread.
        Checks running processes every check_interval seconds.
        """
        print("[AppMonitor] Monitor loop started")
        
        while self.is_running:
            try:
                # Get current watchlist
                watchlist = self.config_manager.get_watchlist()
                
                if watchlist:
                    # Check which watched apps are running
                    running_apps = self._get_running_watched_apps(watchlist)
                    
                    # Increment counters for running apps
                    with self.lock:
                        for app_name in running_apps:
                            if app_name not in self.usage_counters:
                                self.usage_counters[app_name] = 0
                            self.usage_counters[app_name] += self.check_interval
                    
                    # Periodically save accumulated time to database
                    current_time = time.time()
                    if current_time - self.last_save_time >= self.save_interval:
                        self._save_accumulated_time()
                        self.last_save_time = current_time
                
                # Sleep for the check interval
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"[AppMonitor] Error in monitor loop: {e}")
                time.sleep(self.check_interval)
        
        print("[AppMonitor] Monitor loop ended")
    
    def _get_running_watched_apps(self, watchlist: list) -> Set[str]:
        """
        Check which applications from the watchlist are currently running.
        
        Args:
            watchlist: List of executable names to watch for
            
        Returns:
            Set of running application names from the watchlist
        """
        running_apps = set()
        watchlist_lower = [app.lower() for app in watchlist]
        
        try:
            # Iterate through all running processes
            for proc in psutil.process_iter(['name']):
                try:
                    # Get process name
                    proc_name = proc.info['name']
                    if proc_name:
                        proc_name_lower = proc_name.lower()
                        
                        # Check if process is in watchlist
                        if proc_name_lower in watchlist_lower:
                            running_apps.add(proc_name_lower)
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process terminated or access denied - skip it
                    continue
                except Exception as e:
                    # Unexpected error - log and continue
                    print(f"[AppMonitor] Error checking process: {e}")
                    continue
        
        except Exception as e:
            print(f"[AppMonitor] Error iterating processes: {e}")
        
        return running_apps
    
    def _save_accumulated_time(self):
        """
        Save accumulated time to the database and reset counters.
        Thread-safe operation.
        """
        with self.lock:
            if not self.usage_counters:
                return
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Save each app's accumulated time
            for app_name, seconds in self.usage_counters.items():
                if seconds > 0:
                    try:
                        self.db_manager.update_duration(app_name, today, seconds)
                        print(f"[AppMonitor] Saved {seconds}s for {app_name}")
                    except Exception as e:
                        print(f"[AppMonitor] Error saving time for {app_name}: {e}")
            
            # Reset counters after saving
            self.usage_counters.clear()
    
    def force_save(self):
        """Force an immediate save of accumulated time (for manual refresh)."""
        self._save_accumulated_time()
        self.last_save_time = time.time()
        print("[AppMonitor] Forced save completed")
    
    def get_current_tracking(self) -> Dict[str, int]:
        """
        Get currently tracked apps and their pending (unsaved) time.
        
        Returns:
            Dictionary of app_name -> seconds not yet saved to database
        """
        with self.lock:
            return self.usage_counters.copy()
    
    def is_active(self) -> bool:
        """
        Check if monitor is currently running.
        
        Returns:
            True if monitoring is active
        """
        with self.lock:
            return self.is_running


# Testing the monitor service
if __name__ == "__main__":
    from database_manager import DatabaseManager
    from config_manager import ConfigManager
    
    # Create test instances
    db = DatabaseManager("test_tracker.db")
    config = ConfigManager("test_settings.json")
    
    # Add some apps to watchlist
    config.add_app("chrome.exe")
    config.add_app("notepad.exe")
    
    # Create and start monitor
    monitor = AppMonitor(db, config)
    monitor.start()
    
    print("Monitoring for 30 seconds...")
    print("Open Chrome or Notepad to see tracking in action")
    
    # Run for 30 seconds
    time.sleep(30)
    
    # Stop monitor
    monitor.stop()
    
    # Check results
    stats = db.get_today_stats()
    print("Today's stats:", stats)
    
    # Clean up
    import os
    if os.path.exists("test_tracker.db"):
        os.remove("test_tracker.db")
    if os.path.exists("test_settings.json"):
        os.remove("test_settings.json")
    print("Test files cleaned up")
