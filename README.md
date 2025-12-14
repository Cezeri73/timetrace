<div align="center">

# ⏱️ TimeTrace

### Track Your Application Usage Effortlessly

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![GitHub Release](https://img.shields.io/badge/Release-v1.0.0-blue)](https://github.com/Cezeri73/timetrace/releases)
[![Download Script](https://img.shields.io/badge/Download-install.ps1-darkgreen)](https://raw.githubusercontent.com/Cezeri73/timetrace/main/install.ps1)

**[English](#english)** | **[Türkçe](#turkish)**

![TimeTrace Screenshot](https://via.placeholder.com/800x400/1f538d/ffffff?text=TimeTrace+Dashboard)

</div>

---

<a name="english"></a>
## 🌍 English

### 📖 Overview

**TimeTrace** is a modern, lightweight desktop application that helps you understand where your time goes. Track usage duration of specific applications you choose, visualize your daily statistics with charts, receive notifications, and improve your productivity.

### ✨ Features

- 🎯 **Selective Tracking** - Choose exactly which applications to monitor
- 📊 **Beautiful Dashboard** - View daily, weekly, and monthly statistics
- 📈 **Interactive Charts** - Visualize usage with multiple chart types
- 🔔 **Smart Notifications** - Get alerts when apps exceed time limits
- 📅 **History & Date Filters** - Browse and search usage history
- 🌙 **Modern Dark UI** - Sleek interface built with CustomTkinter
- 💾 **Persistent Storage** - SQLite database keeps all your history
- 🔔 **System Tray Support** - Minimize to tray and keep tracking in background
- ⚡ **Low Resource Usage** - Efficient monitoring with minimal CPU impact
- 🔍 **Running Apps Discovery** - See all running applications to easily add them
- 🛡️ **Error Resilient** - Gracefully handles access denied and process errors
- 🌐 **Bilingual Interface** - English and Turkish language support
- 📤 **CSV Export** - Export your usage data for analysis
- ⚙️ **Advanced Settings** - Customize intervals, retention, startup behavior

### 🚀 Quick Start

#### 📦 Installation Methods

**Choose one of the following methods:**

##### ⚡ Method 1: PowerShell Installer (Recommended)

**One-click installation via script:**

1. Download **[install.ps1](https://raw.githubusercontent.com/Cezeri73/timetrace/main/install.ps1)** (Right-click → Save As)
2. Run: `powershell -ExecutionPolicy Bypass -File install.ps1`
3. The script downloads latest code, creates venv, installs dependencies, and creates shortcuts
4. Launch from Desktop or Start Menu
5. No console window, runs with pythonw.exe

##### 🔧 Method 2: Manual Setup (For Development)

**Clone and run from source:**

```bash
# Clone the repository
git clone https://github.com/Cezeri73/timetrace.git
cd timetrace

# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application (no console window)
pythonw main.py
```

**Or visit:** [Releases Page](https://github.com/Cezeri73/timetrace/releases) for binary downloads (coming soon)

### 📱 Usage

1. **Add Applications**
   - Go to **⚙️ Watchlist** tab
   - Click **"🔄 Refresh Running Apps"** to see all running applications
   - Copy the .exe name and add it to your watchlist
   - Or manually enter app names (e.g., `chrome.exe`, `valorant.exe`)

2. **Monitor Usage**
   - The app runs in the background automatically
   - Checks every 5 seconds for running tracked apps
   - Saves data every 60 seconds to database

3. **View Statistics**
   - Open **📊 Dashboard** tab
   - Select period: Today, This Week, or This Month
   - Click **"🔄 Refresh Stats"** for latest data

4. **Visualize with Charts**
   - Go to **📈 Charts** tab
   - View Top Apps, Daily Trend, Category Distribution, and Week Comparison

5. **Set Notifications**
   - Open **🔔 Notifications** tab
   - Set time thresholds for each tracked app
   - Configure quiet hours and snooze duration

6. **Browse History**
   - Navigate to **📅 History** tab
   - Use date range filters or presets (Today, Last 7 Days, Last 30 Days)
   - Search and review past usage

7. **System Tray**
   - Closing the window minimizes to system tray
   - Right-click tray icon to show/hide or exit
   - App continues tracking in background

### 📂 Project Structure

```
TimeTrace/
├── main.py                  # Application entry point
├── main_ui.py              # GUI interface (CustomTkinter)
├── database_manager.py     # SQLite database operations
├── config_manager.py       # JSON configuration management
├── monitor_service.py      # Background monitoring service
├── notification_service.py # Notification handling service
├── build.ps1              # Build script for creating EXE
├── install.ps1            # PowerShell installation script
├── installer.nsi          # NSIS installer configuration
├── requirements.txt       # Python dependencies
├── tracker.db            # SQLite database (auto-created)
└── settings.json         # Configuration file (auto-created)
```

### 🔧 Configuration

The `settings.json` file stores your preferences:

```json
{
    "watchlist": ["chrome.exe", "valorant.exe"],
    "check_interval_seconds": 5,
    "save_interval_seconds": 60,
    "theme": "dark",
    "minimize_to_tray": true,
    "run_at_startup": false,
    "export_directory": "C:\\Users\\YourName\\Documents\\TimeTrace_Exports",
    "export_range": "today"
}
```

### 💡 Common Applications

**Browsers:** `chrome.exe`, `firefox.exe`, `msedge.exe`, `brave.exe`, `opera.exe`  
**Games:** `valorant.exe`, `LeagueClient.exe`, `RiotClientServices.exe`  
**Communication:** `discord.exe`, `whatsapp.exe`, `telegram.exe`, `slack.exe`  
**Development:** `code.exe` (VS Code), `pycharm64.exe`, `notepad++.exe`  
**Office:** `WINWORD.EXE` (Word), `EXCEL.EXE`, `POWERPNT.EXE`  
**Media:** `spotify.exe`, `vlc.exe`, `obs64.exe`

### 🛠️ Tech Stack

- **Python 3.10+** - Core language
- **CustomTkinter** - Modern UI framework
- **psutil** - Process monitoring
- **SQLite3** - Local database
- **pystray** - System tray integration
- **Pillow** - Icon generation
- **matplotlib** - Chart visualization
- **win10toast** - Desktop notifications
- **PyInstaller** - EXE packaging
- **NSIS** - Professional Windows installer

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md)

### 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🔒 Privacy

- All data is stored **locally** on your computer
- No data is sent to external servers
- Database: `tracker.db` (SQLite)
- Configuration: `settings.json`

### 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/Cezeri73/timetrace/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Cezeri73/timetrace/discussions)

---

<a name="turkish"></a>
## 🇹🇷 Türkçe

### 📖 Genel Bakış

**TimeTrace**, zamanınızın nereye gittiğini anlamanıza yardımcı olan modern, hafif bir masaüstü uygulamasıdır. Seçtiğiniz uygulamaların kullanım süresini takip edin, grafiklerle görselleştirin, bildirimler alın ve verimliliğinizi artırın.

### ✨ Özellikler

- 🎯 **Seçici İzleme** - Tam olarak hangi uygulamaları izleyeceğinizi seçin
- 📊 **Güzel Dashboard** - Günlük, haftalık ve aylık istatistikleri görün
- 📈 **İnteraktif Grafikler** - Kullanımı birden fazla grafik türüyle görselleştirin
- 🔔 **Akıllı Bildirimler** - Uygulamalar zaman limitini aştığında uyarı alın
- 📅 **Geçmiş & Tarih Filtreleri** - Kullanım geçmişini tarayın ve arayın
- 🌙 **Modern Karanlık Tema** - CustomTkinter ile yapılmış şık arayüz
- 💾 **Kalıcı Depolama** - SQLite veritabanı tüm geçmişinizi saklar
- 🔔 **Sistem Tepsisi Desteği** - Tepsiye küçült ve arka planda takip et
- ⚡ **Düşük Kaynak Kullanımı** - Minimum CPU etkisi ile verimli izleme
- 🔍 **Çalışan Uygulamaları Keşfet** - Kolayca eklemek için tüm çalışan uygulamaları gör
- 🛡️ **Hata Dayanıklılığı** - Erişim reddedildi ve işlem hatalarını zarif bir şekilde yönetir
- 🌐 **İki Dilli Arayüz** - İngilizce ve Türkçe dil desteği
- 📤 **CSV Dışa Aktarım** - Analiz için kullanım verilerinizi dışa aktarın
- ⚙️ **Gelişmiş Ayarlar** - Aralıkları, saklama süresini, başlangıç davranışını özelleştirin

### 🚀 Hızlı Başlangıç

#### 📦 Kurulum Yöntemleri

**Aşağıdaki yöntemlerden birini seçin:**

##### ⚡ Yöntem 1: PowerShell Kurulum Scripti (Önerilen)

**Script ile tek tıkla kurulum:**

1. **[install.ps1](https://raw.githubusercontent.com/Cezeri73/timetrace/main/install.ps1)** indirin (Sağ tık → Farklı Kaydet)
2. Çalıştırın: `powershell -ExecutionPolicy Bypass -File install.ps1`
3. Script en son kodu indirir, venv oluşturur, bağımlılıkları kurar ve kısayollar ekler
4. Masaüstü veya Başlat Menüsü'nden başlatın
5. Konsol penceresi yok, pythonw.exe ile çalışır

##### 🔧 Yöntem 2: Manuel Kurulum (Geliştirme İçin)

**Kaynak koddan çalıştırın:**

```bash
# Depoyu klonlayın
git clone https://github.com/Cezeri73/timetrace.git
cd timetrace

# Sanal ortam oluşturun (önerilen)
python -m venv .venv
.venv\Scripts\activate

# Bağımlılıkları kurun
pip install -r requirements.txt

# Uygulamayı çalıştırın (konsol penceresi olmadan)
pythonw main.py
```

**Veya ziyaret edin:** [Releases Sayfası](https://github.com/Cezeri73/timetrace/releases) binary indirmeleri için (yakında)

### 📱 Kullanım

1. **Uygulama Ekleyin**
   - **⚙️ Watchlist** sekmesine gidin
   - **"🔄 Çalışan Uygulamaları Yenile"** butonuna tıklayarak tüm çalışan uygulamaları görün
   - .exe adını kopyalayıp izleme listesine ekleyin
   - Veya manuel olarak uygulama adları girin (örn: `chrome.exe`, `valorant.exe`)

2. **Kullanımı İzleyin**
   - Uygulama arka planda otomatik çalışır
   - Her 5 saniyede bir izlenen uygulamaları kontrol eder
   - Her 60 saniyede bir veritabanına veri kaydeder

3. **İstatistikleri Görüntüleyin**
   - **📊 Dashboard** sekmesini açın
   - Dönem seçin: Bugün, Bu Hafta veya Bu Ay
   - En son veriler için **"🔄 İstatistikleri Yenile"** butonuna tıklayın

4. **Grafiklerle Görselleştirin**
   - **📈 Grafikler** sekmesine gidin
   - En Çok Kullanılan, Günlük Trend, Kategori Dağılımı ve Hafta Karşılaştırma grafiklerini görün

5. **Bildirimler Ayarlayın**
   - **🔔 Bildirimler** sekmesini açın
   - Her izlenen uygulama için zaman eşikleri belirleyin
   - Sessiz saatleri ve erteleme süresini yapılandırın

6. **Geçmişi İnceleyin**
   - **📅 Geçmiş** sekmesine gidin
   - Tarih aralığı filtreleri veya önayarları kullanın (Bugün, Son 7 Gün, Son 30 Gün)
   - Geçmiş kullanımı arayın ve inceleyin

7. **Sistem Tepsisi**
   - Pencereyi kapatmak sistem tepsisine küçültür
   - Göster/gizle veya çık için tepsi ikonuna sağ tıklayın
   - Uygulama arka planda izlemeye devam eder

### 📂 Proje Yapısı

```
TimeTrace/
├── main.py                  # Uygulama giriş noktası
├── main_ui.py              # GUI arayüzü (CustomTkinter)
├── database_manager.py     # SQLite veritabanı işlemleri
├── config_manager.py       # JSON yapılandırma yönetimi
├── monitor_service.py      # Arka plan izleme servisi
├── notification_service.py # Bildirim yönetimi servisi
├── build.ps1              # EXE oluşturma scripti
├── install.ps1            # PowerShell kurulum scripti
├── installer.nsi          # NSIS kurulum yapılandırması
├── requirements.txt       # Python bağımlılıkları
├── tracker.db            # SQLite veritabanı (otomatik oluşturulur)
└── settings.json         # Yapılandırma dosyası (otomatik oluşturulur)
```

### 🔧 Yapılandırma

`settings.json` dosyası tercihlerinizi saklar:

```json
{
    "watchlist": ["chrome.exe", "valorant.exe"],
    "check_interval_seconds": 5,
    "save_interval_seconds": 60,
    "theme": "dark",
    "minimize_to_tray": true,
    "run_at_startup": false,
    "export_directory": "C:\\Users\\KullaniciAdi\\Documents\\TimeTrace_Exports",
    "export_range": "today"
}
```

### 💡 Yaygın Uygulamalar

**Tarayıcılar:** `chrome.exe`, `firefox.exe`, `msedge.exe`, `brave.exe`, `opera.exe`  
**Oyunlar:** `valorant.exe`, `LeagueClient.exe`, `RiotClientServices.exe`  
**İletişim:** `discord.exe`, `whatsapp.exe`, `telegram.exe`, `slack.exe`  
**Geliştirme:** `code.exe` (VS Code), `pycharm64.exe`, `notepad++.exe`  
**Ofis:** `WINWORD.EXE` (Word), `EXCEL.EXE`, `POWERPNT.EXE`  
**Medya:** `spotify.exe`, `vlc.exe`, `obs64.exe`

### 🛠️ Teknoloji Yığını

- **Python 3.10+** - Ana dil
- **CustomTkinter** - Modern UI framework
- **psutil** - İşlem izleme
- **SQLite3** - Yerel veritabanı
- **pystray** - Sistem tepsisi entegrasyonu
- **Pillow** - İkon oluşturma
- **matplotlib** - Grafik görselleştirme
- **win10toast** - Masaüstü bildirimleri
- **PyInstaller** - EXE paketleme
- **NSIS** - Profesyonel Windows kurulum

### 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Lütfen bir Pull Request göndermekten çekinmeyin.

1. Projeyi fork edin
2. Özellik dalınızı oluşturun (`git checkout -b feature/HarikaBirOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Harika bir özellik ekle'`)
4. Dalınıza push edin (`git push origin feature/HarikaBirOzellik`)
5. Bir Pull Request açın

Daha fazla detay için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.

### 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

### 🔒 Gizlilik

- Tüm veriler bilgisayarınızda **yerel olarak** saklanır
- Hiçbir veri harici sunuculara gönderilmez
- Veritabanı: `tracker.db` (SQLite)
- Yapılandırma: `settings.json`

### 📧 İletişim & Destek

- **Sorunlar:** [GitHub Issues](https://github.com/Cezeri73/timetrace/issues)
- **Tartışmalar:** [GitHub Discussions](https://github.com/Cezeri73/timetrace/discussions)

---

<div align="center">

Made with ❤️ by developers, for developers

**[⭐ Star this repo](https://github.com/Cezeri73/timetrace)** if you find it useful!

</div>
