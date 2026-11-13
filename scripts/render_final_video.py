#!/usr/bin/env python3
import json
import os
import sys

CONFIG_PATH = "config/channel_config.json"
EDIT_LIST_PATH = "data/edit_list.json"
OUTPUT_PATH = "output/final_video.mp4"


def main():
    for required in (CONFIG_PATH, EDIT_LIST_PATH):
        if not os.path.exists(required):
            print("ERROR: missing " + required)
            sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    with open(EDIT_LIST_PATH, "r", encoding="utf-8") as f:
        edit_list = json.load(f)

    resolution = cfg["output_resolution"]
    fps = cfg["fps"]
    inputs = " ".join("-i " + c["file"] for c in edit_list["clips"])
    command = (
        "ffmpeg " + inputs
        + " -filter_complex concat=n=" + str(len(edit_list["clips"])) + ":v=1:a=0"
        + " -s " + resolution + " -r " + str(fps) + " " + OUTPUT_PATH
    )
    print("Mock ffmpeg command (not executed):")
    print(command)

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("MOCK FINAL VIDEO\n")
        f.write("resolution=" + resolution + "\n")
        f.write("fps=" + str(fps) + "\n")
        f.write("total_duration=" + str(edit_list["total_duration"]) + "\n")
        f.write("command=" + command + "\n")
    print("Wrote " + OUTPUT_PATH)


if __name__ == "__main__":
    main()
