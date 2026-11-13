#!/usr/bin/env python3
import json
import os
import sys

CONFIG_PATH = "config/channel_config.json"
OUTPUT_PATH = "data/edit_list.json"


def main():
    if not os.path.exists(CONFIG_PATH):
        print("ERROR: missing " + CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    duration = cfg["clip_duration"]
    clips = []
    for index in (1, 2):
        clips.append({
            "file": "clips/clip_%03d.mp4" % index,
            "start": 0,
            "duration": duration,
        })

    edit_list = {"clips": clips, "total_duration": duration * len(clips)}

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(edit_list, f, indent=2)
        f.write("\n")
    print("Wrote " + OUTPUT_PATH + " (total_duration=" + str(edit_list["total_duration"]) + ")")


if __name__ == "__main__":
    main()
