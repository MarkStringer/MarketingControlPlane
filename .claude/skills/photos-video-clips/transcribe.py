"""Transcribe a video with the whisper CLI; write <id>.json and <id>.txt to source/photos-videos/transcripts/."""
import json, subprocess, sys, tempfile
from pathlib import Path

OUT = Path("source/photos-videos/transcripts")

def main(video):
    video = Path(video)
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["whisper", str(video), "--model", "small.en", "--language", "en",
                        "--output_format", "json", "--output_dir", tmp], check=True)
        data = json.loads((Path(tmp) / (video.stem + ".json")).read_text())
    segs = [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in data["segments"]]
    (OUT / (video.stem + ".json")).write_text(json.dumps(segs, indent=1))
    (OUT / (video.stem + ".txt")).write_text("\n".join(
        "[%02d:%02d] %s" % (int(s["start"] // 60), int(s["start"] % 60), s["text"]) for s in segs) + "\n")
    print("wrote", OUT / (video.stem + ".txt"), "(%d segments)" % len(segs))

if __name__ == "__main__":
    main(sys.argv[1])
