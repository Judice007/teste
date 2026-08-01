import subprocess
from datetime import timedelta


def _format_timestamp(seconds: float) -> str:
    td = timedelta(seconds=max(seconds, 0))
    total_ms = int(td.total_seconds() * 1000)
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def write_srt(segments: list[dict], clip_start: float, clip_end: float, srt_path: str) -> None:
    """Writes an .srt file with the segments overlapping [clip_start, clip_end],
    re-based to clip-relative timestamps."""
    lines = []
    index = 1
    for seg in segments:
        if seg["end"] <= clip_start or seg["start"] >= clip_end:
            continue
        rel_start = max(seg["start"], clip_start) - clip_start
        rel_end = min(seg["end"], clip_end) - clip_start
        lines.append(str(index))
        lines.append(f"{_format_timestamp(rel_start)} --> {_format_timestamp(rel_end)}")
        lines.append(seg["text"])
        lines.append("")
        index += 1
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def burn_captions(video_path: str, srt_path: str, output_path: str) -> None:
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles='{srt_path}'",
        "-c:a", "copy",
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
