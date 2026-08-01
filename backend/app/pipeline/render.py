import subprocess


def cut_and_reframe(source_path: str, start: float, end: float, output_path: str) -> None:
    """Cuts [start, end] from source and reframes it to 9:16 with a center crop.

    Face/subject tracking for a smarter per-scene crop is a future
    improvement (see docs/mvp-architecture.md) — the center crop is the
    intentional MVP fallback.
    """
    duration = end - start
    vf = "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920"
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start), "-i", source_path,
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-c:a", "aac",
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
