# src/__main__.py
import sys
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

def main():
    # 設定托盤選單
    menu = (item('Exit', exit_app),)
    icon = pystray.Icon("HotkeyTray", create_image(), "HotkeyTray", menu)

    # 註冊熱鍵
    hotkey = "alt+1"
    keyboard.add_hotkey(hotkey, on_hotkey)
    print(f"Listening for hotkey: {hotkey}")

    # 開始托盤
    icon.run()

if __name__ == "__main__":
    main()
