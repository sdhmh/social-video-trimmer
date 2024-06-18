from pathlib import Path
import math
from utils import Video


def generate_for_status(
    video: Video,
    ext: str = ".mp4",
    output_suffix: str = ".whatsapp.status",
    whatsapp_web_compatible: bool = True,
):
    duration = video.get_duration(flat=True)
    for _ in range(0, int(duration), 30):
        start = _
        end = _ + (30 if _ + 30 <= 30 * math.floor(duration/30) else duration % 30)
        if whatsapp_web_compatible:
            trimmed = video.trim(start, end, vcodec="libx264", ext=ext, output_suffix=output_suffix + ".encoded")
        else:
            trimmed = video.trim(start, end, ext=ext, output_suffix=output_suffix)
        trimmed.run()


def whatsapp_editor(
    filename: Path,
    dest_dir: Path,
    ext: str = ".mp4",
    output_suffix: str = ".whatsapp",
    whatsapp_web_compatible: bool = True,
    status: bool = False,
):
    video = Video(filename, dest_dir)
    if status:
        generate_for_status(
            video, ext, output_suffix + ".status", whatsapp_web_compatible
        )
    elif whatsapp_web_compatible:
        encoded = video.encode("libx264", ext=ext, output_suffix=output_suffix + ".encoded")
        encoded.run()
    else:
        print("Nothing to do! Exiting...")
