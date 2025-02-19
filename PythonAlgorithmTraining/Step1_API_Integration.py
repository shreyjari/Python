import json
import time
import random
import threading
import winsound  # Module for soft chime alerts
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from googleapiclient.discovery import build
import os
import signal

### 🔹 CONFIGURATION ###
API_KEY = "AIzaSyBG5MkoVh3G1ktS2nga8Hu-LBNu9qFDYDk"

# Primary Search Queries
primary_queries = [
    "Project Management",
    "Engineering",
    "Data Visualization",
    "Problem Solving using Data",
    "Healthcare AI",
    "Manufacturing Analytics",
    "Construction Management",
]

# Paths
CHROME_DRIVER_PATH = r"C:\Users\ShreyJariwala\OneDrive\Desktop\1. Learning\1. Projects\2. Python\PythonAlgorithmTraining\chromedriver-win64\chromedriver.exe"
BRAVE_PATH = r"C:\Users\ShreyJariwala\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"

# JSON Log File
LOG_FILE = "watched_videos.json"

# Ensure JSON file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump([], file)

# Function to play a soft chime at script start & end
def play_chime():
    winsound.Beep(1000, 500)  # Beep sound at 1000Hz for 500ms

# Get user input for window mode (default: hidden after 5 seconds)
def get_window_mode():
    print("\n🔹 Do you want to see the browser window? (yes/no) - Default: No in 5 seconds")
    try:
        user_input = input().strip().lower()
    except:
        user_input = "no"

    if user_input == "yes":
        return "--window-size=800,600"  # Minimized
    else:
        return "--headless=new"  # Hidden Mode (default)

# Singleton Pattern for managing WebDriver instance
class WebDriverManager:
    _instance = None

    def __new__(cls, window_mode):
        if cls._instance is None:
            cls._instance = super(WebDriverManager, cls).__new__(cls)
            cls._instance.init_driver(window_mode)
        return cls._instance

    def init_driver(self, window_mode):
        options = webdriver.ChromeOptions()
        options.binary_location = BRAVE_PATH
        options.add_argument("--mute-audio")
        options.add_argument(window_mode)  # User-defined window mode
        self.driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

    def get_driver(self):
        return self.driver

    def is_browser_open(self):
        """Check if the browser is still running."""
        try:
            self.driver.current_window_handle  # Access any property to check if browser is open
            return True
        except:
            return False

# Factory Pattern for YouTube API integration
class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def fetch_videos(self, query, max_results=5):
        request = self.youtube.search().list(
            part="snippet",
            q=query,
            maxResults=max_results,
            type="video",
            order="relevance"
        )
        response = request.execute()

        videos = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            if "shorts" not in title.lower():
                videos.append({"video_id": video_id, "title": title, "url": video_url})

        return videos

# Log Manager for storing watched videos
class LogManager:
    @staticmethod
    def is_video_watched(video_id):
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            watched_videos = json.load(file)
            return any(video["video_id"] == video_id for video in watched_videos)

    @staticmethod
    def log_watched_video(video_id, title, url):
        watched_entry = {
            "video_id": video_id,
            "title": title,
            "url": url,
            "watched_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(LOG_FILE, "r+", encoding="utf-8") as file:
            watched_videos = json.load(file)
            watched_videos.append(watched_entry)
            file.seek(0)
            json.dump(watched_videos, file, indent=4)

# YouTube Watcher with Multithreading & Browser Monitoring
class YouTubeWatcher:
    def __init__(self, window_mode):
        self.driver_manager = WebDriverManager(window_mode)
        self.driver = self.driver_manager.get_driver()
        self.api = YouTubeAPI(API_KEY)
        self.running = True

    def watch_video(self, video):
        if not self.driver_manager.is_browser_open():
            print("❌ Browser closed. Stopping script...")
            self.running = False
            return

        video_id, title, url = video["video_id"], video["title"], video["url"]

        if LogManager.is_video_watched(video_id):
            print(f"⚠️ Skipping (Already Watched): {title}")
            return

        print(f"🎥 Watching: {title} - {url}")
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(2)

        # Switch to new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Set playback speed to max
        try:
            time.sleep(5)
            self.driver.find_element(By.TAG_NAME, "body").send_keys(">")
            self.driver.find_element(By.TAG_NAME, "body").send_keys(">")
        except:
            pass

        watch_time = random.randint(5, 45)
        time.sleep(watch_time)

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        LogManager.log_watched_video(video_id, title, url)
        print(f"✅ Logged: {title} (Watched for {watch_time} sec)")

    def run_parallel(self, search_queries, max_videos=3):
        threads = []
        for query in search_queries:
            if not self.running:
                break

            videos = self.api.fetch_videos(query, max_videos)
            for video in videos:
                if not self.running:
                    break

                thread = threading.Thread(target=self.watch_video, args=(video,))
                threads.append(thread)
                thread.start()

                if len(threads) >= 5:
                    for t in threads:
                        t.join()
                    threads = []

        for t in threads:
            t.join()

# Run the YouTube Watching Automation
if __name__ == "__main__":
    play_chime()  # 🎵 Soft chime at script start
    window_mode = get_window_mode()  # Get user preference for window mode
    watcher = YouTubeWatcher(window_mode)

    try:
        watcher.run_parallel(primary_queries, max_videos=3)
    except KeyboardInterrupt:
        print("\n❌ Script stopped by user.")
    finally:
        print("🛑 Cleaning up resources...")
        watcher.driver.quit()
        print("✅ Cleaning up Complete!")  # Ensure message prints after cleanup
        play_chime()  # 🎵 Soft chime at script end
    
        
