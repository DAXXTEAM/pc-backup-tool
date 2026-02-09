#!/usr/bin/env python3
"""
🔄 Auto PC Backup Tool
Automatically backs up PC when USB is connected
"""

import os
import shutil
import json
import platform
import subprocess
from datetime import datetime
import hashlib

class PCBackup:
    def __init__(self, usb_drive_letter="E:"):
        self.usb_drive = usb_drive_letter
        self.backup_root = os.path.join(usb_drive_letter, "PC_Backup")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_folder = os.path.join(self.backup_root, f"Backup_{self.timestamp}")
        
    def create_backup_structure(self):
        """Create backup folder structure"""
        folders = [
            self.backup_folder,
            os.path.join(self.backup_folder, "Documents"),
            os.path.join(self.backup_folder, "Pictures"),
            os.path.join(self.backup_folder, "Videos"),
            os.path.join(self.backup_folder, "Desktop"),
            os.path.join(self.backup_folder, "Downloads"),
            os.path.join(self.backup_folder, "Music"),
            os.path.join(self.backup_folder, "Browser_Data"),
            os.path.join(self.backup_folder, "System_Info"),
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        print(f"✅ Backup folders created at: {self.backup_folder}")
    
    def get_system_info(self):
        """Get complete system information"""
        info = {
            "timestamp": self.timestamp,
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "username": os.getlogin(),
        }
        
        # Get disk info
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['wmic', 'logicaldisk', 'get', 'caption,filesystem,size,freespace'],
                                      capture_output=True, text=True)
                info['disks'] = result.stdout
            except:
                pass
        
        # Get installed programs (Windows)
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['wmic', 'product', 'get', 'name,version'],
                                      capture_output=True, text=True, timeout=60)
                info['installed_programs'] = result.stdout
            except:
                info['installed_programs'] = "Could not retrieve"
        
        # Get network info
        try:
            result = subprocess.run(['ipconfig'] if platform.system() == "Windows" else ['ifconfig'],
                                  capture_output=True, text=True)
            info['network'] = result.stdout
        except:
            pass
        
        return info
    
    def save_system_info(self):
        """Save system information to file"""
        print("📋 Collecting system information...")
        
        info = self.get_system_info()
        info_file = os.path.join(self.backup_folder, "System_Info", "system_info.json")
        
        with open(info_file, 'w') as f:
            json.dump(info, f, indent=4)
        
        print(f"✅ System info saved: {info_file}")
    
    def backup_user_folders(self):
        """Backup important user folders"""
        if platform.system() == "Windows":
            user_profile = os.environ.get('USERPROFILE', 'C:\\Users\\' + os.getlogin())
        else:
            user_profile = os.path.expanduser('~')
        
        folders_to_backup = {
            'Documents': os.path.join(user_profile, 'Documents'),
            'Pictures': os.path.join(user_profile, 'Pictures'),
            'Videos': os.path.join(user_profile, 'Videos'),
            'Desktop': os.path.join(user_profile, 'Desktop'),
            'Downloads': os.path.join(user_profile, 'Downloads'),
            'Music': os.path.join(user_profile, 'Music'),
        }
        
        for folder_name, source_path in folders_to_backup.items():
            if os.path.exists(source_path):
                dest_path = os.path.join(self.backup_folder, folder_name)
                print(f"📁 Backing up {folder_name}...")
                
                try:
                    # Copy with progress
                    self.copy_with_progress(source_path, dest_path)
                    print(f"✅ {folder_name} backed up!")
                except Exception as e:
                    print(f"⚠️ Error backing up {folder_name}: {e}")
            else:
                print(f"⏭️ {folder_name} not found, skipping...")
    
    def copy_with_progress(self, src, dst):
        """Copy folder with progress indication"""
        if not os.path.exists(src):
            return
        
        # Count total files
        total_files = sum([len(files) for r, d, files in os.walk(src)])
        copied_files = 0
        
        for root, dirs, files in os.walk(src):
            # Create destination directory structure
            dest_root = root.replace(src, dst, 1)
            os.makedirs(dest_root, exist_ok=True)
            
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest_root, file)
                
                try:
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    
                    # Show progress every 10 files
                    if copied_files % 10 == 0:
                        progress = (copied_files / total_files) * 100
                        print(f"   Progress: {progress:.1f}% ({copied_files}/{total_files})")
                except Exception as e:
                    print(f"   ⚠️ Could not copy {file}: {e}")
    
    def backup_browser_data(self):
        """Backup browser bookmarks and passwords"""
        print("🌐 Backing up browser data...")
        
        if platform.system() == "Windows":
            user_profile = os.environ.get('USERPROFILE')
            
            # Chrome
            chrome_path = os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default')
            if os.path.exists(chrome_path):
                try:
                    bookmarks = os.path.join(chrome_path, 'Bookmarks')
                    if os.path.exists(bookmarks):
                        shutil.copy2(bookmarks, os.path.join(self.backup_folder, 'Browser_Data', 'Chrome_Bookmarks'))
                        print("✅ Chrome bookmarks backed up!")
                except Exception as e:
                    print(f"⚠️ Chrome backup error: {e}")
            
            # Firefox
            firefox_path = os.path.join(user_profile, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
            if os.path.exists(firefox_path):
                try:
                    # Find default profile
                    for profile in os.listdir(firefox_path):
                        if profile.endswith('.default') or profile.endswith('.default-release'):
                            places = os.path.join(firefox_path, profile, 'places.sqlite')
                            if os.path.exists(places):
                                shutil.copy2(places, os.path.join(self.backup_folder, 'Browser_Data', 'Firefox_Places.sqlite'))
                                print("✅ Firefox data backed up!")
                except Exception as e:
                    print(f"⚠️ Firefox backup error: {e}")
    
    def create_file_inventory(self):
        """Create inventory of all backed up files"""
        print("📝 Creating file inventory...")
        
        inventory = []
        total_size = 0
        
        for root, dirs, files in os.walk(self.backup_folder):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    total_size += size
                    
                    # Calculate MD5 hash for verification
                    with open(filepath, 'rb') as f:
                        md5 = hashlib.md5(f.read()).hexdigest()
                    
                    inventory.append({
                        'file': filepath.replace(self.backup_folder, ''),
                        'size': size,
                        'md5': md5
                    })
                except:
                    pass
        
        # Save inventory
        inventory_file = os.path.join(self.backup_folder, 'file_inventory.json')
        with open(inventory_file, 'w') as f:
            json.dump({
                'total_files': len(inventory),
                'total_size': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'files': inventory
            }, f, indent=2)
        
        print(f"✅ Inventory created: {len(inventory)} files, {total_size / (1024**3):.2f} GB")
    
    def create_readme(self):
        """Create README file"""
        readme_content = f"""
╔═══════════════════════════════════════════════════════════╗
║              PC BACKUP - AUTO BACKUP SYSTEM               ║
╚═══════════════════════════════════════════════════════════╝

Backup Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Computer: {platform.node()}
User: {os.getlogin()}
OS: {platform.system()} {platform.release()}

───────────────────────────────────────────────────────────

📁 BACKED UP DATA:

✅ Documents
✅ Pictures  
✅ Videos
✅ Desktop files
✅ Downloads
✅ Music
✅ Browser bookmarks
✅ System information
✅ File inventory

───────────────────────────────────────────────────────────

📋 FILE STRUCTURE:

/PC_Backup/
  └── Backup_[timestamp]/
      ├── Documents/        → Your documents
      ├── Pictures/         → Photos & images
      ├── Videos/           → Video files
      ├── Desktop/          → Desktop files
      ├── Downloads/        → Downloaded files
      ├── Music/            → Music files
      ├── Browser_Data/     → Browser bookmarks
      ├── System_Info/      → System details
      └── file_inventory.json → Complete file list

───────────────────────────────────────────────────────────

🔄 TO RESTORE:

1. Copy folders back to your PC
2. Check file_inventory.json for verification
3. Refer to System_Info/ for original locations

───────────────────────────────────────────────────────────

⚠️ SECURITY NOTE:

This backup contains your personal data!
Keep this USB drive secure and encrypted.

───────────────────────────────────────────────────────────

Made with ❤️ by DAXX
Generated: {self.timestamp}

╚═══════════════════════════════════════════════════════════╝
"""
        
        readme_file = os.path.join(self.backup_folder, 'README.txt')
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"✅ README created")
    
    def run_backup(self):
        """Run complete backup process"""
        print("=" * 60)
        print("🔄 PC AUTO BACKUP TOOL")
        print("=" * 60)
        print()
        
        print(f"📍 Backup Location: {self.backup_folder}")
        print()
        
        try:
            # Step 1: Create structure
            self.create_backup_structure()
            print()
            
            # Step 2: System info
            self.save_system_info()
            print()
            
            # Step 3: Backup user folders
            self.backup_user_folders()
            print()
            
            # Step 4: Browser data
            self.backup_browser_data()
            print()
            
            # Step 5: Create inventory
            self.create_file_inventory()
            print()
            
            # Step 6: Create README
            self.create_readme()
            print()
            
            print("=" * 60)
            print("✅ BACKUP COMPLETE!")
            print("=" * 60)
            print(f"\n📁 Backup saved at: {self.backup_folder}")
            print("\n💾 You can now safely remove the USB drive!")
            
        except Exception as e:
            print(f"\n❌ BACKUP FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    # Get USB drive letter from command line or use default
    usb_drive = sys.argv[1] if len(sys.argv) > 1 else "E:"
    
    # Create and run backup
    backup = PCBackup(usb_drive)
    backup.run_backup()
    
    input("\nPress Enter to exit...")
