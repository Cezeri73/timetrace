"""
Notification Service for TimeTrace
Sends desktop notifications when usage thresholds are exceeded
"""

import threading
from typing import Dict, Optional
from database_manager import DatabaseManager
from config_manager import ConfigManager
from datetime import datetime
import time

try:
    from win10toast import ToastNotifier
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False
    print("[NotificationService] win10toast not available - notifications disabled")


class NotificationService:
    """
    Monitors app usage and sends notifications when thresholds are exceeded.
    Runs as a background thread.
    """
    
    def __init__(self, db_manager: DatabaseManager, config_manager: ConfigManager):
        """
        Initialize notification service.
        
        Args:
            db_manager: DatabaseManager instance
            config_manager: ConfigManager instance
        """
        self.db_manager = db_manager
        self.config_manager = config_manager
        self.running = False
        self.thread = None
        self._notification_sent_today = {}  # Track which apps already notified
        
        # Default thresholds (in hours)
        self.default_thresholds = {
            "chrome.exe": 4,
            "discord.exe": 3,
            "valorant.exe": 4,
            "firefox.exe": 4,
            "vscode.exe": 8,
            "code.exe": 8,
        }
        
        print("[NotificationService] Initialized")
    
    def start(self):
        """Start the notification monitoring thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._notification_loop, daemon=True)
        self.thread.start()
        print("[NotificationService] Started")
    
    def stop(self):
        """Stop the notification monitoring thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("[NotificationService] Stopped")
    
    def _notification_loop(self):
        """Main notification monitoring loop."""
        while self.running:
            try:
                # Skip during quiet hours or snooze
                if not self._is_quiet_hours() and not self._is_snoozed():
                    self._check_thresholds()
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"[NotificationService] Error in notification loop: {e}")
    
    def _check_thresholds(self):
        """Check if any app has exceeded its threshold."""
        if not NOTIFICATION_AVAILABLE:
            return
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # Reset notifications for new day
        if not hasattr(self, '_last_check_date') or self._last_check_date != today_str:
            self._notification_sent_today = {}
            self._last_check_date = today_str
        
        try:
            stats = self.db_manager.get_today_stats()
            
            for app_name, total_seconds in stats.items():
                # Skip if already notified
                if app_name in self._notification_sent_today:
                    continue
                
                # Get threshold (from config or default)
                threshold_hours = self._get_threshold(app_name)
                threshold_seconds = threshold_hours * 3600
                
                # Check if exceeded
                if total_seconds >= threshold_seconds:
                    self._send_notification(app_name, total_seconds, threshold_hours)
                    self._notification_sent_today[app_name] = True
                    
        except Exception as e:
            print(f"[NotificationService] Error checking thresholds: {e}")
    
    def _get_threshold(self, app_name: str) -> float:
        """
        Get the usage threshold for an app.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Threshold in hours
        """
        thresholds = self.config_manager.get_setting("notification_thresholds")
        
        if thresholds is None:
            thresholds = self.default_thresholds
        
        # Check exact match
        if app_name in thresholds:
            return float(thresholds[app_name])
        
        # Check case-insensitive match
        for key, value in thresholds.items():
            if key.lower() == app_name.lower():
                return float(value)
        
        # Return default threshold if not configured
        return 2.0  # 2 hours default
    
    def _send_notification(self, app_name: str, total_seconds: int, threshold_hours: float):
        """
        Send a desktop notification.
        
        Args:
            app_name: Application name
            total_seconds: Total usage in seconds
            threshold_hours: Threshold in hours
        """
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        
        message = f"{app_name.replace('.exe', '')} uygulamasını {hours}s {minutes}d kullanıyorsunuz!"
        
        try:
            if NOTIFICATION_AVAILABLE:
                notifier = ToastNotifier()
                notifier.show_toast(
                    "TimeTrace - Kullanım Uyarısı",
                    message,
                    duration=10,
                    threaded=True
                )
                # Record a short snooze if configured
                snooze_minutes = int(self.config_manager.get_setting("notification_snooze_minutes") or 0)
                if snooze_minutes > 0:
                    from datetime import timedelta
                    self._snooze_until = datetime.now() + timedelta(minutes=snooze_minutes)
            print(f"[NotificationService] Notification sent: {message}")
        except Exception as e:
            print(f"[NotificationService] Error sending notification: {e}")
    
    def set_threshold(self, app_name: str, threshold_hours: float):
        """
        Set custom threshold for an app.
        
        Args:
            app_name: Application name
            threshold_hours: Threshold in hours
        """
        thresholds = self.config_manager.get_setting("notification_thresholds")
        if thresholds is None:
            thresholds = self.default_thresholds.copy()
        
        thresholds[app_name] = threshold_hours
        self.config_manager.set_setting("notification_thresholds", thresholds)
        print(f"[NotificationService] Threshold set: {app_name} -> {threshold_hours}h")
    
    def get_threshold(self, app_name: str) -> float:
        """
        Get current threshold for an app.
        
        Args:
            app_name: Application name
            
        Returns:
            Threshold in hours
        """
        return self._get_threshold(app_name)
    
    def reset_thresholds(self):
        """Reset all thresholds to defaults."""
        self.config_manager.set_setting("notification_thresholds", self.default_thresholds.copy())
        print("[NotificationService] Thresholds reset to defaults")

    # Quiet hours and Snooze helpers
    def _is_quiet_hours(self) -> bool:
        """Return True if current time falls within quiet hours."""
        try:
            start = self.config_manager.get_setting("quiet_hours_start")  # e.g., "22:00"
            end = self.config_manager.get_setting("quiet_hours_end")      # e.g., "07:00"
            if not start or not end:
                return False
            now = datetime.now().time()
            from datetime import datetime as dt
            s = dt.strptime(start, "%H:%M").time()
            e = dt.strptime(end, "%H:%M").time()
            if s < e:
                return s <= now <= e
            else:
                # Over midnight
                return now >= s or now <= e
        except Exception:
            return False

    def _is_snoozed(self) -> bool:
        """Return True if notifications are snoozed until a future time."""
        try:
            return hasattr(self, "_snooze_until") and self._snooze_until and datetime.now() < self._snooze_until
        except Exception:
            return False
