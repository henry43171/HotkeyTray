# src/__main__.py
import sys
import json
import os
from pathlib import Path
import pystray
from pystray import MenuItem as item

import keyboard
from modules.screenshot import take_screenshot, get_monitor_info


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
        "hotkeys": ["alt+1", "alt+2"],
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
    
    # Handle backward compatibility for old config format
    if "hotkey_left" in defaults or "hotkey_right" in defaults:
        # Convert old format to new array format
        left_key = defaults.get("hotkey_left", "alt+1")
        right_key = defaults.get("hotkey_right", "alt+2")
        defaults["hotkeys"] = [left_key, right_key]
        # Remove old keys
        defaults.pop("hotkey_left", None)
        defaults.pop("hotkey_right", None)
    
    # Override with environment variables
    env_mapping = {
        "HOTKEY_TRAY_ACTION": "action", 
        "HOTKEY_TRAY_SCREENSHOT_PATH": "screenshot_path"
    }
    
    for env_var, config_key in env_mapping.items():
        env_value = os.getenv(env_var)
        if env_value is not None:
            defaults[config_key] = env_value
    
    # Handle hotkeys environment variables
    hotkey_left_env = os.getenv("HOTKEY_TRAY_HOTKEY_LEFT")
    hotkey_right_env = os.getenv("HOTKEY_TRAY_HOTKEY_RIGHT")
    if hotkey_left_env or hotkey_right_env:
        current_hotkeys = defaults.get("hotkeys", ["alt+1", "alt+2"])
        if hotkey_left_env:
            current_hotkeys[0] = hotkey_left_env
        if hotkey_right_env and len(current_hotkeys) > 1:
            current_hotkeys[1] = hotkey_right_env
        elif hotkey_right_env:
            current_hotkeys.append(hotkey_right_env)
        defaults["hotkeys"] = current_hotkeys
            
    return defaults


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
    menu = (item('Exit', exit_app),)
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
    file_path = take_screenshot(config=current_config, monitor=1)
    print(f"Left monitor screenshot saved: {file_path}")

def on_hotkey_right():
    """
    Handler for Alt+2: Screenshot right monitor.
    """
    current_config = load_config()
    file_path = take_screenshot(config=current_config, monitor=2)
    print(f"Right monitor screenshot saved: {file_path}")


if __name__ == "__main__":
    main()
