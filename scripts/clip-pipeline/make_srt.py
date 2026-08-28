import os, subprocess, json
from faster_whisper import WhisperModel

SP = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
DL = "/home/mark/Downloads"
WAV = "/tmp/ycwab-clipwav"; os.makedirs(WAV, exist_ok=True)
SRT = SP + "/srt-raw";     os.makedirs(SRT, exist_ok=True)

AUDIO = {"22": DL+"/Voice 260822_181740.m4a",
         "24": DL+"/Voice 260824_181409.m4a",
         "25": DL+"/Voice 260825_182031.m4a"}

def t(m): a,b = m.split(":"); return int(a)*60+int(b)

CLIPS = [
    (1,  "paul-mccartney",        "22", "44:00", "45:31"),
    (2,  "six-year-sulk",         "22", "11:00", "11:58"),
    (3,  "victoria-line",         "24", "42:26", "43:23"),
    (4,  "slush-pile",            "22", "08:00", "09:02"),
    (5,  "john-mills-bathroom",   "24", "27:53", "29:41"),
    (6,  "talking-in-a-field",    "24", "30:17", "31:23"),
    (7,  "tell-me-a-story",       "22", "33:46", "34:53"),
    (8,  "emotional-labour",      "22", "40:31", "41:47"),
    (9,  "skull-not-crossbones",  "22", "49:07", "50:06"),
    (10, "englished-our-way",     "24", "51:05", "51:51"),
    (11, "nearest-and-dearest",   "24", "51:53", "52:41"),
    (12, "opening-the-box",       "24", "59:27", "60:20"),
    (13, "audience-of-one",       "25", "00:03", "01:07"),
    (14, "split-infinitive",      "22", "20:53", "22:01"),
    (15, "tech-rehearsal",        "24", "56:32", "57:28"),
]

model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=16)

MAXLINE, MAXLINES = 38, 2

def fmt(s):
    h = int(s//3600); m = int(s%3600//60); sec = s%60
    return "%02d:%02d:%06.3f" % (h, m, sec).replace(".", ",") if False else \
           "%02d:%02d:%02d,%03d" % (h, m, int(sec), round((sec-int(sec))*1000))

def flush(words, out):
    if not words: return
    text = " ".join(w["w"] for w in words)
    # wrap to at most MAXLINES lines
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur)+1+len(w) > MAXLINE:
            lines.append(cur); cur = w
        else:
            cur = (cur+" "+w).strip()
    if cur: lines.append(cur)
    out.append((words[0]["s"], words[-1]["e"], "\n".join(lines[:MAXLINES] if len(lines)<=MAXLINES else lines)))

for order, slug, date, tin, tout in CLIPS:
    if os.path.exists("%s/%s.srt" % (SRT, slug)):
        continue
    wav = "%s/%s.wav" % (WAV, slug)
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t(tin)),"-to",str(t(tout)),
                        "-i",AUDIO[date],"-vn","-ac","1","-ar","16000","-c:a","pcm_s16le",wav],check=True)
    segs,_ = model.transcribe(wav, beam_size=5, word_timestamps=True,
                              vad_filter=True, vad_parameters=dict(min_silence_duration_ms=400))
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "s": w.start, "e": w.end})
    cues, buf = [], []
    for w in words:
        buf.append(w)
        n = len(" ".join(x["w"] for x in buf))
        gap_next = False
        if n >= MAXLINE*MAXLINES or (buf[-1]["w"].endswith((".","?","!")) and n > 20) \
           or (buf[-1]["e"] - buf[0]["s"]) > 5.0:
            flush(buf, cues); buf = []
    flush(buf, cues)
    # enforce min duration and no overlap
    fixed = []
    for i,(s,e,txt) in enumerate(cues):
        e = max(e, s+1.0)
        if i+1 < len(cues): e = min(e, cues[i+1][0]-0.02)
        if e <= s: e = s+0.9
        fixed.append((s,e,txt))
    with open("%s/%s.srt" % (SRT, slug), "w") as f:
        for i,(s,e,txt) in enumerate(fixed,1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, fmt(s), fmt(e), txt))
    print("srt", slug, len(fixed), "cues")
