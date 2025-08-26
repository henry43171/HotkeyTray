import json
from pathlib import Path
import os
from dotenv import load_dotenv

CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.json"

# 預設 config，如果 config.json 不存在就用這個建立
DEFAULT_CONFIG = {
    "hotkeys": ["alt+1", "alt+2"],
    "screenshot_path": "screenshots",
    "action": "screenshot"
}

def load_config():
    """
    Load config.json if exists, otherwise create from DEFAULT_CONFIG.
    Environment variables override if present.
    """
    load_dotenv()
    
    config = DEFAULT_CONFIG.copy()
    
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config.json: {e}")

    # 環境變數覆蓋
    if os.getenv("HOTKEYS"):
        config["hotkeys"] = os.getenv("HOTKEYS").split(",")
    if os.getenv("ACTION"):
        config["action"] = os.getenv("ACTION")
    if os.getenv("SCREENSHOT_PATH"):
        config["screenshot_path"] = os.getenv("SCREENSHOT_PATH")
    
    return config

def save_config(config: dict):
    """
    Save the config dict to config.json.
    """
    os.makedirs(CONFIG_PATH.parent, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
