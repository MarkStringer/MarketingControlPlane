"""Cut video[start:end] to out; fail if the result is not 60-90 seconds."""
import subprocess, sys
from pathlib import Path

LO, HI = 60.0, 90.0

def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout)

def main(video, start, end, out):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-to", str(end), "-i", video,
                    "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", out], check=True)
    d = duration(out)
    print("%s: %.1fs" % (out, d))
    if not LO <= d <= HI:
        Path(out).unlink()
        sys.exit("duration %.1fs outside %d-%ds; clip deleted" % (d, LO, HI))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
