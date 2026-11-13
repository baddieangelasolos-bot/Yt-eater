#!/usr/bin/env python3
import glob
import json
import os
import subprocess
import sys

from ytdlp_common import load_config, ytdlp_base

VIDEO_LIST_PATH = "data/video_list.json"
MANIFEST_PATH = "data/clips_manifest.json"


def main():
    if not os.path.exists(VIDEO_LIST_PATH):
        print("ERROR: missing " + VIDEO_LIST_PATH + " (run fetch_channel_videos.py first)")
        sys.exit(1)
    cfg = load_config()
    with open(VIDEO_LIST_PATH, "r", encoding="utf-8") as f:
        videos = json.load(f)["videos"]

    duration = cfg["clip_duration"]
    max_height = int(cfg["output_resolution"].split("x")[1])
    fmt = "bv*[height<=" + str(max_height) + "]+ba/b[height<=" + str(max_height) + "]/b"
    os.makedirs("clips", exist_ok=True)

    clips = []
    index = 0
    for video in videos:
        known = video.get("duration_seconds")
        if known is not None and known < duration:
            print("Skipping " + video["id"] + " (shorter than clip_duration)")
            continue

        index += 1
        prefix = "clips/clip_%03d" % index
        cmd = ytdlp_base() + [
            "--no-playlist", "--retries", "3",
            "--download-sections", "*0-" + str(duration),
            "--force-keyframes-at-cuts",
            "-f", fmt, "--merge-output-format", "mp4",
            "-o", prefix + ".%(ext)s",
            video["url"],
        ]
        print("Downloading clip " + str(index) + " from " + video["url"])
        try:
            result = subprocess.run(cmd, timeout=900)
            code = result.returncode
        except subprocess.TimeoutExpired:
            print("WARNING: download timed out for " + video["id"])
            code = 1

        files = [p for p in glob.glob(prefix + ".*") if not p.endswith((".part", ".ytdl"))]
        if code != 0 or not files:
            print("WARNING: download failed for " + video["id"])
            for leftover in glob.glob(prefix + ".*"):
                os.remove(leftover)
            index -= 1
            continue

        clips.append({
            "file": files[0],
            "source_video_id": video["id"],
            "source_url": video["url"],
        })
        print("Saved " + files[0])

    if not clips:
        print("ERROR: no clips were downloaded. See the warnings above.")
        print("If you see 'Sign in to confirm you are not a bot', add a valid YOUTUBE_COOKIES secret.")
        sys.exit(1)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump({"clips": clips}, f, indent=2)
        f.write("\n")
    print("Wrote " + MANIFEST_PATH + " (" + str(len(clips)) + " clips)")


if __name__ == "__main__":
    main()
