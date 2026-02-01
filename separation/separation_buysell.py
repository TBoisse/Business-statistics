import cv2
import numpy as np

def sep_buysell(img_path : str, platform : str):
    """
    Return the transaction type for the platform.
    
    :param img_path: The screenshot path.
    :type img_path: str
    :param platform: The platform from which the screenshot come.
    :type platform: str
    """
    img_bgr = cv2.imread(img_path)
    h, w, _ = img_bgr.shape
    header = img_bgr[int(0.14 * h):int(0.17 * h), :]
    hsv = cv2.cvtColor(header, cv2.COLOR_BGR2HSV)

    if platform == "vinted":
        lower = np.array([90, 80, 80])
        upper = np.array([140, 255, 255])
    else:
        lower = np.array([0, 0, 33])
        upper = np.array([0, 0, 73])
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    proj = np.sum(mask, axis=0)
    if proj.max() < 10:
        return "unknown"
    xs = np.arange(len(proj))
    x_center = int(np.sum(xs * proj) / np.sum(proj))
    if x_center < w // 2:
        return "sell"
    else:
        return "buy"