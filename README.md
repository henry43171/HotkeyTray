(For Chinese version, please see README_zh.md)
# HotkeyTray

HotkeyTray is a simple Windows system tray utility that provides hotkey-based screenshot functionality with multi-monitor support.  

## Features

- Runs in the background with a system tray icon  
- Hotkey-based screenshot functionality (default: Alt+1 for left monitor, Alt+2 for right monitor)  
- Multi-monitor detection support  
- Settings window for customizing hotkeys and screenshot save path  
- Settings are saved in `config/config.json`  
- Supports `.env` file for overriding part of the configuration  

## Project Structure

HotkeyTray/  
├── src/  
│   ├── __main__.py              # Main program: system tray and hotkey registration  
│   ├── modules/  
│   │   └── screenshot.py        # Screenshot and monitor info  
│   └── tray_settings/  
│       ├── tray_config.py       # Config file load/save  
│       └── tray_ui.py           # Settings window (Tkinter)  
├── config/  
│   └── config.json              # User config file (auto-generated)  
├── assets/  
│   └── icon.ico                 # System tray icon  
└── .env                         # Environment variables  

## Usage

1. Install dependencies  
   Manually install the required packages:  
   pip install pystray keyboard pillow python-dotenv  

2. Run the program  
   python src/__main__.py  

3. The system tray will display the HotkeyTray icon:  
   - Alt+1: Capture left monitor  
   - Alt+2: Capture right monitor  
   - Settings: Open settings window  
   - Exit: Quit program  

## Configuration

- config/config.json: Main configuration file, auto-generated at runtime  
- .env: Optional, takes precedence over values in config.json  

Example .env:  
HOTKEYS=alt+1,alt+2  
ACTION=screenshot  
SCREENSHOT_PATH=screenshots  
"""