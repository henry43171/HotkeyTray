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
        self.geometry("450x280")
        self.config_data = config_data
        self.recording = False  # 是否正在錄製

        hotkeys = self.config_data.get("hotkeys", ["alt+1", "alt+2"])
        if len(hotkeys) < 2:
            hotkeys += [""] * (2 - len(hotkeys))

        # --- Layout container ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)

        # --- Hotkey 1 ---
        ctk.CTkLabel(main_frame, text="Hotkey 1:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.hotkey1_var = ctk.StringVar(value=hotkeys[0])
        hotkey1_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        hotkey1_frame.grid(row=0, column=1, sticky="w", pady=5)
        self.hotkey1_entry = ctk.CTkEntry(hotkey1_frame, textvariable=self.hotkey1_var, width=180)
        self.hotkey1_entry.pack(side="left", padx=(0, 8))
        self.record_button1 = ctk.CTkButton(hotkey1_frame, text="Record", width=80,
                                            command=lambda: self.start_recording(self.hotkey1_var, 1))
        self.record_button1.pack(side="left")

        # --- Hotkey 2 ---
        ctk.CTkLabel(main_frame, text="Hotkey 2:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.hotkey2_var = ctk.StringVar(value=hotkeys[1])
        hotkey2_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        hotkey2_frame.grid(row=1, column=1, sticky="w", pady=5)
        self.hotkey2_entry = ctk.CTkEntry(hotkey2_frame, textvariable=self.hotkey2_var, width=180)
        self.hotkey2_entry.pack(side="left", padx=(0, 8))
        self.record_button2 = ctk.CTkButton(hotkey2_frame, text="Record", width=80,
                                            command=lambda: self.start_recording(self.hotkey2_var, 2))
        self.record_button2.pack(side="left")

        # --- Screenshot Path ---
        ctk.CTkLabel(main_frame, text="Screenshot Path:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.path_var = ctk.StringVar(value=self.config_data.get("screenshot_path", "screenshots"))
        self.path_entry = ctk.CTkEntry(main_frame, textvariable=self.path_var, width=280)
        self.path_entry.grid(row=2, column=1, sticky="w", pady=10)

        # --- Save Button ---
        self.save_button = ctk.CTkButton(main_frame, text="Save and Restart", command=self.save_and_close)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=(15, 5))

        # --- Status Label ---
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(5, 5))

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
