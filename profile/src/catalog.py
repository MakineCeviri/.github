"""The numbers the panels show, read from where they live: the Launcher's own manifest (the same file the Launcher
downloads, and the source the website counts from) and the GitHub API for the open-source repositories."""
import json
import os
import urllib.request
from datetime import datetime

MANIFEST = "https://cdn.makineceviri.org/assets/index.json"
REPOS = ["Makine-Launcher", "Makine-LauncherPlugin-Live", "Makine-LauncherPlugin-Hook", "Makine-LauncherPlugin-Template",
         "Makine-LauncherPlugins"]
MONTHS = "Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık".split()


def _get(url, token=None):
    headers = {"User-Agent": "MakineCeviri-profile"}
    if token:
        headers["Authorization"] = f"bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def manifest():
    """Patch count, the 'coming soon' count, the catalogue date and the newest patches (name, date, size)."""
    m = _get(MANIFEST)
    pkgs = sorted(m["packages"].values(), key=lambda p: p.get("v") or "", reverse=True)
    return dict(count=len(m["packages"]), soon=len(m.get("soon") or {}), generated=m["generatedAt"],
                recent=[dict(name=p["name"], date=(p.get("v") or "")[:10], size=p.get("sizeBytes") or 0) for p in pkgs])


def repos():
    """Stars and the last push date of each open-source repository."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    out = {}
    for r in REPOS:
        d = _get(f"https://api.github.com/repos/MakineCeviri/{r}", token)
        out[r] = dict(stars=d["stargazers_count"], pushed=d["pushed_at"][:10])
    return out


def tr_date(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def tr_short(day):
    """2026-10-27 -> 27 Eki"""
    y, m, d = (int(x) for x in day.split("-"))
    return f"{d} {MONTHS[m - 1][:3]}"


def size(n):
    """Binary units with one decimal, written the way the website and the Launcher write them (8.2 MB)."""
    for unit, k in (("GB", 1 << 30), ("MB", 1 << 20)):
        if n >= k:
            return f"{n / k:.1f} {unit}"
    return f"{max(n, 1) / 1024:.0f} KB"
