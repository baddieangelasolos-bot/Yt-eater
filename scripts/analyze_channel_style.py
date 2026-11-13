#!/usr/bin/env python3
import json
import os
import sys

CONFIG_PATH = "config/channel_config.json"
OUTPUT_PATH = "data/style_profile.json"


def main():
    if not os.path.exists(CONFIG_PATH):
        print("ERROR: missing " + CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    profile = {
        "reference_channel_url": cfg["reference_channel_url"],
        "average_cut_length_seconds": 3.5,
        "dominant_transition": "hard_cut",
        "color_grade": "neutral",
        "music_style": "upbeat",
        "caption_style": "bottom_center_white",
    }

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
        f.write("\n")
    print("Wrote " + OUTPUT_PATH)


if __name__ == "__main__":
    main()
