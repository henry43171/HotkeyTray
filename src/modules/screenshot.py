import datetime
import os
import mss

def take_screenshot(save_dir="screenshots"):
    """Take a screenshot and save it with timestamp filename."""
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(save_dir, f"screenshot_{timestamp}.png")

    with mss.mss() as sct:
        sct.shot(output=filepath)

    return filepath

# if __name__ == "__main__":
#     file_path = take_screenshot()
#     print(f"Screenshot saved to: {file_path}")