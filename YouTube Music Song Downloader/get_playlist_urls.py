import yt_dlp
import os
import json
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TXXX, TALB, TCON
from hashlib import sha1

# Input URL (can be single video or playlist)
playlist_url = "https://music.youtube.com/watch?v=ayni7P5qdA4"
playlist_url = playlist_url.replace("music.youtube.com", "www.youtube.com")

# Output paths
output_dir = r"C:\Users\shrey\Music"
json_path = os.path.join(output_dir, "library.json")
archive_path = os.path.join(output_dir, "downloaded.txt")
output_template = os.path.join(output_dir, "%(title).100s.%(ext)s")

# Load or create library.json
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        library = json.load(f)
else:
    library = {}

# Create hash of audio file to avoid content duplication
def hash_audio_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            return sha1(f.read()).hexdigest()
    except:
        return None

# Function to detect classic songs (simple heuristic: older or long-duration songs)
def is_classic_song(info):
    title = info.get("title", "").lower()
    duration = info.get("duration", 0)
    classic_keywords = ["lata", "kishore", "rafi", "mukesh", "classic", "evergreen", "golden"]
    return any(keyword in title for keyword in classic_keywords) or duration > 600

# Function to process each downloaded song
def process_downloaded_song(info):
    title = info.get("title", "Unknown Title")
    artist = ", ".join(info.get("artist", [])) if isinstance(info.get("artist"), list) else info.get("artist", "Unknown Artist")
    playlist = info.get("playlist_title") or info.get("title") or "Unknown Playlist"
    video_id = info.get("id", "")
    duration = info.get("duration", 0)
    filename = os.path.join(output_dir, f"{title}.mp3")

    # Check for duplicate using content hash
    audio_hash = hash_audio_file(filename)
    if audio_hash:
        for entry in library.values():
            if entry.get("hash") == audio_hash:
                print(f"Duplicate content detected. Removing {filename}...")
                os.remove(filename)
                return

    # Update library.json
    library[video_id] = {
        "title": title,
        "artist": artist,
        "playlist": playlist,
        "duration": duration,
        "filename": filename,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "hash": audio_hash
    }

    # Tag Album (Playlist Name), YTVideoID, and Genre if classic
    try:
        audio = ID3(filename)
        audio.add(TALB(encoding=3, text=playlist))  # Album
        audio.add(TXXX(encoding=3, desc="YTVideoID", text=video_id))  # Custom video ID
        if is_classic_song(info):
            audio.add(TCON(encoding=3, text="Classic"))  # Genre
        audio.save()
        print(f"Tagged: {title}")
    except Exception as e:
        print(f"Failed to tag {filename}: {e}")

# Hook after each file is finished
def hook(d):
    if d["status"] == "finished":
        info_dict = d.get("info_dict")
        if info_dict:
            process_downloaded_song(info_dict)

# yt-dlp options
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': output_template,
    'quiet': False,
    'extract_flat': False,
    'ignoreerrors': True,
    'download_archive': archive_path,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            'key': 'EmbedThumbnail',
        },
        {
            'key': 'FFmpegMetadata',
        }
    ],
    'writethumbnail': True,
    'ffmpeg_location': r'C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin',
    'progress_hooks': [hook],
}

# Start download with yt-dlp
def is_playlist(url):
    return "list=" in url

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print(f"\n Downloading from: {playlist_url}\n")
    ydl.download([playlist_url])

# Save updated library
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(library, f, indent=4, ensure_ascii=False)

print(f"\n Library saved to: {json_path}")
