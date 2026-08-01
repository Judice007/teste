import os

import yt_dlp


def download_source(source_url: str, dest_dir: str) -> str:
    """Downloads a VOD (Twitch/YouTube/Kick) and returns the local mp4 path."""
    os.makedirs(dest_dir, exist_ok=True)
    output_template = os.path.join(dest_dir, "source.%(ext)s")
    ydl_opts = {
        "format": "bestvideo[height<=1080]+bestaudio/best",
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([source_url])
    return os.path.join(dest_dir, "source.mp4")
