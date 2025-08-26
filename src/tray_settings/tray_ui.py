# src/tray_settings/tray_ui.py
import sys
import os
import customtkinter as ctk
from tray_settings.tray_config import save_config

class SettingsWindow(ctk.CTk):
    def __init__(self, config_data):
        super().__init__()
        self.title("Settings")
        self.geometry("400x250")
        
        # 使用傳入的 config
        self.config_data = config_data
        
        # Hotkeys Label + Entry
        ctk.CTkLabel(self, text="Hotkeys (comma separated)").pack(pady=(20,5))
        self.hotkeys_var = ctk.StringVar(value=",".join(self.config_data.get("hotkeys", [])))
        self.hotkeys_entry = ctk.CTkEntry(self, textvariable=self.hotkeys_var)
        self.hotkeys_entry.pack(pady=5)
        
        # Screenshot Path Label + Entry
        ctk.CTkLabel(self, text="Screenshot Path").pack(pady=(10,5))
        self.path_var = ctk.StringVar(value=self.config_data.get("screenshot_path", "screenshots"))
        self.path_entry = ctk.CTkEntry(self, textvariable=self.path_var)
        self.path_entry.pack(pady=5)
        
        # Save Button
        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_and_close)
        self.save_button.pack(pady=20)
        
    def save_and_close(self):
        # 更新 config dict
        self.config_data["hotkeys"] = [hk.strip() for hk in self.hotkeys_var.get().split(",") if hk.strip()]
        self.config_data["screenshot_path"] = self.path_var.get().strip() or "screenshots"
        save_config(self.config_data)
        self.destroy()

        # 強制重啟程式
        python = sys.executable
        os.execl(python, python, *sys.argv)

def show_settings_window(config_data):
    window = SettingsWindow(config_data)
    window.mainloop()
