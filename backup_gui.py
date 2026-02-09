#!/usr/bin/env python3
"""
🖥️ PC BACKUP TOOL - GUI VERSION
Easy-to-use graphical interface for PC backup

Copyright © 2026 DAXX
"""

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    import threading
    import os
    import sys
    from pathlib import Path
    
    # Import our backup modules
    sys.path.insert(0, os.path.dirname(__file__))
    from backup import PCBackup
    from backup_advanced import AdvancedPCBackup
    
except ImportError as e:
    print(f"Error: {e}")
    print("Please install required modules:")
    print("pip install tkinter")
    sys.exit(1)

class BackupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Backup Tool - by DAXX")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Variables
        self.usb_drive = tk.StringVar(value="E:")
        self.backup_type = tk.StringVar(value="basic")
        self.enable_encryption = tk.BooleanVar(value=False)
        self.password = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup GUI components"""
        
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="🔄 PC BACKUP TOOL",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=20)
        
        # Main container
        main = tk.Frame(self.root, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # USB Drive selection
        drive_frame = tk.LabelFrame(main, text="💾 USB Drive", padx=10, pady=10)
        drive_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(drive_frame, text="Drive Letter:").pack(side=tk.LEFT)
        drive_entry = tk.Entry(drive_frame, textvariable=self.usb_drive, width=10)
        drive_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            drive_frame,
            text="Browse",
            command=self.browse_drive
        ).pack(side=tk.LEFT)
        
        # Backup type
        type_frame = tk.LabelFrame(main, text="📦 Backup Type", padx=10, pady=10)
        type_frame.pack(fill=tk.X, pady=5)
        
        tk.Radiobutton(
            type_frame,
            text="📁 Basic (Documents, Photos, Videos)",
            variable=self.backup_type,
            value="basic"
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            type_frame,
            text="⚙️ Advanced (System Settings, WiFi, Browser)",
            variable=self.backup_type,
            value="advanced"
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            type_frame,
            text="🔥 Complete (Both Basic + Advanced)",
            variable=self.backup_type,
            value="complete"
        ).pack(anchor=tk.W)
        
        # Encryption
        encrypt_frame = tk.LabelFrame(main, text="🔒 Encryption (Optional)", padx=10, pady=10)
        encrypt_frame.pack(fill=tk.X, pady=5)
        
        tk.Checkbutton(
            encrypt_frame,
            text="Enable encryption for sensitive data",
            variable=self.enable_encryption,
            command=self.toggle_password
        ).pack(anchor=tk.W)
        
        self.password_frame = tk.Frame(encrypt_frame)
        
        tk.Label(self.password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = tk.Entry(
            self.password_frame,
            textvariable=self.password,
            show="*",
            width=20
        )
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Progress
        progress_frame = tk.LabelFrame(main, text="📊 Progress", padx=10, pady=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=10,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(main)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 START BACKUP",
            command=self.start_backup,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(
            button_frame,
            text="❌ EXIT",
            command=self.root.quit,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
    def browse_drive(self):
        """Browse for USB drive"""
        folder = filedialog.askdirectory()
        if folder:
            self.usb_drive.set(folder)
    
    def toggle_password(self):
        """Toggle password field"""
        if self.enable_encryption.get():
            self.password_frame.pack(pady=5)
        else:
            self.password_frame.pack_forget()
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_backup(self):
        """Start backup process"""
        # Validate
        if not self.usb_drive.get():
            messagebox.showerror("Error", "Please select USB drive!")
            return
        
        if self.enable_encryption.get() and not self.password.get():
            messagebox.showerror("Error", "Please enter encryption password!")
            return
        
        # Confirm
        result = messagebox.askyesno(
            "Confirm Backup",
            f"Start backup to {self.usb_drive.get()}?\n\nType: {self.backup_type.get()}"
        )
        
        if not result:
            return
        
        # Disable button
        self.start_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        
        # Run in thread
        thread = threading.Thread(target=self.run_backup)
        thread.start()
    
    def run_backup(self):
        """Run backup in background thread"""
        try:
            self.log("=" * 50)
            self.log("🔄 STARTING BACKUP...")
            self.log("=" * 50)
            
            backup_type = self.backup_type.get()
            usb = self.usb_drive.get()
            pwd = self.password.get() if self.enable_encryption.get() else None
            
            if backup_type in ["basic", "complete"]:
                self.log("\n📁 Running BASIC backup...")
                backup = PCBackup(usb)
                
                # Redirect prints to GUI
                import sys
                from io import StringIO
                
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                backup.run_backup()
                
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                self.log(output)
            
            if backup_type in ["advanced", "complete"]:
                self.log("\n⚙️ Running ADVANCED backup...")
                adv_backup = AdvancedPCBackup(usb, pwd)
                
                import sys
                from io import StringIO
                
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                adv_backup.run_advanced_backup()
                
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                self.log(output)
            
            self.log("\n" + "=" * 50)
            self.log("✅ BACKUP COMPLETE!")
            self.log("=" * 50)
            
            messagebox.showinfo(
                "Success",
                "Backup completed successfully!\n\nYou can now safely remove the USB drive."
            )
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {e}")
            messagebox.showerror("Error", f"Backup failed:\n{e}")
        
        finally:
            self.progress_bar.stop()
            self.start_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = BackupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
