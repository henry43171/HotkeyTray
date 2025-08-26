# src/__main__.py
import sys
import json
import os
from pathlib import Path
import pystray
from pystray import MenuItem as item
from dotenv import load_dotenv

import keyboard
from modules.screenshot import take_screenshot, get_monitor_info

from tray_settings.tray_config import load_config, save_config
from tray_settings.tray_ui import show_settings_window

import threading
# from tray_settings.tray_config import load_config
# from tray_settings.tray_ui import show_settings_window

def load_icon():
    """
    Load the icon image for the tray.
    Returns a PIL.Image object, handling both dev and PyInstaller environments.
    """
    from PIL import Image
    
    if getattr(sys, 'frozen', False):
        # PyInstaller environment
        base_path = Path(sys._MEIPASS)
    else:
        # Development environment
        base_path = Path(__file__).parent
    
    icon_path = base_path / "assets" / "icon.ico"
    return Image.open(icon_path)


def exit_app(icon, item):
    """
    Stop the tray icon and exit the program.
    """
    icon.stop()
    sys.exit()


def load_config():
    """
    Load configuration from config/config.json.
    If the file does not exist, create it using .env or default values.
    Returns a dictionary with config values.
    """
    from dotenv import load_dotenv
    load_dotenv()  # 讀取 .env

    config_dir = Path(__file__).parent.parent / "config"
    config_path = config_dir / "config.json"

    # 確保 config 目錄存在
    config_dir.mkdir(parents=True, exist_ok=True)

    # 如果 JSON 存在，直接讀取
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config.json: {e}")
            config = {}
    else:
        config = {}

    # 從 .env 取得 fallback
    env_hotkeys = os.getenv("HOTKEYS")
    env_action = os.getenv("ACTION")
    env_screenshot_path = os.getenv("SCREENSHOT_PATH")

    # 如果 JSON 沒有對應值，就用 .env
    if "hotkeys" not in config and env_hotkeys:
        config["hotkeys"] = env_hotkeys.split(",")
    if "action" not in config and env_action:
        config["action"] = env_action
    if "screenshot_path" not in config and env_screenshot_path:
        config["screenshot_path"] = env_screenshot_path

    # 如果 JSON 沒有任何值，給一個安全預設
    if "hotkeys" not in config:
        config["hotkeys"] = ["alt+1", "alt+2"]
    if "action" not in config:
        config["action"] = "screenshot"
    if "screenshot_path" not in config:
        config["screenshot_path"] = "screenshots"

    # 如果原本 JSON 不存在，建立一份新的 config.json
    if not config_path.exists():
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            print(f"Config file created at {config_path}")
        except IOError as e:
            print(f"Error: Failed to create config.json: {e}")

    return config


def on_settings(icon, item):
    """
    Handler for 'Settings' tray menu item.
    Opens the settings window in a separate thread to avoid blocking pystray.
    """
    config = load_config()
    threading.Thread(target=show_settings_window, args=(config,), daemon=True).start()


def main():
    """
    Main entry point:
    - Load config
    - Setup tray icon and menu
    - Register dual monitor screenshot hotkeys
    - Start the tray icon
    """
    config = load_config()

    # Setup system tray menu with only an Exit option
    
    menu = (
    item('Settings', on_settings),
    item('Exit', exit_app),
    )
    
    icon = pystray.Icon("HotkeyTray", load_icon(), "HotkeyTray", menu)

    # Register hotkeys for dual monitor screenshot from config
    hotkeys = config.get('hotkeys', ['alt+1', 'alt+2'])
    
    # Ensure we have at least 2 hotkeys
    if len(hotkeys) < 2:
        hotkeys.extend(['alt+1', 'alt+2'][len(hotkeys):])
    
    hotkey_left = hotkeys[0]
    hotkey_right = hotkeys[1]
    
    keyboard.add_hotkey(hotkey_left, on_hotkey_left)
    keyboard.add_hotkey(hotkey_right, on_hotkey_right)
    
    print("Multi-monitor screenshot ready!")
    print(f"{hotkey_left} = Left monitor screenshot")
    print(f"{hotkey_right} = Right monitor screenshot")
    print(f"Screenshot path: {config.get('screenshot_path', 'screenshots')}")
    
    # Display monitor info
    try:
        monitors = get_monitor_info()
        print(f"Detected {len(monitors)} monitors:")
        for mon in monitors:
            print(f"  Monitor {mon['number']}: {mon['width']}x{mon['height']} at ({mon['left']}, {mon['top']})")
    except Exception as e:
        print(f"Warning: Could not detect monitor info: {e}")

    # Run the tray icon loop
    icon.run()


def on_hotkey_left():
    """
    Handler for Alt+1: Screenshot left monitor.
    """
    current_config = load_config()
    file_path = take_screenshot(config=current_config, monitor="left")
    print(f"Left monitor screenshot saved: {file_path}")

def on_hotkey_right():
    """
    Handler for Alt+2: Screenshot right monitor.
    """
    current_config = load_config()
    file_path = take_screenshot(config=current_config, monitor="right")
    print(f"Right monitor screenshot saved: {file_path}")


if __name__ == "__main__":
    main()
