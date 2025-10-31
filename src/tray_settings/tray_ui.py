# src/tray_settings/tray_ui.py
import sys
import os
import threading
import customtkinter as ctk
import keyboard
from tray_settings.tray_config import save_config


class SettingsWindow(ctk.CTk):
    def __init__(self, config_data):
        super().__init__()
        self.title("Settings")
        self.geometry("420x360")
        self.config_data = config_data
        self.recording = False  # 是否正在錄製

        hotkeys = self.config_data.get("hotkeys", ["alt+1", "alt+2"])
        if len(hotkeys) < 2:
            hotkeys += [""] * (2 - len(hotkeys))

        # --- Hotkey 1 ---
        ctk.CTkLabel(self, text="Hotkey 1").pack(pady=(20, 5))
        self.hotkey1_var = ctk.StringVar(value=hotkeys[0])
        entry_frame1 = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame1.pack(pady=5)
        self.hotkey1_entry = ctk.CTkEntry(entry_frame1, textvariable=self.hotkey1_var, width=200)
        self.hotkey1_entry.pack(side="left", padx=(0, 10))
        self.record_button1 = ctk.CTkButton(entry_frame1, text="Record", width=100,
                                            command=lambda: self.start_recording(self.hotkey1_var, 1))
        self.record_button1.pack(side="left")

        # --- Hotkey 2 ---
        ctk.CTkLabel(self, text="Hotkey 2").pack(pady=(20, 5))
        self.hotkey2_var = ctk.StringVar(value=hotkeys[1])
        entry_frame2 = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame2.pack(pady=5)
        self.hotkey2_entry = ctk.CTkEntry(entry_frame2, textvariable=self.hotkey2_var, width=200)
        self.hotkey2_entry.pack(side="left", padx=(0, 10))
        self.record_button2 = ctk.CTkButton(entry_frame2, text="Record", width=100,
                                            command=lambda: self.start_recording(self.hotkey2_var, 2))
        self.record_button2.pack(side="left")

        # --- Screenshot Path ---
        ctk.CTkLabel(self, text="Screenshot Path").pack(pady=(25, 5))
        self.path_var = ctk.StringVar(value=self.config_data.get("screenshot_path", "screenshots"))
        self.path_entry = ctk.CTkEntry(self, textvariable=self.path_var, width=300)
        self.path_entry.pack(pady=5)

        # --- Save Button ---
        self.save_button = ctk.CTkButton(self, text="Save and Restart", command=self.save_and_close)
        self.save_button.pack(pady=(25, 10))

        # --- Status Label ---
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=(5, 10))

    def start_recording(self, target_var, index):
        if self.recording:
            return

        self.recording = True
        self.status_label.configure(text=f"Recording hotkey {index}... Press your keys.")

        def record_hotkey():
            recorded = keyboard.read_hotkey(suppress=False)
            target_var.set(recorded)
            self.status_label.configure(text=f"Hotkey {index} recorded: {recorded}")
            self.recording = False

        threading.Thread(target=record_hotkey, daemon=True).start()

    def save_and_close(self):
        # 更新 config
        self.config_data["hotkeys"] = [
            self.hotkey1_var.get().strip(),
            self.hotkey2_var.get().strip()
        ]
        self.config_data["screenshot_path"] = self.path_var.get().strip() or "screenshots"

        save_config(self.config_data)
        self.destroy()

        # 自動重啟
        python = sys.executable
        os.execl(python, python, *sys.argv)


def show_settings_window(config_data):
    window = SettingsWindow(config_data)
    window.mainloop()
