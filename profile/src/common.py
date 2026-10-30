"""Shared look for the profile panels, taken from Makine Launcher (Theme.qml) as the website does: the nine-stop brand
gradient, gold for the main accent, teal for live data, #171C1E containers, Montserrat embedded as a subset (an SVG
shown through <img> cannot load fonts of its own). Every number on a panel is read from a real source (catalog.py).
"""
import base64
import html
import io
import re
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

SRC = Path(__file__).parent

BRAND = ["#FCCD66", "#F7AE76", "#EE968F", "#CC9FD8", "#90C2E6", "#77DBC8", "#80E59D", "#C8EB7C", "#D4BE77"]
GOLD, TEAL, GREEN = "#FCCD66", "#77DBC8", "#80E59D"
PANEL, SUNK, SURFACE = "#171C1E", "#0d0d11", "#121216"
TEXT, MUTED, FAINT = "#dedad4", "#A1A1AA", "#7d7a73"
BORDER, BORDER_LIGHT = "#262632", "rgba(222,218,212,.12)"

SANS = "'Makine Sans', Montserrat, 'Segoe UI', sans-serif"


@lru_cache(None)
def _static(weight):
    return instancer.instantiateVariableFont(TTFont(SRC / "fonts" / "Montserrat[wght].ttf"), {"wght": weight})


def text_width(text, size, weight=500, tracking=0):
    """Advance width of one line in px; tracking in em, as in CSS letter-spacing."""
    ft = _static(weight)
    cmap, hmtx, upm = ft.getBestCmap(), ft["hmtx"], ft["head"].unitsPerEm
    return sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in text) * size / upm + len(text) * tracking * size


def font_face(weight, text):
    buf = io.BytesIO()
    _static(weight).save(buf)
    buf.seek(0)
    ft = TTFont(buf)
    opts = subset.Options()
    opts.flavor, opts.layout_features, opts.name_IDs = "woff2", ["kern", "liga", "tnum"], []
    sub = subset.Subsetter(opts)
    sub.populate(text=text + " ")
    sub.subset(ft)
    out = io.BytesIO()
    ft.flavor = "woff2"
    ft.save(out)
    return (f"@font-face {{ font-family: 'Makine Sans'; font-weight: {weight}; "
            f"src: url(data:font/woff2;base64,{base64.b64encode(out.getvalue()).decode()}) format('woff2'); }}")


def text_of(svg):
    runs = re.findall(r"<text\b[^>]*>(.*?)</text>", svg, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", "".join(runs)))


def wrap(text, width, size, weight=400):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and text_width(trial, size, weight) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def brand_gradient(gid, x1, x2, seconds=22):
    """The brand gradient as a repeating loop that flows sideways, like the website's .metallic-text."""
    period = x2 - x1
    stops = BRAND + BRAND[:1]
    s = "".join(f'<stop offset="{k / (len(stops) - 1):.4f}" stop-color="{c}"/>' for k, c in enumerate(stops))
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="0" x2="{x2}" y2="0" spreadMethod="repeat">{s}'
            f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{period} 0" dur="{seconds}s" '
            f'repeatCount="indefinite"/></linearGradient>')


def logo_uri():
    return "data:image/webp;base64," + base64.b64encode((SRC / "logo.webp").read_bytes()).decode()


GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%">'
         '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 .87  0 0 0 0 .85  0 0 0 0 .83  0 0 0 .05 0"/></filter>')


def card(w, h, body, *, label, weights, defs="", css="", radius=16, inset=0, background=PANEL):
    """A rounded container with a hairline edge and a fine grain. inset (one number, or left, top, right, bottom)
    leaves a transparent gutter, so cards set edge to edge in the README still read as separate cards."""
    left, top, right, bottom = inset if isinstance(inset, tuple) else (inset,) * 4
    x0, y0, cw, ch = left, top, w - left - right, h - top - bottom
    chars = text_of(body)
    upper = chars.upper().replace("I", "Iİ")
    style = "\n".join(font_face(wt, chars + upper) for wt in weights)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(label)}">
<title>{html.escape(label)}</title>
<defs>
  <clipPath id="card"><rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="{radius}"/></clipPath>
  {GRAIN}
  {defs}
</defs>
<style>
{style}
  text {{ font-family: {SANS}; fill: {TEXT}; font-variant-numeric: tabular-nums; }}
  .muted {{ fill: {MUTED}; }} .faint {{ fill: {FAINT}; }} .gold {{ fill: {GOLD}; }} .teal {{ fill: {TEAL}; }}
{css}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation-duration: 1ms !important; animation-delay: 0s !important;
    animation-iteration-count: 1 !important; }} }}
</style>
<g clip-path="url(#card)">
  <rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" fill="{background}"/>
{body}
  <rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" filter="url(#grain)"/>
</g>
<rect x="{x0 + .5}" y="{y0 + .5}" width="{cw - 1}" height="{ch - 1}" rx="{radius - .5}" fill="none" stroke="{BORDER_LIGHT}"/>
</svg>
"""


def write(out, name, svg):
    path = Path(out) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    assert "—" not in svg, f"{name}: no em dash in Makine copy"
    print(f"{name}: {len(svg.encode()) / 1024:.0f} KB")
