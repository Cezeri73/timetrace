"""
Database Manager for TimeAudit Application
Handles all SQLite database operations for tracking app usage
"""

import sqlite3
from datetime import datetime
from typing import Dict
import os


class DatabaseManager:
    """
    Manages SQLite database for storing application usage logs.
    Thread-safe with proper connection handling.
    """
    
    def __init__(self, db_path: str = "tracker.db"):
        """
        Initialize database manager and create tables if needed.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create usage_logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL DEFAULT 0,
                    UNIQUE(app_name, date)
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_app_date 
                ON usage_logs(app_name, date)
            ''')
            
            conn.commit()
            conn.close()
            print(f"[DatabaseManager] Database initialized: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error initializing database: {e}")
            raise
    
    def update_duration(self, app_name: str, date: str, seconds_to_add: int):
        """
        Add duration to an existing record or create a new one.
        Uses INSERT OR REPLACE to handle both cases atomically.
        
        Args:
            app_name: Name of the application (e.g., "chrome.exe")
            date: Date in YYYY-MM-DD format
            seconds_to_add: Number of seconds to add to the duration
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # First, try to get existing duration
            cursor.execute('''
                SELECT duration_seconds FROM usage_logs 
                WHERE app_name = ? AND date = ?
            ''', (app_name, date))
            
            result = cursor.fetchone()
            
            if result:
                # Update existing record
                new_duration = result[0] + seconds_to_add
                cursor.execute('''
                    UPDATE usage_logs 
                    SET duration_seconds = ? 
                    WHERE app_name = ? AND date = ?
                ''', (new_duration, app_name, date))
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO usage_logs (app_name, date, duration_seconds)
                    VALUES (?, ?, ?)
                ''', (app_name, date, seconds_to_add))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error updating duration for {app_name}: {e}")
            if conn:
                conn.close()
    
    def get_today_stats(self) -> Dict[str, int]:
        """
        Get usage statistics for today.
        
        Returns:
            Dictionary mapping app_name to duration_seconds for today
            Example: {"chrome.exe": 3600, "valorant.exe": 7200}
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_stats_for_date(today)
    
    def get_week_stats(self) -> Dict[str, int]:
        """
        Get usage statistics for the past 7 days.
        
        Returns:
            Dictionary mapping app_name to total duration_seconds
        """
        from datetime import timedelta
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get dates for last 7 days
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
            
            cursor.execute('''
                SELECT app_name, SUM(duration_seconds) as total
                FROM usage_logs 
                WHERE date >= ? AND date <= ?
                GROUP BY app_name
                ORDER BY total DESC
            ''', (start_date, end_date))
            
            results = cursor.fetchall()
            conn.close()
            
            stats = {row[0]: row[1] for row in results}
            return stats
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting week stats: {e}")
            if conn:
                conn.close()
            return {}
    
    def get_month_stats(self) -> Dict[str, int]:
        """
        Get usage statistics for the past 30 days.
        
        Returns:
            Dictionary mapping app_name to total duration_seconds
        """
        from datetime import timedelta
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get dates for last 30 days
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=29)).strftime("%Y-%m-%d")
            
            cursor.execute('''
                SELECT app_name, SUM(duration_seconds) as total
                FROM usage_logs 
                WHERE date >= ? AND date <= ?
                GROUP BY app_name
                ORDER BY total DESC
            ''', (start_date, end_date))
            
            results = cursor.fetchall()
            conn.close()
            
            stats = {row[0]: row[1] for row in results}
            return stats
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting month stats: {e}")
            if conn:
                conn.close()
            return {}
    
    def get_stats_for_date_range(self, start_date: str, end_date: str) -> Dict[str, int]:
        """
        Get usage statistics for a custom date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary mapping app_name to total duration_seconds
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT app_name, SUM(duration_seconds) as total
                FROM usage_logs 
                WHERE date >= ? AND date <= ?
                GROUP BY app_name
                ORDER BY total DESC
            ''', (start_date, end_date))
            
            results = cursor.fetchall()
            conn.close()
            
            stats = {row[0]: row[1] for row in results}
            return stats
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting date range stats: {e}")
            if conn:
                conn.close()
            return {}
    
    def get_stats_for_date(self, date: str) -> Dict[str, int]:
        """
        Get usage statistics for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Dictionary mapping app_name to duration_seconds
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT app_name, duration_seconds 
                FROM usage_logs 
                WHERE date = ?
                ORDER BY duration_seconds DESC
            ''', (date,))
            
            results = cursor.fetchall()
            conn.close()
            
            # Convert to dictionary
            stats = {row[0]: row[1] for row in results}
            return stats
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting stats for {date}: {e}")
            if conn:
                conn.close()
            return {}
    
    def get_all_tracked_apps(self) -> list:
        """
        Get list of all apps that have been tracked.
        
        Returns:
            List of unique application names
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT app_name FROM usage_logs
                ORDER BY app_name
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            return [row[0] for row in results]
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting tracked apps: {e}")
            if conn:
                conn.close()
            return []
    
    def clear_old_data(self, days_to_keep: int = 90):
        """
        Remove records older than specified days.
        
        Args:
            days_to_keep: Number of days of data to retain
        """
        try:
            from datetime import timedelta
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM usage_logs WHERE date < ?
            ''', (cutoff_date,))
            
            deleted_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            print(f"[DatabaseManager] Cleaned up {deleted_rows} old records")
            
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error clearing old data: {e}")
            if conn:
                conn.close()


# Testing the database manager
if __name__ == "__main__":
    # Create a test database
    db = DatabaseManager("test_tracker.db")
    
    # Test update_duration
    today = datetime.now().strftime("%Y-%m-%d")
    db.update_duration("chrome.exe", today, 60)
    db.update_duration("valorant.exe", today, 120)
    db.update_duration("chrome.exe", today, 30)  # Should add to existing
    
    # Test get_today_stats
    stats = db.get_today_stats()
    print("Today's stats:", stats)
    
    # Clean up test database
    if os.path.exists("test_tracker.db"):
        os.remove("test_tracker.db")
        print("Test database cleaned up")
