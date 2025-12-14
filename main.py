"""
Main Entry Point for TimeTrace Application
Integrates GUI, monitoring, and system tray functionality
"""

import sys
import threading
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from database_manager import DatabaseManager
from config_manager import ConfigManager
from monitor_service import AppMonitor
from main_ui import TimeTraceUI


class TimeTraceApp:
    """
    Main application class integrating all components.
    Handles system tray integration and lifecycle management.
    """
    
    def __init__(self):
        """Initialize the TimeTrace application."""
        print("[TimeTrace] Starting TimeTrace Application...")
        
        # Initialize components
        self.db_manager = DatabaseManager("tracker.db")
        self.config_manager = ConfigManager("settings.json")
        self.monitor = AppMonitor(self.db_manager, self.config_manager)
        
        # UI will be created in run()
        self.ui = None
        
        # System tray
        self.tray_icon = None
        self.tray_thread = None
        
        # Application state
        self.is_running = True
        
        print("[TimeAudit] Application initialized")
    
    def create_tray_icon(self):
        """Create a system tray icon."""
        # Create a simple icon image
        icon_image = self._create_icon_image()
        
        # Define menu items
        menu = pystray.Menu(
            item('Show', self._show_window, default=True),
            item('Hide', self._hide_window),
            pystray.Menu.SEPARATOR,
            item('Exit', self._quit_application)
        )
        
        # Create tray icon
        self.tray_icon = pystray.Icon(
            "TimeTrace",
            icon_image,
            "TimeTrace - App Usage Tracker",
            menu
        )
        
        print("[TimeTrace] System tray icon created")
    
    def _create_icon_image(self):
        """
        Create a simple icon image for the system tray.
        
        Returns:
            PIL Image object
        """
        # Create a 64x64 image with a clock-like icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='#1f538d')
        
        # Draw a simple clock face
        draw = ImageDraw.Draw(image)
        
        # Draw circle (clock outline)
        padding = 8
        draw.ellipse(
            [padding, padding, width - padding, height - padding],
            fill='#1f538d',
            outline='white',
            width=3
        )
        
        # Draw clock hands
        center_x = width // 2
        center_y = height // 2
        
        # Hour hand
        draw.line(
            [(center_x, center_y), (center_x + 10, center_y - 15)],
            fill='white',
            width=3
        )
        
        # Minute hand
        draw.line(
            [(center_x, center_y), (center_x + 15, center_y - 5)],
            fill='white',
            width=2
        )
        
        return image
    
    def _show_window(self, icon=None, item=None):
        """Show the main application window."""
        if self.ui:
            self.ui.show()
            print("[TimeTrace] Window shown")
    
    def _hide_window(self, icon=None, item=None):
        """Hide the main application window."""
        if self.ui:
            self.ui.hide()
            print("[TimeTrace] Window hidden")
    
    def _on_window_close(self):
        """Handle window close event - minimize to tray instead of quitting."""
        minimize_to_tray = self.config_manager.get_setting("minimize_to_tray", True)
        
        if minimize_to_tray:
            self._hide_window()
        else:
            self._quit_application()
    
    def _quit_application(self, icon=None, item=None):
        """Completely quit the application."""
        print("[TimeTrace] Shutting down application...")
        
        self.is_running = False
        
        # Stop monitoring
        if self.monitor:
            self.monitor.stop()
        
        # Stop tray icon
        if self.tray_icon:
            self.tray_icon.stop()
        
        # Destroy UI
        if self.ui:
            try:
                self.ui.destroy()
            except:
                pass  # Window might already be destroyed
        
        print("[TimeTrace] Application shut down successfully")
        sys.exit(0)
    
    def run_tray_icon(self):
        """Run the system tray icon in a separate thread."""
        if self.tray_icon:
            print("[TimeTrace] Starting system tray icon...")
            self.tray_icon.run()
    
    def run(self):
        """Start the application."""
        try:
            # Start monitoring service
            self.monitor.start()
            
            # Create system tray icon
            self.create_tray_icon()
            
            # Start tray icon in a separate thread
            self.tray_thread = threading.Thread(target=self.run_tray_icon, daemon=True)
            self.tray_thread.start()
            
            # Create and show UI
            self.ui = TimeTraceUI(
                self.db_manager,
                self.config_manager,
                self.monitor,
                on_close_callback=self._on_window_close
            )
            
            print("[TimeTrace] Application ready!")
            print("[TimeTrace] You can minimize to system tray when closing the window")
            
            # Run UI main loop (blocking)
            self.ui.run()
            
            # If we get here, the UI was closed without going to tray
            self._quit_application()
            
        except KeyboardInterrupt:
            print("\n[TimeTrace] Keyboard interrupt received")
            self._quit_application()
        except Exception as e:
            print(f"[TimeTrace] Fatal error: {e}")
            import traceback
            traceback.print_exc()
            self._quit_application()


def main():
    """Main entry point."""
    print("=" * 60)
    print("TimeTrace - Application Usage Tracker")
    print("Track how much time you spend on different applications")
    print("=" * 60)
    print()
    
    app = TimeTraceApp()
    app.run()


if __name__ == "__main__":
    main()
