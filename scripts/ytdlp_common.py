#!/usr/bin/env python3
import json
import os
import re
import sys

CONFIG_PATH = "config/channel_config.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("ERROR: missing " + CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_url(url):
    # A bare channel URL lists tabs; point it at the Videos tab instead.
    u = url.strip().rstrip("/")
    pattern = r"^https?://(www\.|m\.)?youtube\.com/(@[^/?]+|channel/[^/?]+|c/[^/?]+|user/[^/?]+)$"
    if re.match(pattern, u):
        u = u + "/videos"
    return u


def ytdlp_base():
    cmd = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node"]
    cookies = os.environ.get("YT_COOKIES_FILE", "")
    if cookies and os.path.exists(cookies):
        cmd += ["--cookies", cookies]
    return cmd


def collect_entries(data, out):
    if not isinstance(data, dict):
        return
    entries = data.get("entries")
    if entries:
        for entry in entries:
            collect_entries(entry, out)
    elif data.get("id") and data.get("_type", "video") in ("video", "url", "url_transparent"):
        out.append(data)


def entry_url(entry):
    url = entry.get("webpage_url") or entry.get("url") or ""
    if not url.startswith("http"):
        url = "https://www.youtube.com/watch?v=" + str(entry["id"])
    return url
