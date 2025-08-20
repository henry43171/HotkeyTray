import datetime
import os
import mss
import mss.tools

def take_screenshot(config=None, save_dir=None, monitor=None):
    """
    Take a screenshot and save it with timestamp filename.

    Parameters:
    - config: dict, optional, configuration containing 'screenshot_path'
    - save_dir: str, optional, overrides config path
    - monitor: str, optional
        * "left"  -> 最左邊的螢幕
        * "right" -> 最右邊的螢幕
        * None    -> 截全部螢幕 (mss index 0)
    """
    if save_dir is None:
        save_dir = config.get("screenshot_path") if config and "screenshot_path" in config else "screenshots"

    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    with mss.mss() as sct:
        monitors = sct.monitors[1:]  # 跳過 0 (全螢幕範圍)

        if monitor == "left":
            target_monitor = min(monitors, key=lambda m: m["left"])
            monitor_label = "left"
        elif monitor == "right":
            target_monitor = max(monitors, key=lambda m: m["left"])
            monitor_label = "right"
        elif monitor is None:
            filepath = os.path.join(save_dir, f"screenshot_{timestamp}.png")
            sct.shot(output=filepath)
            return filepath
        else:
            raise ValueError("monitor must be 'left', 'right', or None")

        filepath = os.path.join(save_dir, f"screenshot_{monitor_label}_{timestamp}.png")
        sct_img = sct.grab(target_monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)

    return filepath


def get_monitor_info():
    """
    Get information about available monitors.
    Returns list of monitor configurations.
    """
    with mss.mss() as sct:
        monitors = []
        for i, monitor in enumerate(sct.monitors[1:], 1):  # 跳過索引0（全螢幕）
            monitors.append({
                "number": i,
                "width": monitor["width"],
                "height": monitor["height"],
                "left": monitor["left"],
                "top": monitor["top"]
            })
        return monitors
