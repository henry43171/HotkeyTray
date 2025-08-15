# src/__main__.py
import sys
import json
from pathlib import Path
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import keyboard
from modules.screenshot import take_screenshot


def create_image():
    """
    Create a simple monochrome tray icon.
    Returns a PIL.Image object.
    """
    image = Image.new('RGB', (64, 64), color='white')
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16, 48, 48], fill='black')  # Draw a simple black square
    return image


def exit_app(icon, item):
    """
    Stop the tray icon and exit the program.
    """
    icon.stop()
    sys.exit()


def load_config():
    """
    Load configuration from config/config.json.
    Returns a dictionary with config values.
    """
    config_path = Path(__file__).parent.parent / "config" / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


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
    icon = pystray.Icon("HotkeyTray", create_image(), "HotkeyTray", menu)

    # Register hotkey to trigger screenshot, pass config to handler
    keyboard.add_hotkey(screenshot_hotkey, lambda: on_hotkey(config))
    print(f"Listening for hotkey: {screenshot_hotkey}")

    # Run the tray icon loop
    icon.run()


def on_hotkey(config):
    """
    Handler called when the screenshot hotkey is pressed.
    Calls the screenshot module and prints the saved path.
    """
    file_path = take_screenshot(config=config)
    print(f"Screenshot saved: {file_path}")


if __name__ == "__main__":
    main()
