<div align="center">

# ⏱️ TimeTrace

### Track Your Application Usage Effortlessly

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**[English](#english)** | **[Türkçe](#turkish)**

![TimeTrace Screenshot](https://via.placeholder.com/800x400/1f538d/ffffff?text=TimeTrace+Dashboard)

</div>

---

<a name="english"></a>
## 🌍 English

### 📖 Overview

**TimeTrace** is a modern, lightweight desktop application that helps you understand where your time goes. Track usage duration of specific applications you choose, visualize your daily statistics, and improve your productivity.

### ✨ Features

- 🎯 **Selective Tracking** - Choose exactly which applications to monitor
- 📊 **Beautiful Dashboard** - View today's usage statistics at a glance
- 🌙 **Modern Dark UI** - Sleek interface built with CustomTkinter
- 💾 **Persistent Storage** - SQLite database keeps all your history
- 🔔 **System Tray Support** - Minimize to tray and keep tracking in background
- ⚡ **Low Resource Usage** - Efficient monitoring with minimal CPU impact
- 🔍 **Running Apps Discovery** - See all running applications to easily add them
- 🛡️ **Error Resilient** - Gracefully handles access denied and process errors
- 🌐 **Bilingual Interface** - Turkish language support

### 🚀 Quick Start

#### Prerequisites
- **Python 3.10+**
- **Windows OS**

#### Installation (Quick)

On Windows, you can use the one-click installer:

1. Download `install.ps1` from the repository root.
2. Right-click the file and select "Run with PowerShell".
3. It will download the latest code, create a virtual environment, and install dependencies.
4. At the end, it prints the exact command to run the app.

#### Installation (Manual)

```bash
# Clone the repository
git clone https://github.com/Cezeri73/timetrace.git
cd timetrace

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

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
   - Click **"🔄 Refresh Stats"** for latest data
   - See time spent on each app today

4. **System Tray**
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
├── requirements.txt        # Python dependencies
├── tracker.db             # SQLite database (auto-created)
└── settings.json          # Configuration file (auto-created)
```

### 🔧 Configuration

The `settings.json` file stores your preferences:

```json
{
    "watchlist": ["chrome.exe", "valorant.exe"],
    "check_interval_seconds": 5,
    "save_interval_seconds": 60,
    "theme": "dark",
    "minimize_to_tray": true
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

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

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

**TimeTrace**, zamanınızın nereye gittiğini anlamanıza yardımcı olan modern, hafif bir masaüstü uygulamasıdır. Seçtiğiniz uygulamaların kullanım süresini takip edin, günlük istatistiklerinizi görselleştirin ve verimliliğinizi artırın.

### ✨ Özellikler

- 🎯 **Seçici İzleme** - Tam olarak hangi uygulamaları izleyeceğinizi seçin
- 📊 **Güzel Dashboard** - Bugünün kullanım istatistiklerini bir bakışta görün
- 🌙 **Modern Karanlık Tema** - CustomTkinter ile yapılmış şık arayüz
- 💾 **Kalıcı Depolama** - SQLite veritabanı tüm geçmişinizi saklar
- 🔔 **Sistem Tepsisi Desteği** - Tepsiye küçült ve arka planda takip et
- ⚡ **Düşük Kaynak Kullanımı** - Minimum CPU etkisi ile verimli izleme
- 🔍 **Çalışan Uygulamaları Keşfet** - Kolayca eklemek için tüm çalışan uygulamaları gör
- 🛡️ **Hata Dayanıklılığı** - Erişim reddedildi ve işlem hatalarını zarif bir şekilde yönetir
- 🌐 **İki Dilli Arayüz** - Türkçe dil desteği

### 🚀 Hızlı Başlangıç

#### Gereksinimler
- **Python 3.10+**
- **Windows OS**

#### Kurulum (Hızlı)

Windows için tek tıkla kurulum kullanabilirsiniz:

1. Depo kök klasöründen `install.ps1` dosyasını indirin.
2. Dosyaya sağ tıklayın ve "PowerShell ile Çalıştır" seçin.
3. En son kodu indirir, sanal ortam oluşturur ve bağımlılıkları kurar.
4. Sonunda uygulamayı çalıştırmak için komutu görüntüler.

#### Kurulum (Manuel)

```bash
# Depoyu klonlayın
git clone https://github.com/Cezeri73/timetrace.git
### 📤 Dışa Aktarım

**🔧 Gelişmiş Ayarlar** sekmesinden CSV dışa aktarımı yapabilirsiniz.
Uygulama dışa aktarımdan sonra dosyanın tam yolunu gösterir ve **Klasörü Aç** butonu sunar.
Ayrıca dışa aktarılan klasörü ve aralığı (Bugün / 7 Gün / 30 Gün) ayarlayabilirsiniz.
cd timetrace

# Bağımlılıkları kurun
pip install -r requirements.txt

# Uygulamayı çalıştırın
python main.py
```

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
   - En son veriler için **"🔄 İstatistikleri Yenile"** butonuna tıklayın
   - Bugün her uygulamada harcanan süreyi görün

4. **Sistem Tepsisi**
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
├── requirements.txt        # Python bağımlılıkları
├── tracker.db             # SQLite veritabanı (otomatik oluşturulur)
└── settings.json          # Yapılandırma dosyası (otomatik oluşturulur)
```

### 🔧 Yapılandırma

`settings.json` dosyası tercihlerinizi saklar:

```json
{
    "watchlist": ["chrome.exe", "valorant.exe"],
    "check_interval_seconds": 5,
    "save_interval_seconds": 60,
    "theme": "dark",
    "minimize_to_tray": true
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

### 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Lütfen bir Pull Request göndermekten çekinmeyin.

1. Projeyi fork edin
2. Özellik dalınızı oluşturun (`git checkout -b feature/HarikaBirOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Harika bir özellik ekle'`)
4. Dalınıza push edin (`git push origin feature/HarikaBirOzellik`)
5. Bir Pull Request açın

### 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

### 🔒 Gizlilik

- Tüm veriler bilgisayarınızda **yerel olarak** saklanır
- Hiçbir veri harici sunuculara gönderilmez
- Veritabanı: `tracker.db` (SQLite)
- Yapılandırma: `settings.json`

### 📧 İletişim & Destek

- **Sorunlar:** [GitHub Issues](https://github.com/yourusername/timetrace/issues)
- **Tartışmalar:** [GitHub Discussions](https://github.com/yourusername/timetrace/discussions)

---

<div align="center">

Made with ❤️ by developers, for developers

**[⭐ Star this repo](https://github.com/Cezeri73/timetrace)** if you find it useful!

</div>
