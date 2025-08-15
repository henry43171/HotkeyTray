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
    - monitor: int, optional, specific monitor number (1=left, 2=right, None=all)
    """
    if save_dir is None:
        if config and "screenshot_path" in config:
            save_dir = config["screenshot_path"]
        else:
            save_dir = "screenshots"

    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 加入螢幕標識到檔名
    if monitor is not None:
        monitor_label = "left" if monitor == 1 else "right" if monitor == 2 else f"monitor{monitor}"
        filepath = os.path.join(save_dir, f"screenshot_{monitor_label}_{timestamp}.png")
        
        # 截取指定螢幕
        with mss.mss() as sct:
            monitor_info = sct.monitors[monitor]
            sct_img = sct.grab(monitor_info)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
    else:
        # 截取所有螢幕（原本的行為）
        filepath = os.path.join(save_dir, f"screenshot_{timestamp}.png")
        with mss.mss() as sct:
            sct.shot(output=filepath)

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
