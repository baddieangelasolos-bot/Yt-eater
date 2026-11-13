#!/usr/bin/env python3
import json
import os
import sys

from ytdlp_common import load_config

MANIFEST_PATH = "data/clips_manifest.json"
OUTPUT_PATH = "data/edit_list.json"


def main():
    if not os.path.exists(MANIFEST_PATH):
        print("ERROR: missing " + MANIFEST_PATH + " (run download_clips.py first)")
        sys.exit(1)
    cfg = load_config()
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    duration = cfg["clip_duration"]
    clips = [{"file": c["file"], "start": 0, "duration": duration} for c in manifest["clips"]]
    edit_list = {"clips": clips, "total_duration": duration * len(clips)}

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(edit_list, f, indent=2)
        f.write("\n")
    print("Wrote " + OUTPUT_PATH + " (total_duration=" + str(edit_list["total_duration"]) + ")")


if __name__ == "__main__":
    main()
