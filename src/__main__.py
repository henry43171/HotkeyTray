# src/__main__.py
import sys
import json
import os
from pathlib import Path
import pystray
from pystray import MenuItem as item

import keyboard
from .modules.screenshot import take_screenshot


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
    Load configuration with priority: ENV vars > config.json > defaults.
    Returns a dictionary with config values.
    """
    # Default values
    defaults = {
        "hotkey": "alt+1",
        "action": "screenshot", 
        "screenshot_path": "screenshots"
    }
    
    # Load from config.json if exists
    config_path = Path(__file__).parent.parent / "config" / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            defaults.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config.json: {e}")
    
    # Override with environment variables
    env_mapping = {
        "HOTKEY_TRAY_HOTKEY": "hotkey",
        "HOTKEY_TRAY_ACTION": "action", 
        "HOTKEY_TRAY_SCREENSHOT_PATH": "screenshot_path"
    }
    
    for env_var, config_key in env_mapping.items():
        env_value = os.getenv(env_var)
        if env_value is not None:
            defaults[config_key] = env_value
            
    return defaults


def main():
    """
    Main entry point:
    - Load config
    - Setup tray icon and menu
    - Register screenshot hotkey
    - Start the tray icon
    """
    config = load_config()
    screenshot_hotkey = config.get("hotkey", "alt+1")  # default hotkey

    # Setup system tray menu with only an Exit option
    menu = (item('Exit', exit_app),)
    icon = pystray.Icon("HotkeyTray", load_icon(), "HotkeyTray", menu)

    # Register hotkey to trigger screenshot
    keyboard.add_hotkey(screenshot_hotkey, on_hotkey)
    print(f"Listening for hotkey: {screenshot_hotkey}")
    print(f"Screenshot path: {config.get('screenshot_path', 'screenshots')}")

    # Run the tray icon loop
    icon.run()


def on_hotkey():
    """
    Handler called when the screenshot hotkey is pressed.
    Reloads config and calls the screenshot module.
    """
    current_config = load_config()  # 每次都重新載入最新配置
    file_path = take_screenshot(config=current_config)
    print(f"Screenshot saved: {file_path}")


if __name__ == "__main__":
    main()
