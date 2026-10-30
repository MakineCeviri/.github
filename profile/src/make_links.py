"""Builds the link buttons, one SVG each so each is its own link. Square-cornered like the Launcher's buttons
(dialogRadius 4px); the download is the one gold button, as on the website. Discord, X, YouTube and Instagram marks
come from simple-icons (CC0).

Run: python profile/src/make_links.py  -> writes profile/assets/links/*.svg
"""
import re
import urllib.request

from common import GOLD, MUTED, PANEL, SANS, SRC, TEXT, font_face, logo_uri, text_width, write

H, ICON, PAD, SIZE = 38, 16, 14, 13
SIMPLE_ICONS = "https://cdn.jsdelivr.net/npm/simple-icons@16.36.0/icons/{}.svg"
LINKEDIN = ("M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414"
            "v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063"
            "-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9"
            "h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271"
            "V1.729C24 .774 23.2 0 22.222 0h.003z")  # simple-icons dropped LinkedIn; this is its former CC0 path
DOWNLOAD = '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'

LINKS = [  # (file, label, icon, primary)
    ("download", "Launcher'ı indirin", "download", True),
    ("site", "makineceviri.org", "logo", False),
    ("discord", "Discord", "si:discord", False),
    ("x", "@Makineceviri", "si:x", False),
    ("youtube", "YouTube", "si:youtube", False),
    ("instagram", "Instagram", "si:instagram", False),
    ("linkedin", "LinkedIn", "linkedin", False),
]


def icon(kind, x, y, color):
    s = ICON
    if kind == "logo":
        return f'<image href="{logo_uri()}" x="{x - 1}" y="{y - 1}" width="{s + 2}" height="{s + 2}"/>'
    if kind == "download":
        return f'<g transform="translate({x} {y}) scale({s / 24})" stroke="{color}">{DOWNLOAD}</g>'
    if kind == "linkedin":
        d = LINKEDIN
    else:
        with urllib.request.urlopen(SIMPLE_ICONS.format(kind[3:])) as r:
            d = re.search(r' d="([^"]+)"', r.read().decode()).group(1)
    k = .86 if kind == "si:x" else 1
    return (f'<path fill="{color}" transform="translate({x + s * (1 - k) / 2:.2f} {y + s * (1 - k) / 2:.2f}) '
            f'scale({s * k / 24:.4f})" d="{d}"/>')


def button(label, kind, primary):
    weight = 600 if primary else 500
    w = round(PAD + ICON + 9 + text_width(label, SIZE, weight) + PAD + 2)
    bg, fg, edge = (GOLD, PANEL, GOLD) if primary else (PANEL, TEXT, "rgba(222,218,212,.14)")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {H}" width="{w}" height="{H}" role="img" aria-label="{label}">
<style>
{font_face(weight, label)}
  text {{ font: {weight} {SIZE}px {SANS}; fill: {fg}; }}
</style>
<rect x=".5" y=".5" width="{w - 1}" height="{H - 1}" rx="4" fill="{bg}" stroke="{edge}"/>
{icon(kind, PAD, (H - ICON) / 2, PANEL if primary else MUTED)}
<text x="{PAD + ICON + 9}" y="{H / 2 + SIZE * .36:.2f}">{label}</text>
</svg>
"""


if __name__ == "__main__":
    for name, label, kind, primary in LINKS:
        write(SRC.parent / "assets" / "links", f"{name}.svg", button(label, kind, primary))
