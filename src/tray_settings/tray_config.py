# src\tray_settings\tray_config.py
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Unified path pointing to project_root/config/config.json
CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "config.json"

# Default config used when config.json does not exist
DEFAULT_CONFIG = {
    "hotkeys": ["alt+1", "alt+2"],
    "screenshot_path": "screenshots",
    "action": "screenshot"
}

def load_config():
    """
    Load config.json if it exists, otherwise create it from DEFAULT_CONFIG.
    Environment variables take precedence if present.
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

    # Override with environment variables if available
    if os.getenv("HOTKEYS"):
        config["hotkeys"] = os.getenv("HOTKEYS").split(",")
    if os.getenv("ACTION"):
        config["action"] = os.getenv("ACTION")
    if os.getenv("SCREENSHOT_PATH"):
        config["screenshot_path"] = os.getenv("SCREENSHOT_PATH")
    
    # Auto-create config.json if it does not exist
    if not CONFIG_PATH.exists():
        save_config(config)
        print(f"Created default config at {CONFIG_PATH}")
    
    return config

def save_config(config: dict):
    """
    Save the given config dictionary to config.json.
    """
    os.makedirs(CONFIG_PATH.parent, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
