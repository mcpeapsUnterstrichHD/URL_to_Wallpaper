import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
from screeninfo import get_monitors

def get_largest_display():
    """Returns the size of the largest display."""
    max_width = 0
    max_height = 0
    for monitor in get_monitors():
        width = monitor.width
        height = monitor.height
        if width * height > max_width * max_height:
            max_width = width
            max_height = height
    return int(max_width), int(max_height)

def take_screenshot(url, width, height):
    """Takes a screenshot of the specified website."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--window-size={width}x{height}")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # Ensure the page has fully loaded
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    image = Image.open(BytesIO(screenshot))
    image = image.resize((width, height), Image.LANCZOS)
    return image

def save_image(image, path):
    """Saves the image to the specified path."""
    image.save(path)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python3 URL_to_Wallpaper.py [URL] [path to save the Wallpaper] [optional: waiting time in minutes]")
        sys.exit(1)

    url = sys.argv[1]
    save_path = sys.argv[2]
    waiting_time_in_minutes = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    if waiting_time_in_minutes < 0:
        waiting_time_in_minutes = waiting_time_in_minutes * -1

    if waiting_time_in_minutes > 0:
        print(f"Waiting for {waiting_time_in_minutes} minutes before taking the screenshot...")
        time.sleep(waiting_time_in_minutes * 60)  # Convert minutes to seconds

    width, height = get_largest_display()
    screenshot = take_screenshot(url, width, height)
    save_image(screenshot, save_path)
    print(f"Screenshot taken and saved to {save_path}")
