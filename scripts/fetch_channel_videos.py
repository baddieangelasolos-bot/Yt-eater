#!/usr/bin/env python3
import json
import os
import sys

CONFIG_PATH = "config/channel_config.json"
OUTPUT_PATH = "data/video_list.json"


def main():
    if not os.path.exists(CONFIG_PATH):
        print("ERROR: missing " + CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    print("Reference channel: " + cfg["reference_channel_url"])
    videos = []
    for i, channel in enumerate(cfg["source_channels"], start=1):
        print("Source channel: " + channel)
        for j in (1, 2):
            videos.append({
                "id": "mock_%d_%d" % (i, j),
                "channel": channel,
                "title": "Mock video %d from source %d" % (j, i),
                "duration_seconds": 120,
            })

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"videos": videos}, f, indent=2)
        f.write("\n")
    print("Wrote " + OUTPUT_PATH + " (" + str(len(videos)) + " videos)")


if __name__ == "__main__":
    main()
