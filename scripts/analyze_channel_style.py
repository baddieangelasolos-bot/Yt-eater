#!/usr/bin/env python3
import json
import os
import subprocess

from ytdlp_common import collect_entries, load_config, normalize_url, ytdlp_base

OUTPUT_PATH = "data/style_profile.json"


def main():
    cfg = load_config()
    url = normalize_url(cfg["reference_channel_url"])
    print("Sampling reference channel: " + url)

    durations = []
    cmd = ytdlp_base() + ["--ignore-errors", "--flat-playlist", "-J", "--playlist-end", "10", url]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    if proc.stdout.strip():
        try:
            found = []
            collect_entries(json.loads(proc.stdout), found)
            durations = [e["duration"] for e in found if e.get("duration")]
        except ValueError:
            print("WARNING: could not parse reference channel data")
    else:
        print("WARNING: no data returned for the reference channel")

    average = round(sum(durations) / len(durations), 1) if durations else None
    profile = {
        "reference_channel_url": cfg["reference_channel_url"],
        "sample_size": len(durations),
        "average_video_duration_seconds": average,
        "note": "Visual style analysis (cuts, color, captions) is not implemented yet.",
    }

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
        f.write("\n")
    print("Wrote " + OUTPUT_PATH)


if __name__ == "__main__":
    main()
