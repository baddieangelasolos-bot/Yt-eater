#!/usr/bin/env python3
import json
import os
import shlex
import subprocess
import sys

from ytdlp_common import load_config

EDIT_LIST_PATH = "data/edit_list.json"
OUTPUT_PATH = "output/final_video.mp4"


def has_audio(path):
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", path],
        stdout=subprocess.PIPE, universal_newlines=True,
    )
    return bool(probe.stdout.strip())


def main():
    if not os.path.exists(EDIT_LIST_PATH):
        print("ERROR: missing " + EDIT_LIST_PATH + " (run generate_edit_list.py first)")
        sys.exit(1)
    cfg = load_config()
    with open(EDIT_LIST_PATH, "r", encoding="utf-8") as f:
        edit_list = json.load(f)

    width, height = cfg["output_resolution"].split("x")
    fps = str(cfg["fps"])
    clips = edit_list["clips"]
    audio = all(has_audio(c["file"]) for c in clips)
    if not audio:
        print("Some clips have no audio; rendering video only.")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for c in clips:
        cmd += ["-t", str(c["duration"]), "-i", c["file"]]

    parts = []
    labels = ""
    for i in range(len(clips)):
        parts.append(
            "[%d:v]scale=%s:%s:force_original_aspect_ratio=decrease,"
            "pad=%s:%s:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=%s,format=yuv420p[v%d]"
            % (i, width, height, width, height, fps, i)
        )
        labels += "[v%d]" % i
        if audio:
            parts.append("[%d:a]aresample=48000,aformat=channel_layouts=stereo[a%d]" % (i, i))
            labels += "[a%d]" % i
    parts.append(labels + "concat=n=%d:v=1:a=%d%s" % (len(clips), 1 if audio else 0, "[v][a]" if audio else "[v]"))

    cmd += ["-filter_complex", ";".join(parts), "-map", "[v]"]
    if audio:
        cmd += ["-map", "[a]", "-c:a", "aac"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-movflags", "+faststart", OUTPUT_PATH]

    os.makedirs("output", exist_ok=True)
    print("Running: " + " ".join(shlex.quote(a) for a in cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("ERROR: ffmpeg failed")
        sys.exit(1)
    if not os.path.exists(OUTPUT_PATH) or os.path.getsize(OUTPUT_PATH) == 0:
        print("ERROR: output video is missing or empty")
        sys.exit(1)
    print("Wrote " + OUTPUT_PATH + " (" + str(os.path.getsize(OUTPUT_PATH)) + " bytes)")


if __name__ == "__main__":
    main()
