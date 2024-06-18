import ffmpeg
from pathlib import Path
import math


class Video:
    def __init__(self, filename: Path, output_dest: Path):
        self.filename = filename
        self.metadata = ffmpeg.probe(filename)["streams"]
        self.output_dest = output_dest
        output_dest.mkdir(exist_ok=True)
        self.video_tracks = [
            track for track in self.metadata if track["codec_type"] == "video"
        ]
        self.audio_tracks = [
            track for track in self.metadata if track["codec_type"] == "audio"
        ]

    def get_duration(self, flat: bool = False) -> float | dict[str, int]:
        audio_track = self.audio_tracks[0]  # ? For now just select the first audio
        video_track = self.video_tracks[0]  # ? and video track
        video_duration = float(video_track["duration"])
        if not flat:
            hours = math.floor(video_duration / 3600)
            mins = math.floor(video_duration / 60)
            secs = math.floor(video_duration % 60)
            ms = math.floor((video_duration % 1) * 1000)
            video_duration = {"hours": hours, "mins": mins, "secs": secs, "ms": ms}
        return video_duration

    def get_metadata(self) -> list[dict]:
        return self.video_tracks, self.audio_tracks

    def trim(self, start: str, stop: str, vcodec: str = "mpeg4", acodec: str = "aac", ext: str = ".mp4", output_suffix=".reencoded"):
        return ffmpeg.input(self.filename).output(
            filename=str(self.output_dest / f"{self.filename.stem}.{start}s-{stop}s{output_suffix}{ext}"),
            ss=start,
            to=stop,
            vcodec=vcodec,
            acodec=acodec,
        )

    def encode(self, vcodec: str = "mpeg4", acodec: str = "aac", ext: str = ".mp4", output_suffix=".reencoded"):
        return ffmpeg.input(self.filename).output(
            filename=str(self.output_dest / f"{self.filename.stem}{output_suffix}{ext}"),
            vcodec=vcodec,
            acodec=acodec,
        )
