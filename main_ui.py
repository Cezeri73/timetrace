"""
Main UI for TimeTrace Application
Modern GUI using CustomTkinter with tabbed interface
"""

import customtkinter as ctk
from typing import Callable, Dict, List
from database_manager import DatabaseManager
from config_manager import ConfigManager
from monitor_service import AppMonitor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import psutil
import os
import sys


# Uygulama Kategorileri
APP_CATEGORIES = {
    "🎮 Oyunlar": [
        "valorant.exe", "leagueclient.exe", "riotclientservices.exe",
        "csgo.exe", "dota2.exe", "elden ring.exe", "minecraft.exe",
        "fortnite.exe", "apex.exe", "overwatch2.exe"
    ],
    "🌐 Tarayıcılar": [
        "chrome.exe", "firefox.exe", "msedge.exe", "brave.exe",
        "opera.exe", "vivaldi.exe", "chromium.exe", "iexplore.exe"
    ],
    "💬 İletişim": [
        "discord.exe", "telegram.exe", "slack.exe", "whatsapp.exe",
        "skype.exe", "zoom.exe", "teams.exe", "messenger.exe"
    ],
    "📝 Metin & Ofis": [
        "notepad.exe", "notepad++.exe", "code.exe", "winword.exe",
        "excel.exe", "powerpnt.exe", "adobephotoshop.exe", "gimp.exe"
    ],
    "🎵 Medya & Tasarım": [
        "spotify.exe", "vlc.exe", "audacity.exe", "obs64.exe",
        "blender.exe", "clip studio.exe", "aseprite.exe"
    ],
    "⚙️ Geliştirme Araçları": [
        "pycharm64.exe", "clion64.exe", "idea64.exe", "visual studio.exe",
        "git.exe", "docker.exe", "nodejs.exe", "java.exe"
    ],
    "📊 Diğer Uygulamalar": []
}

# Sistem Processlerini Filtrele (gösterilmeyecekler)
SYSTEM_PROCESSES = {
    "system.exe", "svchost.exe", "csrss.exe", "lsass.exe",
    "services.exe", "smss.exe", "explorer.exe", "dwm.exe",
    "searchindexer.exe", "nvcontainer.exe", "spoolsv.exe",
    "conhost.exe", "rundll32.exe", "wininit.exe", "taskhost.exe",
    "audiodg.exe", "sqlwriter.exe", "mysqld.exe", "nvidia.exe",
    "igfxem.exe", "igfxhk.exe", "amd.exe", "nvwmi.exe"
}


class TimeTraceUI:
    """
    Main GUI application using CustomTkinter.
    Features a tabbed interface with Dashboard and Settings views.
    """
    
    def __init__(self, db_manager: DatabaseManager, config_manager: ConfigManager, 
                 monitor: AppMonitor, notification_service=None, on_close_callback: Callable = None):
        """
        Initialize the TimeTrace UI.
        
        Args:
            db_manager: DatabaseManager instance
            config_manager: ConfigManager instance
            monitor: AppMonitor instance
            notification_service: NotificationService instance (optional)
            on_close_callback: Function to call when window is closed
        """
        self.db_manager = db_manager
        self.config_manager = config_manager
        self.monitor = monitor
        self.notification_service = notification_service
        self.on_close_callback = on_close_callback
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("TimeTrace - Application Usage Tracker")
        self.root.geometry("800x600")
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Create UI components
        self._create_widgets()
        
        print("[TimeTraceUI] UI initialized")
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Create tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tab_dashboard = self.tabview.add("📊 Dashboard")
        self.tab_charts = self.tabview.add("📈 Grafikler")
        self.tab_notifications = self.tabview.add("🔔 Bildirimler")
        self.tab_history = self.tabview.add("📅 Geçmiş")
        self.tab_watchlist = self.tabview.add("⚙️ Watchlist")
        self.tab_advanced_settings = self.tabview.add("🔧 Gelişmiş Ayarlar")
        self.tab_help = self.tabview.add("❓ Nasıl Kullanılır")
        
        # Keep old reference for backward compatibility
        self.tab_settings = self.tab_watchlist
        
        # Setup each tab
        self._setup_dashboard_tab()
        self._setup_charts_tab()
        self._setup_notifications_tab()
        self._setup_history_tab()
        self._setup_watchlist_tab()
        self._setup_advanced_settings_tab()
        self._setup_help_tab()
    
    def _setup_dashboard_tab(self):
        """Setup the Dashboard tab with usage statistics."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_dashboard,
            text="Uygulama Kullanım İstatistikleri",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Time period selector
        period_frame = ctk.CTkFrame(self.tab_dashboard)
        period_frame.pack(pady=10)
        
        period_label = ctk.CTkLabel(
            period_frame,
            text="Dönem Seç:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        period_label.pack(side="left", padx=10)
        
        self.period_var = ctk.StringVar(value="today")
        
        today_btn = ctk.CTkButton(
            period_frame,
            text="📅 Bugün",
            command=lambda: self._set_period("today"),
            width=80
        )
        today_btn.pack(side="left", padx=5)
        
        week_btn = ctk.CTkButton(
            period_frame,
            text="📊 Hafta",
            command=lambda: self._set_period("week"),
            width=80
        )
        week_btn.pack(side="left", padx=5)
        
        month_btn = ctk.CTkButton(
            period_frame,
            text="📈 Ay",
            command=lambda: self._set_period("month"),
            width=80
        )
        month_btn.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            self.tab_dashboard,
            text="🔄 İstatistikleri Yenile",
            command=self._refresh_dashboard,
            width=150,
            height=35
        )
        refresh_btn.pack(pady=10)
        
        # Scrollable frame for app list
        self.stats_frame = ctk.CTkScrollableFrame(
            self.tab_dashboard,
            width=700,
            height=400
        )
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initial load of stats
        self._refresh_dashboard()
    
    def _set_period(self, period: str):
        """
        Set statistics period and refresh.
        
        Args:
            period: "today", "week", or "month"
        """
        self.period_var.set(period)
        self._refresh_dashboard()
    
    def _setup_charts_tab(self):
        """Setup the Charts tab with matplotlib visualizations."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_charts,
            text="Kullanım Trendleri ve Grafikler",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Chart type selector
        chart_frame = ctk.CTkFrame(self.tab_charts)
        chart_frame.pack(pady=10)
        
        chart_label = ctk.CTkLabel(
            chart_frame,
            text="Grafik Türü:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        chart_label.pack(side="left", padx=10)
        
        self.chart_type_var = ctk.StringVar(value="top_apps")
        
        top_apps_btn = ctk.CTkButton(
            chart_frame,
            text="🏆 En Çok Kullanılan",
            command=lambda: self._plot_top_apps_chart(),
            width=120
        )
        top_apps_btn.pack(side="left", padx=5)
        
        trend_btn = ctk.CTkButton(
            chart_frame,
            text="📉 Günlük Trend",
            command=lambda: self._plot_daily_trend_chart(),
            width=120
        )
        trend_btn.pack(side="left", padx=5)
        
        category_btn = ctk.CTkButton(
            chart_frame,
            text="🎯 Kategori Dağılımı",
            command=lambda: self._plot_category_chart(),
            width=120
        )
        category_btn.pack(side="left", padx=5)

        compare_btn = ctk.CTkButton(
            chart_frame,
            text="📊 Karşılaştır (Hafta)",
            command=lambda: self._plot_compare_chart(),
            width=140
        )
        compare_btn.pack(side="left", padx=5)
        
        # Chart period selector
        period_label = ctk.CTkLabel(
            chart_frame,
            text="Dönem:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        period_label.pack(side="left", padx=10)
        
        self.chart_period_var = ctk.StringVar(value="week")
        
        week_btn = ctk.CTkButton(
            chart_frame,
            text="Hafta",
            command=lambda: self._set_chart_period("week"),
            width=80
        )
        week_btn.pack(side="left", padx=5)
        
        month_btn = ctk.CTkButton(
            chart_frame,
            text="Ay",
            command=lambda: self._set_chart_period("month"),
            width=80
        )
        month_btn.pack(side="left", padx=5)
        
        # Canvas frame for charts
        self.chart_canvas_frame = ctk.CTkFrame(self.tab_charts)
        self.chart_canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial chart
        self._plot_top_apps_chart()
    
    def _set_chart_period(self, period: str):
        """Set chart period and refresh."""
        self.chart_period_var.set(period)
        chart_type = self.chart_type_var.get() if hasattr(self, 'chart_type_var') else "top_apps"
        if chart_type == "top_apps":
            self._plot_top_apps_chart()
        elif chart_type == "trend":
            self._plot_daily_trend_chart()
        else:
            self._plot_category_chart()
    
    def _plot_top_apps_chart(self):
        """Plot top 10 most used apps."""
        self.chart_type_var.set("top_apps")
        
        # Clear previous chart
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            period = self.chart_period_var.get() if hasattr(self, 'chart_period_var') else "week"
            
            if period == "week":
                stats = self.db_manager.get_week_stats()
                title = "Son 7 Gün - En Çok Kullanılan Uygulamalar (Top 10)"
            else:
                stats = self.db_manager.get_month_stats()
                title = "Son 30 Gün - En Çok Kullanılan Uygulamalar (Top 10)"
            
            if not stats:
                label = ctk.CTkLabel(
                    self.chart_canvas_frame,
                    text="Grafik için yeterli veri yok",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                label.pack(pady=50)
                return
            
            # Sort and take top 10
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:10]
            apps = [item[0] for item in sorted_stats]
            durations = [item[1] / 3600 for item in sorted_stats]  # Convert to hours
            
            # Create figure
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)
            
            bars = ax.bar(range(len(apps)), durations, color='#1f538d')
            ax.set_xlabel('Uygulama', fontsize=10, fontweight='bold')
            ax.set_ylabel('Saat (hours)', fontsize=10, fontweight='bold')
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xticks(range(len(apps)))
            ax.set_xticklabels(apps, rotation=45, ha='right', fontsize=9)
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for i, (bar, duration) in enumerate(zip(bars, durations)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{duration:.1f}h',
                       ha='center', va='bottom', fontsize=8)
            
            fig.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_canvas_frame,
                text=f"Grafik oluşturma hatası: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
            print(f"[TimeTraceUI] Chart error: {e}")
    
    def _plot_daily_trend_chart(self):
        """Plot daily usage trend over time."""
        self.chart_type_var.set("trend")
        
        # Clear previous chart
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            period = self.chart_period_var.get() if hasattr(self, 'chart_period_var') else "week"
            
            if period == "week":
                days = 7
                title = "Son 7 Gün - Günlük Toplam Kullanım"
            else:
                days = 30
                title = "Son 30 Gün - Günlük Toplam Kullanım"
            
            # Get daily totals
            daily_totals = []
            daily_labels = []
            today = datetime.now().date()
            
            for i in range(days - 1, -1, -1):
                date = today - timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                
                stats = self.db_manager.get_stats_for_date_range(date_str, date_str)
                total_seconds = sum(stats.values()) if stats else 0
                total_hours = total_seconds / 3600
                
                daily_totals.append(total_hours)
                daily_labels.append(date.strftime("%m-%d"))
            
            if not any(daily_totals):
                label = ctk.CTkLabel(
                    self.chart_canvas_frame,
                    text="Grafik için yeterli veri yok",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                label.pack(pady=50)
                return
            
            # Create figure
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)
            
            ax.plot(range(len(daily_totals)), daily_totals, marker='o', 
                   color='#1f538d', linewidth=2, markersize=6)
            ax.fill_between(range(len(daily_totals)), daily_totals, alpha=0.3, color='#1f538d')
            ax.set_xlabel('Tarih', fontsize=10, fontweight='bold')
            ax.set_ylabel('Saat (hours)', fontsize=10, fontweight='bold')
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xticks(range(0, len(daily_labels), max(1, len(daily_labels)//7)))
            ax.set_xticklabels([daily_labels[i] for i in range(0, len(daily_labels), max(1, len(daily_labels)//7))], 
                              rotation=45, ha='right', fontsize=9)
            ax.grid(True, alpha=0.3)
            
            fig.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_canvas_frame,
                text=f"Grafik oluşturma hatası: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
            print(f"[TimeTraceUI] Chart error: {e}")
    
    def _plot_category_chart(self):
        """Plot category distribution pie chart."""
        self.chart_type_var.set("category")
        
        # Clear previous chart
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            period = self.chart_period_var.get() if hasattr(self, 'chart_period_var') else "week"
            
            if period == "week":
                stats = self.db_manager.get_week_stats()
                title = "Son 7 Gün - Kategori Dağılımı"
            else:
                stats = self.db_manager.get_month_stats()
                title = "Son 30 Gün - Kategori Dağılımı"
            
            if not stats:
                label = ctk.CTkLabel(
                    self.chart_canvas_frame,
                    text="Grafik için yeterli veri yok",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                label.pack(pady=50)
                return
            
            # Categorize apps
            category_totals = {}
            for app_name, seconds in stats.items():
                category = "📊 Diğer Uygulamalar"
                for cat, apps in APP_CATEGORIES.items():
                    if any(app_name.lower() == app.lower() for app in apps):
                        category = cat
                        break
                
                if category not in category_totals:
                    category_totals[category] = 0
                category_totals[category] += seconds
            
            # Convert to hours and sort
            categories = list(category_totals.keys())
            hours = [v / 3600 for v in category_totals.values()]
            
            # Create figure
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)
            
            colors = ['#1f538d', '#2e7db3', '#3d9dd9', '#4cbdff', '#5eceff', '#6edfff', '#7eefff']
            wedges, texts, autotexts = ax.pie(hours, labels=categories, autopct='%1.1f%%',
                                              colors=colors[:len(categories)], startangle=90)
            ax.set_title(title, fontsize=12, fontweight='bold')
            
            # Format text
            for text in texts:
                text.set_fontsize(9)
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(8)
                autotext.set_fontweight('bold')
            
            fig.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_canvas_frame,
                text=f"Grafik oluşturma hatası: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
            print(f"[TimeTraceUI] Chart error: {e}")

    def _plot_compare_chart(self):
        """Compare last 7 days vs previous 7 days total hours."""
        self.chart_type_var.set("compare")
        
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            from datetime import datetime, timedelta
            today = datetime.now().date()
            
            def _range_total(start, end):
                stats = self.db_manager.get_stats_for_date_range(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
                return sum(stats.values())/3600 if stats else 0
            
            # Last 7 days
            end1 = today
            start1 = today - timedelta(days=6)
            total1 = _range_total(start1, end1)
            
            # Previous 7 days
            end2 = start1 - timedelta(days=1)
            start2 = end2 - timedelta(days=6)
            total2 = _range_total(start2, end2)
            
            fig = Figure(figsize=(6,4), dpi=100)
            ax = fig.add_subplot(111)
            labels = ["Son 7 Gün", "Önceki 7 Gün"]
            values = [total1, total2]
            bars = ax.bar(labels, values, color=['#1f538d','#3d9dd9'])
            ax.set_ylabel('Saat (hours)', fontsize=10, fontweight='bold')
            ax.set_title('Haftalık Karşılaştırma', fontsize=12, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            for bar, val in zip(bars, values):
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height(), f"{val:.1f}h", ha='center', va='bottom', fontsize=9)
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.chart_canvas_frame,
                text=f"Grafik oluşturma hatası: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
            print(f"[TimeTraceUI] Chart error: {e}")
    
    def _setup_notifications_tab(self):
        """Setup the Notifications tab for threshold configuration."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_notifications,
            text="Kullanım Uyarıları",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Info section
        info_frame = ctk.CTkFrame(self.tab_notifications)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Bilgi: Belirlediğiniz saat sınırına ulaştığında, masaüstü bildirim alacaksınız.",
            font=ctk.CTkFont(size=12),
            text_color="#FFD700"
        )
        info_label.pack(anchor="w", padx=10, pady=5)
        
        # Thresholds section
        thresholds_frame = ctk.CTkFrame(self.tab_notifications)
        thresholds_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        thresholds_label = ctk.CTkLabel(
            thresholds_frame,
            text="⏰ Uygulama Saat Sınırları",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        thresholds_label.pack(anchor="w", pady=10)
        
        # Scrollable frame for threshold settings
        self.thresholds_scroll = ctk.CTkScrollableFrame(
            thresholds_frame,
            width=600,
            height=300
        )
        self.thresholds_scroll.pack(fill="both", expand=True, padx=10)
        
        # Load current thresholds from notification service
        self._load_notification_thresholds()
        
        # Button frame
        button_frame = ctk.CTkFrame(self.tab_notifications)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Varsayılana Sıfırla",
            command=self._reset_notification_thresholds,
            width=150
        )
        reset_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Ayarları Kaydet",
            command=self._save_notification_thresholds,
            width=150
        )
        save_btn.pack(side="left", padx=5)
    
    def _load_notification_thresholds(self):
        """Load and display notification thresholds."""
        if not self.notification_service:
            return
        
        # Get watchlist from config
        watchlist = self.config_manager.get_watchlist()
        
        self.threshold_entries = {}
        
        for app_name in sorted(watchlist):
            threshold = self.notification_service.get_threshold(app_name)
            
            app_frame = ctk.CTkFrame(self.thresholds_scroll)
            app_frame.pack(fill="x", padx=5, pady=5)
            
            # App name label
            label = ctk.CTkLabel(
                app_frame,
                text=app_name.replace(".exe", ""),
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w",
                width=150
            )
            label.pack(side="left", padx=10)
            
            # Entry for threshold
            entry = ctk.CTkEntry(
                app_frame,
                placeholder_text="Saat",
                width=80
            )
            entry.insert(0, str(threshold))
            entry.pack(side="left", padx=5)
            
            # Unit label
            unit_label = ctk.CTkLabel(
                app_frame,
                text="Saat",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            unit_label.pack(side="left", padx=5)
            
            self.threshold_entries[app_name] = entry
    
    def _save_notification_thresholds(self):
        """Save notification thresholds."""
        if not self.notification_service:
            return
        
        try:
            for app_name, entry in self.threshold_entries.items():
                try:
                    threshold = float(entry.get())
                    self.notification_service.set_threshold(app_name, threshold)
                except ValueError:
                    print(f"[TimeTraceUI] Invalid threshold for {app_name}")
            
            print("[TimeTraceUI] Notification thresholds saved")
            
            # Show success message
            message = ctk.CTkLabel(
                self.tab_notifications,
                text="✓ Ayarlar başarıyla kaydedildi!",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            message.pack(pady=10)
            
            # Auto-remove after 3 seconds
            self.root.after(3000, message.destroy)
            
        except Exception as e:
            print(f"[TimeTraceUI] Error saving thresholds: {e}")
    
    def _reset_notification_thresholds(self):
        """Reset notification thresholds to defaults."""
        if not self.notification_service:
            return
        
        self.notification_service.reset_thresholds()
        
        # Reload the thresholds display
        for widget in self.thresholds_scroll.winfo_children():
            widget.destroy()
        
        self._load_notification_thresholds()
        
        print("[TimeTraceUI] Notification thresholds reset to defaults")
    
    def _setup_history_tab(self):
        """Setup the History tab with date filtering."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_history,
            text="Geçmiş İstatistikler",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Date range selection frame
        date_frame = ctk.CTkFrame(self.tab_history)
        date_frame.pack(pady=15, padx=20, fill="x")
        
        # Start date
        start_label = ctk.CTkLabel(
            date_frame,
            text="Başlangıç Tarihi (YYYY-MM-DD):",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        start_label.pack(side="left", padx=10)
        
        self.history_start_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="2024-01-01",
            width=120
        )
        self.history_start_entry.pack(side="left", padx=5)
        
        # End date
        end_label = ctk.CTkLabel(
            date_frame,
            text="Bitiş Tarihi (YYYY-MM-DD):",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        end_label.pack(side="left", padx=10)
        
        self.history_end_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="2024-01-31",
            width=120
        )
        self.history_end_entry.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            date_frame,
            text="🔍 Ara",
            command=self._search_history,
            width=80
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Quick presets
        preset_frame = ctk.CTkFrame(self.tab_history)
        preset_frame.pack(pady=10, padx=20, fill="x")
        
        preset_label = ctk.CTkLabel(
            preset_frame,
            text="Hızlı Seçimler:",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        preset_label.pack(side="left", padx=10)
        
        today_btn = ctk.CTkButton(
            preset_frame,
            text="Bugün",
            command=lambda: self._set_history_range("today"),
            width=70
        )
        today_btn.pack(side="left", padx=3)
        
        week_btn = ctk.CTkButton(
            preset_frame,
            text="Geçen Hafta",
            command=lambda: self._set_history_range("week"),
            width=70
        )
        week_btn.pack(side="left", padx=3)
        
        month_btn = ctk.CTkButton(
            preset_frame,
            text="Geçen Ay",
            command=lambda: self._set_history_range("month"),
            width=70
        )
        month_btn.pack(side="left", padx=3)
        
        all_btn = ctk.CTkButton(
            preset_frame,
            text="Tümü",
            command=lambda: self._set_history_range("all"),
            width=70
        )
        all_btn.pack(side="left", padx=3)
        
        # Results frame
        self.history_results_frame = ctk.CTkScrollableFrame(
            self.tab_history,
            width=700,
            height=400
        )
        self.history_results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initial load
        self._search_history()
    
    def _set_history_range(self, range_type: str):
        """Set history date range using presets."""
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        
        if range_type == "today":
            start = today
            end = today
        elif range_type == "week":
            start = today - timedelta(days=7)
            end = today
        elif range_type == "month":
            start = today - timedelta(days=30)
            end = today
        else:  # all
            start = today - timedelta(days=365)
            end = today
        
        self.history_start_entry.delete(0, "end")
        self.history_start_entry.insert(0, start.strftime("%Y-%m-%d"))
        
        self.history_end_entry.delete(0, "end")
        self.history_end_entry.insert(0, end.strftime("%Y-%m-%d"))
        
        self._search_history()
    
    def _search_history(self):
        """Search and display history for the specified date range."""
        # Clear results
        for widget in self.history_results_frame.winfo_children():
            widget.destroy()
        
        try:
            start_str = self.history_start_entry.get().strip()
            end_str = self.history_end_entry.get().strip()
            
            if not start_str or not end_str:
                label = ctk.CTkLabel(
                    self.history_results_frame,
                    text="Lütfen başlangıç ve bitiş tarihlerini girin",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                label.pack(pady=50)
                return
            
            # Get stats for date range
            stats = self.db_manager.get_stats_for_date_range(start_str, end_str)
            
            if not stats:
                label = ctk.CTkLabel(
                    self.history_results_frame,
                    text=f"{start_str} ile {end_str} arasında veri bulunamadı",
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                label.pack(pady=50)
                return
            
            # Header
            header = ctk.CTkLabel(
                self.history_results_frame,
                text=f"{start_str} ile {end_str} Arasındaki İstatistikler",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#FFD700"
            )
            header.pack(anchor="w", padx=10, pady=10)
            
            # Total time
            total_seconds = sum(stats.values())
            total_hours = total_seconds // 3600
            total_minutes = (total_seconds % 3600) // 60
            
            total_label = ctk.CTkLabel(
                self.history_results_frame,
                text=f"Toplam Kullanım: {total_hours}s {total_minutes}d",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            total_label.pack(anchor="w", padx=20, pady=5)
            
            # Separator
            separator = ctk.CTkLabel(
                self.history_results_frame,
                text="─" * 60,
                text_color="#444444"
            )
            separator.pack(pady=5)
            
            # Apps list
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            for app_name, duration_seconds in sorted_stats:
                hours = duration_seconds // 3600
                minutes = (duration_seconds % 3600) // 60
                secs = duration_seconds % 60
                
                if hours > 0:
                    time_str = f"{hours}s {minutes}d {secs}sn"
                elif minutes > 0:
                    time_str = f"{minutes}d {secs}sn"
                else:
                    time_str = f"{secs}sn"
                
                app_frame = ctk.CTkFrame(self.history_results_frame)
                app_frame.pack(fill="x", padx=10, pady=5)
                
                name_label = ctk.CTkLabel(
                    app_frame,
                    text=app_name,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    anchor="w"
                )
                name_label.pack(side="left", padx=15, pady=10)
                
                time_label = ctk.CTkLabel(
                    app_frame,
                    text=time_str,
                    font=ctk.CTkFont(size=11),
                    text_color="#87CEEB"
                )
                time_label.pack(side="right", padx=20, pady=10)
            
        except ValueError as e:
            error_label = ctk.CTkLabel(
                self.history_results_frame,
                text=f"Tarih formatı hata: {str(e)}\nLütfen YYYY-MM-DD formatını kullanın",
                font=ctk.CTkFont(size=11),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.history_results_frame,
                text=f"Hata: {str(e)}",
                font=ctk.CTkFont(size=11),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
            print(f"[TimeTraceUI] History search error: {e}")
    
    def _setup_watchlist_tab(self):
        """Setup the Watchlist tab."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_watchlist,
            text="Uygulama İzleme Listesi",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            self.tab_watchlist,
            text="İzlemek istediğiniz uygulamaları ekleyin (örn: chrome.exe, valorant.exe, notepad.exe)",
            font=ctk.CTkFont(size=12)
        )
        instructions.pack(pady=5)
        
        # Popular apps section
        popular_frame = ctk.CTkFrame(self.tab_watchlist)
        popular_frame.pack(pady=10, padx=20, fill="x")
        
        popular_label = ctk.CTkLabel(
            popular_frame,
            text="⭐ Popüler Uygulamalar (Hızlı Ekle):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        popular_label.pack(pady=5, anchor="w")
        
        # Popular apps buttons frame
        buttons_frame = ctk.CTkScrollableFrame(
            popular_frame,
            width=600,
            height=60,
            orientation="horizontal"
        )
        buttons_frame.pack(pady=5, padx=10, fill="x")
        
        # Popüler uygulamalar listesi
        popular_apps = [
            ("Chrome", "chrome.exe"),
            ("Firefox", "firefox.exe"),
            ("Discord", "discord.exe"),
            ("VS Code", "code.exe"),
            ("Valorant", "valorant.exe"),
            ("Notepad++", "notepad++.exe"),
        ]
        
        for app_label, app_exe in popular_apps:
            btn = ctk.CTkButton(
                buttons_frame,
                text=f"+ {app_label}",
                command=lambda exe=app_exe: self._quick_add_app(exe),
                width=80,
                height=30
            )
            btn.pack(side="left", padx=5, pady=5)
        
        # Running apps section
        running_apps_frame = ctk.CTkFrame(self.tab_watchlist)
        running_apps_frame.pack(pady=10, padx=20, fill="x")
        
        running_label = ctk.CTkLabel(
            running_apps_frame,
            text="🔍 Şu anda çalışan uygulamalar:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        running_label.pack(pady=5)
        
        # Listbox for running apps
        self.running_apps_listbox = ctk.CTkTextbox(
            running_apps_frame,
            height=100,
            width=600
        )
        self.running_apps_listbox.pack(pady=5, padx=10)
        
        # Refresh running apps button
        refresh_running_btn = ctk.CTkButton(
            running_apps_frame,
            text="🔄 Çalışan Uygulamaları Yenile",
            command=self._refresh_running_apps,
            width=200
        )
        refresh_running_btn.pack(pady=5)
        
        # Add app frame
        add_frame = ctk.CTkFrame(self.tab_watchlist)
        add_frame.pack(pady=20, padx=20, fill="x")
        
        add_label = ctk.CTkLabel(
            add_frame,
            text="➕ Yeni uygulama ekle:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        add_label.pack(pady=5)
        
        # Entry for new app
        self.app_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text=".exe dosya adını girin (örn: notepad.exe)",
            width=400
        )
        self.app_entry.pack(side="left", padx=10, pady=10)
        
        # Add button
        add_btn = ctk.CTkButton(
            add_frame,
            text="✓ İzleme Listesine Ekle",
            command=self._add_app_to_watchlist,
            width=150
        )
        add_btn.pack(side="left", padx=10, pady=10)
        
        # Watchlist title
        watchlist_title = ctk.CTkLabel(
            self.tab_watchlist,
            text="📋 İzlenen Uygulamalar:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        watchlist_title.pack(pady=10)
        
        # Scrollable frame for watchlist
        self.watchlist_frame = ctk.CTkScrollableFrame(
            self.tab_watchlist,
            width=700,
            height=200
        )
        self.watchlist_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initial load of watchlist and running apps
        self._refresh_watchlist()
        self._refresh_running_apps()
    
    def _refresh_dashboard(self):
        """Refresh the dashboard with latest statistics based on selected period."""
        # Force save any pending time
        self.monitor.force_save()
        
        # Clear existing widgets
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        period = self.period_var.get() if hasattr(self, 'period_var') else "today"
        
        try:
            # Get stats based on period
            if period == "today":
                stats = self.db_manager.get_today_stats()
                period_text = "Bugün"
            elif period == "week":
                stats = self.db_manager.get_week_stats()
                period_text = "Son 7 Gün"
            elif period == "month":
                stats = self.db_manager.get_month_stats()
                period_text = "Son 30 Gün"
            else:
                stats = self.db_manager.get_today_stats()
                period_text = "Bugün"
            
            # Period header
            period_header = ctk.CTkLabel(
                self.stats_frame,
                text=f"{period_text} İstatistikleri",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#FFD700"
            )
            period_header.pack(anchor="w", padx=10, pady=(10, 5))
            
            if not stats:
                no_data_label = ctk.CTkLabel(
                    self.stats_frame,
                    text=f"{period_text} için henüz veri yok.\n'⚙️ Watchlist' sekmesinden uygulama ekleyin ve kullanmaya başlayın!",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                no_data_label.pack(pady=50)
                return
            
            # Calculate total time
            total_seconds = sum(stats.values())
            
            # Total time display
            total_hours = total_seconds // 3600
            total_minutes = (total_seconds % 3600) // 60
            total_secs = total_seconds % 60
            
            total_label = ctk.CTkLabel(
                self.stats_frame,
                text=f"Toplam: {total_hours}s {total_minutes}d {total_secs}sn",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#00FF00"
            )
            total_label.pack(anchor="w", padx=20, pady=5)
            
            # Separator
            separator = ctk.CTkLabel(
                self.stats_frame,
                text="─" * 60,
                text_color="#444444"
            )
            separator.pack(pady=5)
            
            # Sort stats by duration (descending)
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            # Display each app
            for app_name, duration_seconds in sorted_stats:
                self._create_app_stat_widget(app_name, duration_seconds)
            
            print(f"[TimeTraceUI] Dashboard refreshed ({period_text})")
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.stats_frame,
                text=f"Hata: {str(e)}",
                font=ctk.CTkFont(size=12),
                text_color="#FF6B6B"
            )
            error_label.pack(pady=20)
            print(f"[TimeTraceUI] Dashboard error: {e}")
    
    def _create_app_stat_widget(self, app_name: str, duration_seconds: int):
        """
        Create a widget displaying app usage statistics.
        
        Args:
            app_name: Name of the application
            duration_seconds: Total duration in seconds
        """
        # Convert seconds to readable format
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        
        if hours > 0:
            time_str = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"
        
        # Create frame for this app
        app_frame = ctk.CTkFrame(self.stats_frame)
        app_frame.pack(fill="x", padx=10, pady=5)
        
        # App name label
        name_label = ctk.CTkLabel(
            app_frame,
            text=app_name,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        name_label.pack(side="left", padx=20, pady=15)
        
        # Duration label
        duration_label = ctk.CTkLabel(
            app_frame,
            text=time_str,
            font=ctk.CTkFont(size=16),
            anchor="e"
        )
        duration_label.pack(side="right", padx=20, pady=15)
        
        # Progress bar (visual representation)
        # Calculate percentage based on max duration in stats
        max_duration = max(self.db_manager.get_today_stats().values())
        progress = duration_seconds / max_duration if max_duration > 0 else 0
        
        progress_bar = ctk.CTkProgressBar(
            app_frame,
            width=300
        )
        progress_bar.set(progress)
        progress_bar.pack(side="right", padx=20, pady=15)
    
    def _refresh_watchlist(self):
        """Refresh the watchlist display."""
        # Clear existing widgets
        for widget in self.watchlist_frame.winfo_children():
            widget.destroy()
        
        # Get current watchlist
        watchlist = self.config_manager.get_watchlist()
        
        if not watchlist:
            no_apps_label = ctk.CTkLabel(
                self.watchlist_frame,
                text="İzleme listesinde uygulama yok.\nYukarıdan uygulama ekleyerek izlemeye başlayın!",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_apps_label.pack(pady=50)
            return
        
        # Display each app in watchlist
        for app_name in watchlist:
            self._create_watchlist_item(app_name)
        
        print("[TimeTraceUI] Watchlist refreshed")
    
    def _refresh_running_apps(self):
        """Refresh the list of currently running applications with categories."""
        import psutil
        
        # Clear textbox
        self.running_apps_listbox.delete("1.0", "end")
        
        try:
            # Get all running processes
            running_processes = set()
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name']
                    if proc_name and proc_name.lower().endswith('.exe'):
                        # Sistem processlerini filtrele
                        if proc_name.lower() not in SYSTEM_PROCESSES:
                            running_processes.add(proc_name.lower())
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Uygulamaları kategorize et
            categorized_apps = self._categorize_apps(running_processes)
            
            if any(apps for apps in categorized_apps.values()):
                display_text = "📱 Çalışan Uygulamalar (Kategorilere Göre):\n\n"
                
                for category, apps in categorized_apps.items():
                    if apps:
                        display_text += f"{category}\n"
                        for app in sorted(apps):
                            display_text += f"  • {app}\n"
                        display_text += "\n"
                
                self.running_apps_listbox.insert("1.0", display_text)
            else:
                self.running_apps_listbox.insert("1.0", "Çalışan normal uygulama bulunamadı.\n(Sistem hizmetleri gösterilmemiştir)")
            
        except Exception as e:
            self.running_apps_listbox.insert("1.0", f"Hata: {e}")
        
        print("[TimeTraceUI] Running apps refreshed")
    
    def _categorize_apps(self, running_apps: set) -> Dict[str, List[str]]:
        """
        Kategorize the running applications.
        
        Args:
            running_apps: Set of running application names
            
        Returns:
            Dictionary with categories as keys and lists of apps as values
        """
        categorized = {}
        
        # Tüm kategorileri başlat
        for category in APP_CATEGORIES.keys():
            categorized[category] = []
        
        # Uygulamaları kategorilere ata
        for app in running_apps:
            found = False
            for category, apps in APP_CATEGORIES.items():
                if app in apps:
                    categorized[category].append(app)
                    found = True
                    break
            
            # Kategoriye ait değilse "Diğer" kategorisine ekle
            if not found:
                categorized["📊 Diğer Uygulamalar"].append(app)
        
        return categorized
    
    def _setup_advanced_settings_tab(self):
        """Setup the Advanced Settings tab for system configuration."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_advanced_settings,
            text="Gelişmiş Ayarlar",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Scrollable frame
        settings_frame = ctk.CTkScrollableFrame(
            self.tab_advanced_settings,
            width=600,
            height=400
        )
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Check Interval Setting
        check_frame = ctk.CTkFrame(settings_frame)
        check_frame.pack(fill="x", padx=10, pady=15)
        
        check_label = ctk.CTkLabel(
            check_frame,
            text="⏱️ Kontrol Aralığı (saniye):",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        check_label.pack(side="left", padx=10)
        
        current_check = self.config_manager.get_setting("check_interval_seconds") or 5
        self.check_interval_var = ctk.StringVar(value=str(current_check))
        
        self.check_interval_entry = ctk.CTkEntry(
            check_frame,
            textvariable=self.check_interval_var,
            width=100
        )
        self.check_interval_entry.pack(side="left", padx=10)
        
        check_info = ctk.CTkLabel(
            check_frame,
            text="Uygulamaların kontrol edilme sıklığı. Düşük değer = Daha fazla CPU kullanımı",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        check_info.pack(side="left", padx=10)
        
        # Save Interval Setting
        save_frame = ctk.CTkFrame(settings_frame)
        save_frame.pack(fill="x", padx=10, pady=15)
        
        save_label = ctk.CTkLabel(
            save_frame,
            text="💾 Kaydetme Aralığı (saniye):",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        save_label.pack(side="left", padx=10)
        
        current_save = self.config_manager.get_setting("save_interval_seconds") or 60
        self.save_interval_var = ctk.StringVar(value=str(current_save))
        
        self.save_interval_entry = ctk.CTkEntry(
            save_frame,
            textvariable=self.save_interval_var,
            width=100
        )
        self.save_interval_entry.pack(side="left", padx=10)
        
        save_info = ctk.CTkLabel(
            save_frame,
            text="Verilerin veritabanına kaydedilme sıklığı",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        save_info.pack(side="left", padx=10)
        
        # Data Retention Setting
        retention_frame = ctk.CTkFrame(settings_frame)
        retention_frame.pack(fill="x", padx=10, pady=15)
        
        retention_label = ctk.CTkLabel(
            retention_frame,
            text="🗑️ Veri Saklama Süresi (gün):",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        retention_label.pack(side="left", padx=10)
        
        self.retention_var = ctk.StringVar(value="90")
        
        self.retention_entry = ctk.CTkEntry(
            retention_frame,
            textvariable=self.retention_var,
            width=100
        )
        self.retention_entry.pack(side="left", padx=10)
        
        retention_info = ctk.CTkLabel(
            retention_frame,
            text="Belirtilen günden eski kayıtlar otomatik silinir",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        retention_info.pack(side="left", padx=10)
        
        # Minimize to tray Setting
        tray_frame = ctk.CTkFrame(settings_frame)
        tray_frame.pack(fill="x", padx=10, pady=15)
        
        tray_label = ctk.CTkLabel(
            tray_frame,
            text="📌 Sistem Tray'a Küçült:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        tray_label.pack(side="left", padx=10)
        
        current_tray = self.config_manager.get_setting("minimize_to_tray")
        self.minimize_to_tray_var = ctk.BooleanVar(value=current_tray if current_tray is not None else True)
        
        tray_switch = ctk.CTkSwitch(
            tray_frame,
            text="Aktif",
            variable=self.minimize_to_tray_var,
            onvalue=True,
            offvalue=False
        )
        tray_switch.pack(side="left", padx=10)
        
        tray_info = ctk.CTkLabel(
            tray_frame,
            text="Pencereyi kapatırken sistem tray'a küçültülüp açık kalır",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        tray_info.pack(side="left", padx=10)

        # Run at Startup Setting
        startup_frame = ctk.CTkFrame(settings_frame)
        startup_frame.pack(fill="x", padx=10, pady=15)

        startup_label = ctk.CTkLabel(
            startup_frame,
            text="🚀 Windows Açılışında Çalıştır:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        startup_label.pack(side="left", padx=10)

        current_startup = self.config_manager.get_setting("run_at_startup")
        self.run_at_startup_var = ctk.BooleanVar(value=current_startup if current_startup is not None else False)

        startup_switch = ctk.CTkSwitch(
            startup_frame,
            text="Aktif",
            variable=self.run_at_startup_var,
            onvalue=True,
            offvalue=False
        )
        startup_switch.pack(side="left", padx=10)

        startup_info = ctk.CTkLabel(
            startup_frame,
            text="Başlangıç klasörüne kısayol ekler/kaldırır",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        startup_info.pack(side="left", padx=10)
        
        # Separator
        separator = ctk.CTkLabel(
            settings_frame,
            text="─" * 80,
            text_color="#444444"
        )
        separator.pack(pady=20)
        
        # Database management section
        db_label = ctk.CTkLabel(
            settings_frame,
            text="📊 Veritabanı Yönetimi",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        db_label.pack(anchor="w", padx=10, pady=10)
        
        # Export options
        export_opts_frame = ctk.CTkFrame(settings_frame)
        export_opts_frame.pack(fill="x", padx=10, pady=10)
        
        export_dir_label = ctk.CTkLabel(
            export_opts_frame,
            text="📁 Dışa Aktarım Klasörü:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        export_dir_label.pack(side="left", padx=10)
        
        # Load export directory from config
        current_export_dir = self.config_manager.get_setting("export_directory") or ""
        self.export_dir_var = ctk.StringVar(value=current_export_dir)
        
        export_dir_entry = ctk.CTkEntry(
            export_opts_frame,
            textvariable=self.export_dir_var,
            width=320
        )
        export_dir_entry.pack(side="left", padx=5)
        
        def _choose_export_dir():
            try:
                from tkinter import filedialog
                # Use underlying tkinter dialog for directory selection
                path = filedialog.askdirectory()
                if path:
                    self.export_dir_var.set(path)
                    self.config_manager.set_setting("export_directory", path)
            except Exception as e:
                print(f"[TimeTraceUI] Export dir choose error: {e}")
        
        export_dir_btn = ctk.CTkButton(
            export_opts_frame,
            text="Seç",
            command=_choose_export_dir,
            width=60
        )
        export_dir_btn.pack(side="left", padx=5)
        
        # Export range presets
        presets_frame = ctk.CTkFrame(settings_frame)
        presets_frame.pack(fill="x", padx=10, pady=10)
        
        presets_label = ctk.CTkLabel(
            presets_frame,
            text="🗓️ Dışa Aktarım Aralığı:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        presets_label.pack(side="left", padx=10)
        
        self.export_range_var = ctk.StringVar(value=self.config_manager.get_setting("export_range") or "month")
        
        def _set_export_range(val: str):
            self.export_range_var.set(val)
            self.config_manager.set_setting("export_range", val)
        
        for label, val in [("Bugün","today"),("7 Gün","week"),("30 Gün","month"),("Özel","custom")]:
            btn = ctk.CTkButton(
                presets_frame,
                text=label,
                command=lambda v=val: _set_export_range(v),
                width=70
            )
            btn.pack(side="left", padx=4)
        
        # Clear old data button
        clear_btn = ctk.CTkButton(
            settings_frame,
            text="🗑️ Eski Verileri Temizle",
            command=self._clear_old_data,
            width=200
        )
        clear_btn.pack(padx=10, pady=5)
        
        # Export data button
        export_btn = ctk.CTkButton(
            settings_frame,
            text="📤 Verileri Dışa Aktar (CSV)",
            command=self._export_data,
            width=200
        )
        export_btn.pack(padx=10, pady=5)
        
        # Separator
        separator2 = ctk.CTkLabel(
            settings_frame,
            text="─" * 80,
            text_color="#444444"
        )
        separator2.pack(pady=20)
        
        # Save and Reset buttons
        button_frame = ctk.CTkFrame(self.tab_advanced_settings)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Varsayılana Sıfırla",
            command=self._reset_advanced_settings,
            width=150
        )
        reset_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Ayarları Kaydet",
            command=self._save_advanced_settings,
            width=150
        )
        save_btn.pack(side="left", padx=5)

        # Notifications settings (Quiet Hours & Snooze)
        notif_frame = ctk.CTkFrame(settings_frame)
        notif_frame.pack(fill="x", padx=10, pady=10)

        notif_label = ctk.CTkLabel(
            notif_frame,
            text="🔔 Bildirim Ayarları",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        notif_label.pack(anchor="w", padx=10)

        qh_frame = ctk.CTkFrame(notif_frame)
        qh_frame.pack(fill="x", padx=10, pady=5)

        qh_label = ctk.CTkLabel(
            qh_frame,
            text="Sessiz Saatler (HH:MM)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        qh_label.pack(side="left", padx=10)

        self.qh_start_var = ctk.StringVar(value=self.config_manager.get_setting("quiet_hours_start") or "22:00")
        self.qh_end_var = ctk.StringVar(value=self.config_manager.get_setting("quiet_hours_end") or "07:00")

        qh_start_entry = ctk.CTkEntry(qh_frame, textvariable=self.qh_start_var, width=80)
        qh_start_entry.pack(side="left", padx=5)
        qh_end_entry = ctk.CTkEntry(qh_frame, textvariable=self.qh_end_var, width=80)
        qh_end_entry.pack(side="left", padx=5)

        snooze_frame = ctk.CTkFrame(notif_frame)
        snooze_frame.pack(fill="x", padx=10, pady=5)

        snooze_label = ctk.CTkLabel(
            snooze_frame,
            text="Snooze (dakika)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        snooze_label.pack(side="left", padx=10)

        self.snooze_var = ctk.StringVar(value=str(self.config_manager.get_setting("notification_snooze_minutes") or 0))
        snooze_entry = ctk.CTkEntry(snooze_frame, textvariable=self.snooze_var, width=80)
        snooze_entry.pack(side="left", padx=5)
    
    def _save_advanced_settings(self):
        """Save advanced settings."""
        try:
            # Save numeric settings
            check_interval = int(self.check_interval_var.get())
            save_interval = int(self.save_interval_var.get())
            
            if check_interval < 1 or save_interval < 1:
                raise ValueError("Aralıklar 1 saniyeden az olamaz")
            
            self.config_manager.set_setting("check_interval_seconds", check_interval)
            self.config_manager.set_setting("save_interval_seconds", save_interval)
            self.config_manager.set_setting("minimize_to_tray", self.minimize_to_tray_var.get())
            self.config_manager.set_setting("run_at_startup", self.run_at_startup_var.get())

            # Save notifications settings
            self.config_manager.set_setting("quiet_hours_start", self.qh_start_var.get())
            self.config_manager.set_setting("quiet_hours_end", self.qh_end_var.get())
            self.config_manager.set_setting("notification_snooze_minutes", int(self.snooze_var.get()))
            
            print("[TimeTraceUI] Advanced settings saved")

            # Apply startup shortcut
            try:
                self._apply_startup_shortcut(self.run_at_startup_var.get())
            except Exception as e:
                print(f"[TimeTraceUI] Startup shortcut error: {e}")
            
            # Show success message
            message = ctk.CTkLabel(
                self.tab_advanced_settings,
                text="✓ Ayarlar başarıyla kaydedildi!",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            message.pack(pady=10)
            self.root.after(3000, message.destroy)
            
        except ValueError as e:
            print(f"[TimeTraceUI] Error saving settings: {e}")
    
    def _reset_advanced_settings(self):
        """Reset advanced settings to defaults."""
        self.check_interval_var.set("5")
        self.save_interval_var.set("60")
        self.minimize_to_tray_var.set(True)
        self.qh_start_var.set("22:00")
        self.qh_end_var.set("07:00")
        self.snooze_var.set("0")
        print("[TimeTraceUI] Advanced settings reset to defaults")

    def _apply_startup_shortcut(self, enable: bool):
        """Create or remove a Startup shortcut based on toggle."""
        startup_dir = os.path.join(os.environ.get('AppData', ''),
                                   'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        if not startup_dir:
            raise RuntimeError("Startup directory not found")
        shortcut_path = os.path.join(startup_dir, 'TimeTrace.lnk')

        # Determine pythonw path
        exe = sys.executable
        if exe.lower().endswith('python.exe'):
            pythonw = exe[:-10] + 'pythonw.exe'
        else:
            pythonw = exe  # if already pythonw or frozen exe

        target_script = os.path.abspath(os.path.join(os.getcwd(), 'main.py'))

        if enable:
            try:
                import win32com.client  # requires pywin32
                shell = win32com.client.Dispatch('WScript.Shell')
                shortcut = shell.CreateShortcut(shortcut_path)
                shortcut.TargetPath = pythonw
                shortcut.Arguments = f'"{target_script}"'
                shortcut.WorkingDirectory = os.getcwd()
                icon_path = os.path.abspath(os.path.join(os.getcwd(), 'icon.ico'))
                if os.path.exists(icon_path):
                    shortcut.IconLocation = icon_path
                shortcut.Description = 'Launch TimeTrace on startup'
                shortcut.Save()
                print(f"[TimeTraceUI] Startup shortcut created at {shortcut_path}")
            except ImportError:
                raise RuntimeError("pywin32 not installed; cannot create startup shortcut")
        else:
            try:
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)
                    print("[TimeTraceUI] Startup shortcut removed")
            except Exception as e:
                print(f"[TimeTraceUI] Failed to remove startup shortcut: {e}")
    
    def _clear_old_data(self):
        """Clear data older than retention period."""
        try:
            retention_days = int(self.retention_var.get())
            self.db_manager.clear_old_data(retention_days)
            
            # Show success message
            message = ctk.CTkLabel(
                self.tab_advanced_settings,
                text=f"✓ {retention_days} günden eski veriler silindi!",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            message.pack(pady=10)
            self.root.after(3000, message.destroy)
            
            print(f"[TimeTraceUI] Old data cleared (retention: {retention_days} days)")
            
        except Exception as e:
            print(f"[TimeTraceUI] Error clearing old data: {e}")
    
    def _export_data(self):
        """Export usage data to CSV file."""
        import csv
        from datetime import datetime
        import os
        
        try:
            export_dir = self.export_dir_var.get().strip() if hasattr(self, 'export_dir_var') else ""
            if export_dir and not os.path.isdir(export_dir):
                os.makedirs(export_dir, exist_ok=True)
            filename = f"timetraces_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            abs_path = os.path.abspath(os.path.join(export_dir or "", filename))
            
            # Determine export range
            range_sel = self.export_range_var.get() if hasattr(self, 'export_range_var') else "month"
            if range_sel == "today":
                stats = self.db_manager.get_today_stats()
            elif range_sel == "week":
                stats = self.db_manager.get_week_stats()
            else:
                stats = self.db_manager.get_month_stats()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Uygulama", "Saat"])
                
                for app_name, seconds in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                    hours = seconds / 3600
                    writer.writerow([app_name, f"{hours:.2f}"])
            
            # Show success message with full path
            message = ctk.CTkLabel(
                self.tab_advanced_settings,
                text=f"✓ Veriler dışa aktarıldı:\n{abs_path}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#00FF00"
            )
            message.pack(pady=10)
            # Keep message visible longer for user to note path
            self.root.after(7000, message.destroy)
            
            # Provide button to open the folder in Explorer
            def _open_export_folder():
                try:
                    os.startfile(os.path.dirname(abs_path))
                except Exception as e:
                    print(f"[TimeTraceUI] Error opening folder: {e}")
            
            open_btn = ctk.CTkButton(
                self.tab_advanced_settings,
                text="📂 Klasörü Aç",
                command=_open_export_folder,
                width=140
            )
            open_btn.pack(pady=5)
            # Auto-remove the button after some time
            self.root.after(15000, open_btn.destroy)
            
            print(f"[TimeTraceUI] Data exported to {abs_path}")
            
        except Exception as e:
            print(f"[TimeTraceUI] Error exporting data: {e}")
    
    def _setup_help_tab(self):
        """Setup the Help/Tutorial tab."""
        # Create scrollable frame for help content
        help_frame = ctk.CTkScrollableFrame(
            self.tab_help,
            width=750,
            height=550
        )
        help_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            help_frame,
            text="⏱️ TimeTrace Nasıl Kullanılır?",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # Step 1
        step1_title = ctk.CTkLabel(
            help_frame,
            text="1️⃣ Uygulama Ekleyin",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        step1_title.pack(fill="x", padx=20, pady=(20, 5))
        
        step1_text = ctk.CTkLabel(
            help_frame,
            text="• '⚙️ Watchlist' sekmesine gidin\n"
                 "• 'Çalışan Uygulamalar' listesine bakın ve izlemek istediğiniz uygulamayı bulun\n"
                 "• Uygulama adını kopyalayıp metin kutusuna yapıştırın\n"
                 "• Veya direkt .exe adını yazın (örn: valorant.exe, chrome.exe)\n"
                 "• '✓ İzleme Listesine Ekle' butonuna tıklayın",
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left"
        )
        step1_text.pack(fill="x", padx=40, pady=5)
        
        # Step 2
        step2_title = ctk.CTkLabel(
            help_frame,
            text="2️⃣ İzleme Otomatik Başlar",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        step2_title.pack(fill="x", padx=20, pady=(20, 5))
        
        step2_text = ctk.CTkLabel(
            help_frame,
            text="• Program arka planda sürekli çalışır\n"
                 "• İzleme listesindeki uygulamalar açık olduğunda süre sayar\n"
                 "• Her 5 saniyede bir kontrol eder\n"
                 "• Her 60 saniyede bir veritabanına kaydeder\n"
                 "• Bilgisayarınızı kapatırsanız bile veriler kaybolmaz",
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left"
        )
        step2_text.pack(fill="x", padx=40, pady=5)
        
        # Step 3
        step3_title = ctk.CTkLabel(
            help_frame,
            text="3️⃣ İstatistikleri Görüntüleyin",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        step3_title.pack(fill="x", padx=20, pady=(20, 5))
        
        step3_text = ctk.CTkLabel(
            help_frame,
            text="• '📊 Dashboard' sekmesine gidin\n"
                 "• Bugün kullandığınız tüm uygulamaları ve sürelerini görün\n"
                 "• '🔄 Refresh Stats' ile güncel verileri görün\n"
                 "• Süreler otomatik olarak saat, dakika, saniye formatında gösterilir",
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left"
        )
        step3_text.pack(fill="x", padx=40, pady=5)
        
        # Step 4
        step4_title = ctk.CTkLabel(
            help_frame,
            text="4️⃣ Sistem Tepsisi (System Tray)",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        step4_title.pack(fill="x", padx=20, pady=(20, 5))
        
        step4_text = ctk.CTkLabel(
            help_frame,
            text="• Pencereyi kapattığınızda program tamamen kapanmaz\n"
                 "• Sistem tepsisinde (saat yanında) küçük bir ikon olarak kalır\n"
                 "• İkona sağ tıklayarak:\n"
                 "  - Pencereyi göster/gizle\n"
                 "  - Programı tamamen kapat\n"
                 "• Program arka planda çalışmaya devam eder",
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left"
        )
        step4_text.pack(fill="x", padx=40, pady=5)
        
        # Tips section
        tips_title = ctk.CTkLabel(
            help_frame,
            text="💡 İpuçları",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        tips_title.pack(fill="x", padx=20, pady=(30, 5))
        
        tips_text = ctk.CTkLabel(
            help_frame,
            text="• Uygulama adının TAM .exe adını kullanın (chrome.exe ✓, chrome ✗)\n"
                 "• Bazı oyunlar farklı .exe adları kullanabilir (örn: VALORANT-Win64-Shipping.exe)\n"
                 "• Program minimum CPU kullanır, performansınızı etkilemez\n"
                 "• Veriler 'tracker.db' dosyasında saklanır\n"
                 "• İstemediğiniz uygulamaları '🗑️ Remove' ile silebilirsiniz",
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left",
            text_color="yellow"
        )
        tips_text.pack(fill="x", padx=40, pady=5)
        
        # Common apps section
        common_title = ctk.CTkLabel(
            help_frame,
            text="📱 Popüler Uygulamalar",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        common_title.pack(fill="x", padx=20, pady=(30, 5))
        
        common_text = ctk.CTkLabel(
            help_frame,
            text="Tarayıcılar: chrome.exe, firefox.exe, msedge.exe, brave.exe, opera.exe\n"
                 "Oyunlar: valorant.exe, LeagueClient.exe, RiotClientServices.exe\n"
                 "Mesajlaşma: discord.exe, whatsapp.exe, telegram.exe, slack.exe\n"
                 "Kodlama: code.exe (VS Code), pycharm64.exe, notepad++.exe\n"
                 "Ofis: WINWORD.EXE (Word), EXCEL.EXE, POWERPNT.EXE\n"
                 "Medya: spotify.exe, vlc.exe, obs64.exe",
            font=ctk.CTkFont(size=13),
            anchor="w",
            justify="left",
            text_color="lightblue"
        )
        common_text.pack(fill="x", padx=40, pady=5)
        
        print("[TimeTraceUI] Help tab created")
    
    def _create_watchlist_item(self, app_name: str):
        """
        Create a widget for a watchlist item.
        
        Args:
            app_name: Name of the application
        """
        # Create frame for this app
        item_frame = ctk.CTkFrame(self.watchlist_frame)
        item_frame.pack(fill="x", padx=10, pady=5)
        
        # App name label
        name_label = ctk.CTkLabel(
            item_frame,
            text=app_name,
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        name_label.pack(side="left", padx=20, pady=10)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            item_frame,
            text="🗑️ Remove",
            command=lambda: self._remove_app_from_watchlist(app_name),
            width=100,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.pack(side="right", padx=20, pady=10)
    
    def _add_app_to_watchlist(self):
        """Add a new app to the watchlist."""
        app_name = self.app_entry.get().strip()
        
        if not app_name:
            self._show_error("Lütfen bir uygulama adı girin")
            return
        
        # Ensure it ends with .exe (for Windows)
        if not app_name.lower().endswith('.exe'):
            app_name += '.exe'
        
        # Add to config
        success = self.config_manager.add_app(app_name)
        
        if success:
            self._show_success(f"{app_name} izleme listesine eklendi ✓")
            self.app_entry.delete(0, 'end')
            self._refresh_watchlist()
        else:
            self._show_error(f"{app_name} zaten izleme listesinde")
    
    def _quick_add_app(self, app_name: str):
        """
        Quickly add a popular app to watchlist.
        
        Args:
            app_name: Executable name to add
        """
        # Add to config
        success = self.config_manager.add_app(app_name)
        
        if success:
            self._show_success(f"{app_name} izleme listesine eklendi ✓")
            self._refresh_watchlist()
        else:
            self._show_error(f"{app_name} zaten izleme listesinde")
    
    def _remove_app_from_watchlist(self, app_name: str):
        """
        Remove an app from the watchlist.
        
        Args:
            app_name: Name of the app to remove
        """
        success = self.config_manager.remove_app(app_name)
        
        if success:
            self._show_success(f"{app_name} izleme listesinden kaldırıldı ✓")
            self._refresh_watchlist()
        else:
            self._show_error(f"{app_name} kaldırılamadı")
    
    def _show_success(self, message: str):
        """Show a success message (simple print for now)."""
        print(f"[SUCCESS] {message}")
        # In a production app, you could use a toast notification or dialog
    
    def _show_error(self, message: str):
        """Show an error message (simple print for now)."""
        print(f"[ERROR] {message}")
        # In a production app, you could use a dialog box
    
    def _on_window_close(self):
        """Handle window close event."""
        if self.on_close_callback:
            self.on_close_callback()
        else:
            self.root.destroy()
    
    def run(self):
        """Start the GUI main loop."""
        print("[TimeTraceUI] Starting GUI main loop")
        self.root.mainloop()
    
    def show(self):
        """Show the window (after being hidden)."""
        self.root.deiconify()
        print("[TimeTraceUI] Window shown")
    
    def hide(self):
        """Hide the window (minimize to tray)."""
        self.root.withdraw()
        print("[TimeTraceUI] Window hidden")
    
    def destroy(self):
        """Destroy the window completely."""
        self.root.destroy()
        print("[TimeTraceUI] Window destroyed")


# Testing the UI (standalone)
if __name__ == "__main__":
    from database_manager import DatabaseManager
    from config_manager import ConfigManager
    from monitor_service import AppMonitor
    
    # Create instances
    db = DatabaseManager("test_tracker.db")
    config = ConfigManager("test_settings.json")
    monitor = AppMonitor(db, config)
    
    # Start monitor
    monitor.start()
    
    # Create and run UI
    ui = TimeTraceUI(db, config, monitor)
    ui.run()
    
    # Cleanup
    monitor.stop()
    
    import os
    if os.path.exists("test_tracker.db"):
        os.remove("test_tracker.db")
    if os.path.exists("test_settings.json"):
        os.remove("test_settings.json")
