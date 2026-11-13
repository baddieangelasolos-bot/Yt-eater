#!/usr/bin/env python3
import json
import os
import sys

VIDEO_LIST_PATH = "data/video_list.json"


def main():
    if not os.path.exists(VIDEO_LIST_PATH):
        print("ERROR: missing " + VIDEO_LIST_PATH + " (run fetch_channel_videos.py first)")
        sys.exit(1)
    with open(VIDEO_LIST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    videos = data.get("videos", [])
    os.makedirs("clips", exist_ok=True)
    for index in (1, 2):
        source = videos[index - 1]["id"] if len(videos) >= index else "none"
        path = "clips/clip_%03d.mp4" % index
        with open(path, "w", encoding="utf-8") as f:
            f.write("MOCK CLIP " + str(index) + " from " + source + "\n")
        print("Wrote " + path)


if __name__ == "__main__":
    main()
