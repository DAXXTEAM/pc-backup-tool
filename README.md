# 🔄 PC Backup & Clone Tool

**Complete PC backup solution with advanced features!**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)]()

---

## ✨ Features

### 📁 Basic Backup
- Documents, Pictures, Videos
- Desktop & Downloads
- Music files
- Browser bookmarks
- System information
- File inventory with MD5 hashes

### ⚙️ Advanced Backup
- Windows Registry
- WiFi passwords
- Browser data (passwords, history, cookies)
- Installed applications list
- System settings & configuration
- Network configuration

### 🔒 Security
- Optional encryption (AES-256)
- Password protection
- Secure sensitive data

### 🖥️ GUI Interface
- Easy-to-use graphical interface
- Progress tracking
- One-click backup
- Visual status updates

---

## 🚀 Quick Start

### Installation

**Option 1: Python Script**
```bash
# Requirements
Python 3.7+

# Clone repository
git clone https://github.com/YOUR_USERNAME/pc-backup-tool.git
cd pc-backup-tool

# Run
python backup.py
```

**Option 2: GUI Version**
```bash
python backup_gui.py
```

**Option 3: Standalone EXE**
```bash
# Download from Releases
# No Python required!
backup.exe
```

---

## 📖 Usage

### Basic Backup
```bash
# Simple backup to E: drive
python backup.py

# Specify drive
python backup.py F:
```

### Advanced Backup
```bash
# Advanced system backup
python backup_advanced.py

# With encryption
python backup_advanced.py
# Then enter password when prompted
```

### GUI Mode
```bash
python backup_gui.py
```

---

## 📂 Output Structure

```
USB_Drive (E:\)
├── PC_Backup\
│   └── Backup_YYYYMMDD_HHMMSS\
│       ├── Documents\
│       ├── Pictures\
│       ├── Videos\
│       ├── Desktop\
│       ├── Downloads\
│       ├── Music\
│       ├── Browser_Data\
│       ├── System_Info\
│       └── file_inventory.json
│
└── PC_Backup_Advanced\
    └── Backup_YYYYMMDD_HHMMSS\
        ├── SystemSettings\
        ├── Registry\
        ├── WiFiPasswords\
        ├── BrowserData\
        ├── Applications\
        ├── NetworkConfig\
        └── RESTORE.bat
```

---

## ⚙️ Configuration

### Change USB Drive
```python
# In backup.py, line 240:
usb_drive = "E:"  # Change to your drive
```

### Add Custom Folders
```python
# In backup.py, line 49:
folders_to_backup = {
    'Documents': os.path.join(user_profile, 'Documents'),
    'CustomFolder': 'C:\\Your\\Path\\Here',  # Add this
}
```

### Enable Encryption
```bash
python backup_advanced.py
# Choose 'y' for encryption
# Enter password
```

---

## 🔧 Advanced Features

### Scheduled Backup (Windows Task Scheduler)
```batch
@echo off
python E:\backup.py E:
```

### Cloud Upload Integration
```python
# Add to backup.py
import dropbox
dbx = dropbox.Dropbox('YOUR_TOKEN')
dbx.files_upload(data, '/backup.zip')
```

### Network Backup
```python
# Backup over network
usb_drive = "\\\\SERVER\\BackupShare"
```

---

## 📋 Requirements

- **Python:** 3.7 or higher
- **OS:** Windows (tested on Windows 10/11)
- **Disk Space:** Depends on data size
- **Optional:** `cryptography` for encryption

```bash
pip install cryptography
```

---

## 🛡️ Security & Privacy

### What is Backed Up
✅ Your personal files  
✅ System configuration  
✅ WiFi networks (with passwords)  
✅ Browser bookmarks  

### What is NOT Backed Up
❌ Windows system files  
❌ Program executables  
❌ Temporary files  

### Encryption
- Uses AES-256 encryption
- Password-based key derivation
- Encrypts: WiFi passwords, browser data, registry

---

## 🐛 Troubleshooting

### "Permission Denied"
- Run as Administrator
- Close programs using files

### "Python not found"
- Install Python from python.org
- Check "Add Python to PATH"

### "Module not found"
```bash
pip install cryptography
```

### Slow Backup
- Use USB 3.0 port
- Large files take time
- Be patient!

---

## 📊 Examples

### Basic Usage
```bash
# Backup everything to E: drive
python backup.py E:

# Output:
✅ Documents backed up (1,234 files)
✅ Pictures backed up (567 files)
✅ Backup complete!
```

### Advanced Usage
```bash
# Full system clone with encryption
python backup_advanced.py

Enter USB drive letter (default E:): F:
Enable encryption? (y/n): y
Enter password: ********

✅ Registry backed up
✅ WiFi passwords extracted
✅ Browser data backed up
✅ Complete!
```

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 👤 Author

**DAXX**

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: vclubtech@gmail.com

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

## 📸 Screenshots

### GUI Version
![GUI Screenshot](screenshots/gui.png)

### Command Line
![CLI Screenshot](screenshots/cli.png)

---

## 🔄 Version History

- **v1.0.0** (2026-02-09)
  - Initial release
  - Basic backup functionality
  - Advanced system backup
  - GUI interface
  - Encryption support

---

## ⚠️ Disclaimer

This tool is for personal backup use only. Always test backups before relying on them. The author is not responsible for data loss.

---

## 📚 Documentation

For detailed documentation, see:
- [Installation Guide](docs/INSTALLATION.md)
- [User Manual](docs/USER_MANUAL.md)
- [API Reference](docs/API.md)

---

## 🎯 Roadmap

- [ ] Linux support
- [ ] Mac support
- [ ] Cloud storage integration
- [ ] Incremental backups
- [ ] Mobile app backup
- [ ] Network backup
- [ ] Auto-schedule

---

**Made with ❤️ by DAXX**

**Star ⭐ this repo if you found it useful!**
