#!/usr/bin/env python3
import json
import os
import subprocess
import sys

from ytdlp_common import collect_entries, entry_url, load_config, normalize_url, ytdlp_base

OUTPUT_PATH = "data/video_list.json"


def main():
    cfg = load_config()
    limit = int(cfg["videos_per_channel"])
    print("Reference channel: " + cfg["reference_channel_url"])

    videos = []
    for channel in cfg["source_channels"]:
        url = normalize_url(channel)
        print("Listing latest videos from: " + url)
        cmd = ytdlp_base() + [
            "--ignore-errors", "--flat-playlist", "-J",
            "--playlist-end", str(limit), url,
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        if not proc.stdout.strip():
            print("WARNING: no data returned for " + channel)
            continue
        try:
            data = json.loads(proc.stdout)
        except ValueError:
            print("WARNING: could not parse yt-dlp output for " + channel)
            continue

        found = []
        collect_entries(data, found)
        for entry in found[:limit]:
            duration = entry.get("duration")
            videos.append({
                "id": str(entry["id"]),
                "title": entry.get("title") or "",
                "url": entry_url(entry),
                "source": channel,
                "duration_seconds": duration,
            })
        print("Found " + str(len(found[:limit])) + " video(s)")

    if not videos:
        print("ERROR: no videos found for any source URL")
        sys.exit(1)

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"videos": videos}, f, indent=2)
        f.write("\n")
    print("Wrote " + OUTPUT_PATH + " (" + str(len(videos)) + " videos)")


if __name__ == "__main__":
    main()
