import sys
import json
from pathlib import Path
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import keyboard

def create_image():
    # 建立單色圖示
    image = Image.new('RGB', (64, 64), color='white')
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16, 48, 48], fill='black')
    return image

def on_hotkey():
    print("Hotkey triggered!")

def exit_app(icon, item):
    icon.stop()
    sys.exit()

def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config = load_config()
    screen_shot_hotkey = config.get("hotkey", "alt+1")  # 預設 alt+1

    # 設定托盤選單
    menu = (item('Exit', exit_app),)
    icon = pystray.Icon("HotkeyTray", create_image(), "HotkeyTray", menu)

    # 註冊熱鍵
    keyboard.add_hotkey(screen_shot_hotkey, on_hotkey)
    print(f"Listening for hotkey: {screen_shot_hotkey}")

    # 開始托盤
    icon.run()

if __name__ == "__main__":
    main()
