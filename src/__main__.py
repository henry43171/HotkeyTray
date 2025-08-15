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
    image = Image.new('RGB', (64, 64), color='white')
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16, 48, 48], fill='black')
    return image

def on_hotkey():
    file_path = take_screenshot()
    print(f"Screenshot saved: {file_path}")

def exit_app(icon, item):
    icon.stop()
    sys.exit()

def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config = load_config()
    screenshot_hotkey = config.get("hotkey", "alt+1")

    menu = (item('Exit', exit_app),)
    icon = pystray.Icon("HotkeyTray", create_image(), "HotkeyTray", menu)

    keyboard.add_hotkey(screenshot_hotkey, on_hotkey)
    print(f"Listening for hotkey: {screenshot_hotkey}")

    icon.run()

if __name__ == "__main__":
    main()
