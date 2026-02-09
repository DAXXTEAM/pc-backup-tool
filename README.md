# 🔄 PC Auto Backup USB Tool

**Apne PC ka complete backup pendrive mein!**

---

## ✨ FEATURES:

✅ **Auto Backup** - Pendrive lagao, backup shuru!  
✅ **Complete Data** - Documents, Photos, Videos, Desktop  
✅ **Browser Data** - Chrome/Firefox bookmarks  
✅ **System Info** - Complete PC details  
✅ **File Inventory** - Sabhi files ki list + MD5 hash  
✅ **Progress Display** - Real-time progress  
✅ **Safe & Secure** - Koi data delete nahi hoga  

---

## 📋 BACKED UP DATA:

- 📄 Documents
- 🖼️ Pictures
- 🎬 Videos
- 🖥️ Desktop files
- 📥 Downloads
- 🎵 Music
- 🌐 Browser bookmarks
- 💻 System information
- 📝 Installed programs list

---

## 🚀 HOW TO USE:

### **Method 1: Python Script (Recommended)**

**Step 1: Install Python**
- Download: https://python.org
- Install with "Add to PATH" checked

**Step 2: Copy to USB**
```
Copy these files to your USB drive:
- backup.py
- README.md
```

**Step 3: Run**
```bash
# Double-click or run:
python backup.py

# Or specify USB drive:
python backup.py D:
python backup.py E:
```

---

### **Method 2: EXE File (No Python needed)**

**Convert to EXE first:**
```bash
pip install pyinstaller
pyinstaller --onefile --icon=backup.ico backup.py
```

**Then:**
1. Copy `backup.exe` to USB root
2. Double-click to run!

---

## 📁 OUTPUT STRUCTURE:

```
USB Drive (E:)
├── backup.py          (The script)
├── backup.exe         (Optional: compiled version)
├── autorun.inf        (Auto-start config)
└── PC_Backup/
    └── Backup_20260208_191500/
        ├── Documents/
        ├── Pictures/
        ├── Videos/
        ├── Desktop/
        ├── Downloads/
        ├── Music/
        ├── Browser_Data/
        ├── System_Info/
        │   └── system_info.json
        ├── file_inventory.json
        └── README.txt
```

---

## ⚙️ CONFIGURATION:

**Change USB Drive Letter:**
```python
# Edit in backup.py line 240:
usb_drive = "E:"  # Change to your drive
```

**Add More Folders:**
```python
# Edit folders_to_backup dictionary:
folders_to_backup = {
    'Documents': os.path.join(user_profile, 'Documents'),
    'MyCustomFolder': 'C:\\Path\\To\\Folder',  # Add here!
}
```

---

## 💡 ADVANCED FEATURES:

### **1. Schedule Auto-Backup (Windows)**

Create `.bat` file:
```batch
@echo off
python E:\backup.py E:
```

Task Scheduler:
- Open Task Scheduler
- Create Task
- Trigger: On USB connect
- Action: Run backup.bat

---

### **2. Encrypted Backup**

Add encryption (requires `cryptography`):
```python
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt files
with open(file, 'rb') as f:
    encrypted = cipher.encrypt(f.read())
```

---

### **3. Cloud Upload After Backup**

Add at end of backup:
```python
# Upload to Google Drive/Dropbox
import dropbox
dbx = dropbox.Dropbox('YOUR_TOKEN')
dbx.files_upload(file_data, '/backup.zip')
```

---

## 🔒 SECURITY TIPS:

1. **Encrypt USB drive** - BitLocker (Windows) / VeraCrypt
2. **Password protect** - 7-Zip encrypted archive
3. **Keep safe** - Store in secure location
4. **Regular backups** - Weekly recommended
5. **Test restore** - Verify backup works!

---

## ⚠️ IMPORTANT NOTES:

**What it DOES:**
✅ Copy your personal files  
✅ Preserve folder structure  
✅ Create file inventory  
✅ Save system info  

**What it DOES NOT:**
❌ Copy Windows system files  
❌ Copy installed programs (only list)  
❌ Copy passwords (only bookmarks)  
❌ Modify or delete anything on PC  

---

## 🐛 TROUBLESHOOTING:

**"Permission Denied" error:**
- Close programs using those files
- Run as Administrator

**"Drive not found":**
- Check USB drive letter
- Change in script

**Slow backup:**
- Normal for large files!
- Wait patiently

**Missing files:**
- Check file_inventory.json
- Some system files can't be copied

---

## 📊 EXAMPLE OUTPUT:

```
============================================================
🔄 PC AUTO BACKUP TOOL
============================================================

📍 Backup Location: E:\PC_Backup\Backup_20260208_191500

✅ Backup folders created
📋 Collecting system information...
✅ System info saved

📁 Backing up Documents...
   Progress: 25.5% (255/1000)
   Progress: 50.0% (500/1000)
   Progress: 100.0% (1000/1000)
✅ Documents backed up!

📁 Backing up Pictures...
✅ Pictures backed up!

... (continues for all folders)

🌐 Backing up browser data...
✅ Chrome bookmarks backed up!

📝 Creating file inventory...
✅ Inventory created: 5,234 files, 12.5 GB

============================================================
✅ BACKUP COMPLETE!
============================================================

📁 Backup saved at: E:\PC_Backup\Backup_20260208_191500

💾 You can now safely remove the USB drive!
```

---

## 🔄 TO RESTORE:

1. Open backup folder on USB
2. Copy folders back to original locations
3. Check `file_inventory.json` for completeness
4. Refer to `System_Info/system_info.json` for details

---

## 📞 SUPPORT:

Made by: DAXX  
Contact: Your Telegram  
Version: 1.0  
Date: Feb 8, 2026  

---

## ⚡ QUICK START COMMANDS:

```bash
# Simple backup
python backup.py

# Specify drive
python backup.py F:

# Create EXE
pyinstaller --onefile backup.py

# Test without USB
python backup.py ./test_backup
```

---

**Happy Backing Up! 🎉**
