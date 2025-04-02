import os
import json
import time
import requests
import ffmpeg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv, set_key

# Load the environment variables from the .env file
load_dotenv()

# Check if ffmpeg path is in the .env file, if not, ask the user for it
ffmpeg_path = os.getenv("FFMPEG_PATH")
if not ffmpeg_path:
    print("FFmpeg path not found in .env file.")
    ffmpeg_path = input("Enter the full path to ffmpeg (e.g., C:\\path\\to\\ffmpeg.exe): ")
    
    # Save the ffmpeg path to the .env file for future use
    with open(".env", "a") as f:
        set_key(".env", "FFMPEG_PATH", ffmpeg_path)

# Prompt user for the song URL
song_url = input("Enter the Audiomack song URL (e.g., https://audiomack.com/artist/song): ")

# Set up Chrome with network logging options
options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
options.add_argument("--no-sandbox")  # Necessary for some environments (optional)

# Enable network logs
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the song page
print(f"Loading {song_url}...")
driver.get(song_url)

# Wait for the page to load completely
time.sleep(5)

# Attempt to close or dismiss the pop-up (if any)
try:
    # Wait until the overlay element is present, then close it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.web-to-app_WebToAppModule__G_Shf"))
    )
    print("Closing pop-up overlay...")
    overlay_close_button = driver.find_element(By.CSS_SELECTOR, "div.web-to-app_WebToAppModule__G_Shf button")
    overlay_close_button.click()  # Close the pop-up
    print("Pop-up closed.")
except Exception as e:
    print("No pop-up found, proceeding...")

# Find and click the play button
try:
    play_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-amlabs-play-button='true']"))
    )
    button_label = play_button.get_attribute("aria-label")
    print(f"Button state: {button_label}")
    if "Play" in button_label:
        play_button.click()
        print("Clicked play button.")
    else:
        print("Song appears to be playing already (Pause state).")
except Exception as e:
    print(f"Error finding/clicking play button: {e}")
    print("Proceeding anyway, assuming auto-play.")

# Wait for streaming to start
time.sleep(5)

# Extract streaming URL from network logs
stream_url = None
logs = driver.get_log("performance")
for entry in logs:
    message = json.loads(entry["message"])["message"]
    if message["method"] == "Network.responseReceived":
        url = message["params"]["response"]["url"]
        if any(ext in url for ext in [".m3u8", ".mp3", ".m4a"]):  # Check for audio formats
            stream_url = url
            break
driver.quit()

if stream_url:
    print(f"Found streaming URL: {stream_url}")
else:
    print("No streaming URL found. The song might be unavailable or not loading.")
    exit()

# Download the audio
headers = {"User-Agent": "Mozilla/5.0"}
print("Downloading audio file...")
response = requests.get(stream_url, headers=headers, stream=True)

if response.status_code != 200:
    print(f"Failed to download: HTTP {response.status_code}")
    exit()

# Use the appropriate extension based on the URL
ext = stream_url.split(".")[-1].split("?")[0]  # e.g., m4a, mp3, m3u8
temp_file = f"temp_audio.{ext}"
with open(temp_file, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
print(f"Downloaded to {temp_file}")

# Ask user for the desired MP3 filename
output_file = input("Enter the name you want to save the MP3 file as (e.g., my_song.mp3): ")

# If the user doesn't provide a filename, use the default one
if not output_file:
    output_file = "put_me_down.mp3"

# Ensure the filename ends with .mp3
if not output_file.endswith(".mp3"):
    output_file += ".mp3"

# Convert to MP3
try:
    print("Converting to MP3...")
    stream = ffmpeg.input(temp_file)
    stream = ffmpeg.output(stream, output_file, format="mp3", acodec="mp3")
    ffmpeg.run(stream, cmd=ffmpeg_path)
    print(f"Saved to {os.path.abspath(output_file)}")
except FileNotFoundError:
    print(f"Error: 'ffmpeg' not found at {ffmpeg_path}. Verify the path.")
except ffmpeg.Error as e:
    print("Conversion error:", e.stderr.decode())
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"Cleaned up {temp_file}")
