import datetime
import os
import mss

def take_screenshot(config=None, save_dir=None):
    """
    Take a screenshot and save it with timestamp filename.

    Parameters:
    - config: dict, optional, configuration containing 'screenshot_path'
    - save_dir: str, optional, overrides config path
    """
    if save_dir is None:
        if config and "screenshot_path" in config:
            save_dir = config["screenshot_path"]
        else:
            save_dir = "screenshots"

    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(save_dir, f"screenshot_{timestamp}.png")

    with mss.mss() as sct:
        sct.shot(output=filepath)

    return filepath
