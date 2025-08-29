# HotkeyTray

HotkeyTray 是一個簡單的 Windows 系統匯托盤工具，提供快捷鍵截圖功能，並支援多螢幕環境。  

## 功能特色

- 支援系統托盤，常駐背景運行  
- 提供快捷鍵截圖功能（預設 Alt+1 截左螢幕，Alt+2 截右螢幕）  
- 支援多螢幕偵測  
- 可透過設定視窗修改快捷鍵與截圖儲存路徑  
- 設定會儲存至 `config/config.json`  
- 可使用 `.env` 檔案覆蓋部分設定  

## 程式架構
```
HotkeyTray/
├── src/
│   ├── __main__.py              # 主程式，負責托盤與快捷鍵註冊
│   ├── modules/
│   │   └── screenshot.py        # 截圖與螢幕資訊
│   └── tray_settings/
│       ├── tray_config.py       # 設定檔讀寫
│       └── tray_ui.py           # 設定視窗 (Tkinter)
├── config/
│   └── config.json              # 使用者設定檔 (自動建立)
├── assets/
│   └── icon.ico                 # 系統托盤圖示
└── .env                         # 環境變數設定
```

## 使用步驟

1. 安裝需求套件  
   先手動安裝主要依賴套件：  
   pip install pystray keyboard pillow python-dotenv  

2. 執行程式  
   python src/__main__.py  

3. 系統托盤中會出現 HotkeyTray 圖示  
   - Alt+1：擷取左螢幕  
   - Alt+2：擷取右螢幕  
   - 設定：開啟設定視窗  
   - Exit：結束程式  

## 設定檔

- config/config.json：主要設定檔，會在程式啟動時自動建立  
- .env：可選，優先權高於 config.json 中的設定  

範例 .env 內容：  
HOTKEYS=alt+1,alt+2  
ACTION=screenshot  
SCREENSHOT_PATH=screenshots  


