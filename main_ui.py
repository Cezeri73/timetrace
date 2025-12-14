"""
Main UI for TimeTrace Application
Modern GUI using CustomTkinter with tabbed interface
"""

import customtkinter as ctk
from typing import Callable, Dict, List
from database_manager import DatabaseManager
from config_manager import ConfigManager
from monitor_service import AppMonitor


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
                 monitor: AppMonitor, on_close_callback: Callable = None):
        """
        Initialize the TimeTrace UI.
        
        Args:
            db_manager: DatabaseManager instance
            config_manager: ConfigManager instance
            monitor: AppMonitor instance
            on_close_callback: Function to call when window is closed
        """
        self.db_manager = db_manager
        self.config_manager = config_manager
        self.monitor = monitor
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
        self.tab_settings = self.tabview.add("⚙️ Watchlist")
        self.tab_help = self.tabview.add("❓ Nasıl Kullanılır")
        
        # Setup each tab
        self._setup_dashboard_tab()
        self._setup_settings_tab()
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
    
    def _setup_settings_tab(self):
        """Setup the Watchlist/Settings tab."""
        # Title
        title_label = ctk.CTkLabel(
            self.tab_settings,
            text="Uygulama İzleme Listesi",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = ctk.CTkLabel(
            self.tab_settings,
            text="İzlemek istediğiniz uygulamaları ekleyin (örn: chrome.exe, valorant.exe, notepad.exe)",
            font=ctk.CTkFont(size=12)
        )
        instructions.pack(pady=5)
        
        # Popular apps section
        popular_frame = ctk.CTkFrame(self.tab_settings)
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
        running_apps_frame = ctk.CTkFrame(self.tab_settings)
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
        add_frame = ctk.CTkFrame(self.tab_settings)
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
            self.tab_settings,
            text="📋 İzlenen Uygulamalar:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        watchlist_title.pack(pady=10)
        
        # Scrollable frame for watchlist
        self.watchlist_frame = ctk.CTkScrollableFrame(
            self.tab_settings,
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
    ui = TimeAuditUI(db, config, monitor)
    ui.run()
    
    # Cleanup
    monitor.stop()
    
    import os
    if os.path.exists("test_tracker.db"):
        os.remove("test_tracker.db")
    if os.path.exists("test_settings.json"):
        os.remove("test_settings.json")
