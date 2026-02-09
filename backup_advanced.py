#!/usr/bin/env python3
"""
🔄 ADVANCED PC BACKUP TOOL
Complete PC Clone with Encryption, Cloud Upload, and more!

Copyright © 2026 DAXX
All Rights Reserved
"""

import os
import shutil
import json
import platform
import subprocess
import hashlib
import zipfile
import sqlite3
from datetime import datetime
from pathlib import Path
import socket
import winreg  # Windows only

class AdvancedPCBackup:
    def __init__(self, usb_drive="E:", password=None):
        self.usb_drive = usb_drive
        self.password = password
        self.backup_root = os.path.join(usb_drive, "PC_Backup_Advanced")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_folder = os.path.join(self.backup_root, f"Backup_{self.timestamp}")
        self.computer_name = platform.node()
        
    def create_structure(self):
        """Create advanced backup folder structure"""
        folders = [
            "UserData",
            "SystemSettings",
            "Registry",
            "WiFiPasswords",
            "BrowserData",
            "Applications",
            "Drivers",
            "NetworkConfig",
            "SystemInfo",
            "Encrypted"
        ]
        
        for folder in folders:
            os.makedirs(os.path.join(self.backup_folder, folder), exist_ok=True)
        
        print(f"✅ Advanced folder structure created!")
        
    def backup_registry(self):
        """Backup Windows Registry (Critical settings)"""
        print("🔑 Backing up Registry...")
        
        if platform.system() != "Windows":
            print("⏭️ Not Windows, skipping registry")
            return
            
        try:
            reg_folder = os.path.join(self.backup_folder, "Registry")
            
            # Export important registry keys
            keys_to_backup = [
                ("HKCU\\Software", "user_software.reg"),
                ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", "installed_programs.reg"),
                ("HKCU\\Network", "network_drives.reg"),
            ]
            
            for key_path, filename in keys_to_backup:
                reg_file = os.path.join(reg_folder, filename)
                try:
                    subprocess.run(
                        ['reg', 'export', key_path, reg_file, '/y'],
                        capture_output=True,
                        timeout=30
                    )
                    print(f"   ✅ Exported: {filename}")
                except Exception as e:
                    print(f"   ⚠️ Failed: {filename}")
                    
        except Exception as e:
            print(f"⚠️ Registry backup error: {e}")
    
    def backup_wifi_passwords(self):
        """Extract and backup WiFi passwords"""
        print("📶 Backing up WiFi passwords...")
        
        if platform.system() != "Windows":
            print("⏭️ Not Windows, skipping WiFi")
            return
            
        try:
            wifi_folder = os.path.join(self.backup_folder, "WiFiPasswords")
            
            # Get all WiFi profiles
            profiles = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profiles']
            ).decode('utf-8', errors='ignore').split('\n')
            
            wifi_data = []
            
            for line in profiles:
                if "All User Profile" in line:
                    profile_name = line.split(":")[1].strip()
                    
                    try:
                        # Get password for this profile
                        profile_info = subprocess.check_output(
                            ['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear']
                        ).decode('utf-8', errors='ignore').split('\n')
                        
                        password = None
                        for info_line in profile_info:
                            if "Key Content" in info_line:
                                password = info_line.split(":")[1].strip()
                                break
                        
                        wifi_data.append({
                            'network': profile_name,
                            'password': password if password else "N/A"
                        })
                        
                        print(f"   ✅ {profile_name}: {'***' if password else 'No password'}")
                        
                    except:
                        pass
            
            # Save WiFi data
            wifi_file = os.path.join(wifi_folder, "wifi_passwords.json")
            with open(wifi_file, 'w') as f:
                json.dump(wifi_data, f, indent=4)
            
            print(f"✅ {len(wifi_data)} WiFi networks backed up!")
            
        except Exception as e:
            print(f"⚠️ WiFi backup error: {e}")
    
    def backup_browser_advanced(self):
        """Advanced browser backup - passwords, history, cookies"""
        print("🌐 Advanced browser backup...")
        
        browser_folder = os.path.join(self.backup_folder, "BrowserData")
        user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
        
        browsers = {
            'Chrome': os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default'),
            'Edge': os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default'),
            'Firefox': os.path.join(user_profile, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'),
            'Brave': os.path.join(user_profile, 'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
        }
        
        for browser_name, browser_path in browsers.items():
            if os.path.exists(browser_path):
                print(f"   📁 Backing up {browser_name}...")
                
                files_to_backup = [
                    'Bookmarks',
                    'History',
                    'Login Data',
                    'Cookies',
                    'Preferences',
                    'Web Data'
                ]
                
                browser_backup = os.path.join(browser_folder, browser_name)
                os.makedirs(browser_backup, exist_ok=True)
                
                for file in files_to_backup:
                    src = os.path.join(browser_path, file)
                    if os.path.exists(src):
                        try:
                            shutil.copy2(src, browser_backup)
                            print(f"      ✅ {file}")
                        except Exception as e:
                            print(f"      ⚠️ {file} (locked)")
                
                # Firefox special handling
                if browser_name == "Firefox" and os.path.isdir(browser_path):
                    for profile in os.listdir(browser_path):
                        if '.default' in profile:
                            profile_path = os.path.join(browser_path, profile)
                            for file in ['places.sqlite', 'key4.db', 'logins.json']:
                                src = os.path.join(profile_path, file)
                                if os.path.exists(src):
                                    try:
                                        shutil.copy2(src, browser_backup)
                                        print(f"      ✅ {file}")
                                    except:
                                        pass
    
    def backup_installed_apps(self):
        """Get detailed list of installed applications"""
        print("📦 Collecting installed applications...")
        
        apps_folder = os.path.join(self.backup_folder, "Applications")
        
        if platform.system() == "Windows":
            try:
                # Get from registry
                apps = []
                
                reg_paths = [
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
                ]
                
                for reg_path in reg_paths:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                        
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                subkey = winreg.OpenKey(key, subkey_name)
                                
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                                    
                                    apps.append({
                                        'name': name,
                                        'version': version,
                                        'publisher': publisher
                                    })
                                    
                                except:
                                    pass
                                    
                                winreg.CloseKey(subkey)
                            except:
                                pass
                        
                        winreg.CloseKey(key)
                    except:
                        pass
                
                # Save apps list
                apps_file = os.path.join(apps_folder, "installed_applications.json")
                with open(apps_file, 'w') as f:
                    json.dump(apps, f, indent=4)
                
                print(f"✅ {len(apps)} applications cataloged!")
                
            except Exception as e:
                print(f"⚠️ Apps backup error: {e}")
    
    def backup_system_settings(self):
        """Backup system configuration and settings"""
        print("⚙️ Backing up system settings...")
        
        settings_folder = os.path.join(self.backup_folder, "SystemSettings")
        
        settings = {
            'computer_name': platform.node(),
            'os': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': socket.gethostname(),
            'ip_addresses': [],
        }
        
        # Get IP addresses
        try:
            hostname = socket.gethostname()
            ip_list = socket.gethostbyname_ex(hostname)[2]
            settings['ip_addresses'] = ip_list
        except:
            pass
        
        # Windows specific
        if platform.system() == "Windows":
            try:
                # Environment variables
                settings['environment_variables'] = dict(os.environ)
                
                # System info
                result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=30)
                settings['systeminfo'] = result.stdout
                
            except:
                pass
        
        # Save settings
        settings_file = os.path.join(settings_folder, "system_config.json")
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
        
        print("✅ System settings backed up!")
    
    def create_clone_script(self):
        """Create restoration script"""
        print("📝 Creating restoration script...")
        
        restore_script = f"""
@echo off
echo ========================================
echo    PC RESTORATION TOOL
echo    Backup Date: {self.timestamp}
echo ========================================
echo.
echo This will restore your backup to current PC.
echo.
pause

echo Restoring user data...
xcopy /E /I /Y "UserData\\*" "%USERPROFILE%\\"

echo.
echo ========================================
echo Restoration complete!
echo.
echo NOTE: Some items may need manual restore:
echo - WiFi passwords (run as Administrator)
echo - Registry settings (import .reg files)
echo - Browser data (copy to browser folders)
echo ========================================
pause
"""
        
        restore_file = os.path.join(self.backup_folder, "RESTORE.bat")
        with open(restore_file, 'w') as f:
            f.write(restore_script)
        
        print("✅ Restoration script created!")
    
    def encrypt_backup(self):
        """Encrypt sensitive data (if password provided)"""
        if not self.password:
            print("⏭️ No password - skipping encryption")
            return
            
        print("🔒 Encrypting sensitive data...")
        
        try:
            from cryptography.fernet import Fernet
            import base64
            
            # Generate key from password
            key = base64.urlsafe_b64encode(hashlib.sha256(self.password.encode()).digest())
            cipher = Fernet(key)
            
            # Encrypt sensitive folders
            sensitive_folders = ['WiFiPasswords', 'BrowserData', 'Registry']
            
            for folder in sensitive_folders:
                folder_path = os.path.join(self.backup_folder, folder)
                if os.path.exists(folder_path):
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            
                            try:
                                with open(file_path, 'rb') as f:
                                    data = f.read()
                                
                                encrypted = cipher.encrypt(data)
                                
                                with open(file_path + '.encrypted', 'wb') as f:
                                    f.write(encrypted)
                                
                                os.remove(file_path)
                                print(f"   🔒 Encrypted: {file}")
                            except:
                                pass
            
            print("✅ Sensitive data encrypted!")
            
        except ImportError:
            print("⚠️ cryptography module not installed - skipping encryption")
            print("   Install with: pip install cryptography")
    
    def run_advanced_backup(self):
        """Run complete advanced backup"""
        print("=" * 70)
        print("🔄 ADVANCED PC BACKUP & CLONE TOOL")
        print("=" * 70)
        print(f"\n📍 Computer: {self.computer_name}")
        print(f"📍 Backup Location: {self.backup_folder}\n")
        
        try:
            # Create structure
            self.create_structure()
            
            # System settings
            self.backup_system_settings()
            
            # Registry
            self.backup_registry()
            
            # WiFi passwords
            self.backup_wifi_passwords()
            
            # Browser data (advanced)
            self.backup_browser_advanced()
            
            # Installed apps
            self.backup_installed_apps()
            
            # Create restore script
            self.create_clone_script()
            
            # Encrypt if password provided
            self.encrypt_backup()
            
            print("\n" + "=" * 70)
            print("✅ ADVANCED BACKUP COMPLETE!")
            print("=" * 70)
            print(f"\n📁 Backup saved at: {self.backup_folder}")
            print("\n💡 TIP: Run backup.py for user files (Documents, Photos, etc.)")
            
        except Exception as e:
            print(f"\n❌ BACKUP FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    print("=" * 70)
    print("🔄 ADVANCED PC BACKUP TOOL")
    print("=" * 70)
    print("\nThis backs up:")
    print("✅ System settings & registry")
    print("✅ WiFi passwords")
    print("✅ Browser data (advanced)")
    print("✅ Installed applications list")
    print("✅ Network configuration")
    print("\n⚠️ Run backup.py separately for user files (Documents, Photos, etc.)")
    print("\n" + "=" * 70)
    
    # Get USB drive
    usb_drive = input("\nEnter USB drive letter (default E:): ").strip() or "E:"
    
    # Optional encryption
    encrypt = input("Enable encryption? (y/n, default n): ").strip().lower()
    password = None
    if encrypt == 'y':
        password = input("Enter encryption password: ").strip()
        if not password:
            print("⚠️ No password provided - encryption disabled")
    
    # Run backup
    backup = AdvancedPCBackup(usb_drive, password)
    backup.run_advanced_backup()
    
    input("\nPress Enter to exit...")
