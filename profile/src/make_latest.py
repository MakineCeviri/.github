"""Builds the 'newest patches' panel: the Launcher's library window with the five most recent patches from the
manifest, each row installing in turn (its check draws as it lands). Real data only, refreshed daily.

Run: python profile/src/make_latest.py [out_dir]  -> writes latest.svg (default out_dir: profile/assets)
"""
import html
import sys

from catalog import manifest, size, tr_short
from common import BORDER, FAINT, GOLD, GREEN, MUTED, SRC, SUNK, SURFACE, TEXT, card, logo_uri, text_width, write

W, H, ROWS = 1000, 440, 5
EASE = "cubic-bezier(.16,1,.3,1)"
WX, WY, WW = 40, 96, W - 80  # the window
ROW_Y, ROW_H = 234, 34
SIZE_X, DATE_X = 760, 920


def rows(recent):
    out = []
    for i, p in enumerate(recent[:ROWS]):
        y = ROW_Y + i * ROW_H
        d = .5 + i * .16
        new = '<rect x="0" y="-12" width="34" height="18" rx="4" class="chip"/><text x="17" y="1" text-anchor="middle" class="chip-t">Yeni</text>'
        name = html.escape(p["name"])
        out.append(f'<g class="row" style="animation-delay:{d:.2f}s">'
                   + (f'<rect x="{WX + 1}" y="{y - 22}" width="{WW - 2}" height="{ROW_H}" class="hl"/>' if i == 0 else "")
                   + f'<circle cx="{WX + 34}" cy="{y - 5}" r="9" class="ring"/>'
                   f'<path d="M{WX + 29.5} {y - 5}l3 3l6 -6" class="tick" style="animation-delay:{d + .35:.2f}s"/>'
                   f'<text x="{WX + 58}" y="{y}" class="name">{name}</text>'
                   + (f'<g transform="translate({WX + 70 + text_width(p["name"], 15, 500):.0f} {y})">{new}</g>' if i == 0 else "")
                   + f'<text x="{SIZE_X}" y="{y}" text-anchor="end" class="cell">{size(p["size"])}</text>'
                   f'<text x="{DATE_X}" y="{y}" text-anchor="end" class="cell">{tr_short(p["date"])}</text>'
                   f'<line x1="{WX + 20}" y1="{y + 12}" x2="{WX + WW - 20}" y2="{y + 12}" class="sep"/></g>')
    return "\n  ".join(out)


def svg(m):
    defs = f"""<linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SURFACE}"/><stop offset="1" stop-color="{SUNK}"/></linearGradient>
  <clipPath id="window"><rect x="{WX}" y="{WY}" width="{WW}" height="{H - WY - 32}" rx="12"/></clipPath>"""
    css = f"""  .fade {{ animation: fade 1s {EASE} both; }}
  .row {{ animation: fade .8s {EASE} both; }}
  .tick {{ fill: none; stroke: {GREEN}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 14; stroke-dashoffset: 14; animation: tick .5s {EASE} forwards; }}
  .ring {{ fill: rgba(128,229,157,.08); stroke: rgba(128,229,157,.35); stroke-width: 1; }}
  .hl {{ fill: rgba(252,205,102,.05); }}
  .chip {{ fill: rgba(252,205,102,.12); stroke: rgba(252,205,102,.4); stroke-width: 1; }}
  .chip-t {{ font-size: 11px; font-weight: 600; fill: {GOLD}; }}
  .title {{ font-size: 26px; font-weight: 700; letter-spacing: -.02em; }}
  .note {{ font-size: 14px; fill: {MUTED}; }}
  .bar {{ font-size: 12.5px; font-weight: 500; fill: {MUTED}; }}
  .lib {{ font-size: 15px; font-weight: 600; }}
  .th {{ font-size: 11px; font-weight: 600; letter-spacing: .14em; fill: {FAINT}; }}
  .name {{ font-size: 15px; font-weight: 500; fill: {TEXT}; }}
  .cell {{ font-size: 14px; fill: {MUTED}; }}
  .sep {{ stroke: rgba(222,218,212,.06); }}
  .glyph {{ stroke: {MUTED}; stroke-width: 1.2; fill: none; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes tick {{ to {{ stroke-dashoffset: 0; }} }}"""
    gx = WX + WW - 22  # Windows caption glyphs, right to left: close, maximise, minimise
    body = f"""  <g class="fade" style="animation-delay:.05s">
    <text x="40" y="62" class="title">Launcher'a yeni eklenenler</text>
    <text x="{W - 40}" y="62" text-anchor="end" class="note">Liste her gün Launcher kataloğundan güncellenir</text>
  </g>
  <g class="fade" style="animation-delay:.2s">
    <rect x="{WX}" y="{WY}" width="{WW}" height="{H - WY - 32}" rx="12" fill="url(#win)" stroke="{BORDER}"/>
    <g clip-path="url(#window)">
      <rect x="{WX}" y="{WY}" width="{WW}" height="36" fill="rgba(255,255,255,.015)"/>
      <line x1="{WX}" y1="{WY + 36}" x2="{WX + WW}" y2="{WY + 36}" stroke="{BORDER}"/>
    </g>
    <image href="{logo_uri()}" x="{WX + 16}" y="{WY + 10}" width="16" height="16"/>
    <text x="{WX + 40}" y="{WY + 23}" class="bar">Makine Launcher</text>
    <path d="M{gx - 4} {WY + 14}l8 8M{gx + 4} {WY + 14}l-8 8" class="glyph"/>
    <rect x="{gx - 40}" y="{WY + 14}" width="8" height="8" class="glyph"/>
    <path d="M{gx - 76} {WY + 18}h9" class="glyph"/>
    <text x="{WX + 20}" y="{WY + 70}" class="lib">Yama kütüphanesi <tspan class="cell" font-weight="400">({m['count']} yama)</tspan></text>
    <text x="{WX + 58}" y="{ROW_Y - 34}" class="th">OYUN</text>
    <text x="{SIZE_X}" y="{ROW_Y - 34}" text-anchor="end" class="th">BOYUT</text>
    <text x="{DATE_X}" y="{ROW_Y - 34}" text-anchor="end" class="th">TARİH</text>
  </g>
  {rows(m["recent"])}"""
    names = ", ".join(f"{p['name']} ({tr_short(p['date'])})" for p in m["recent"][:ROWS])
    label = f"Launcher'a yeni eklenenler. Yama kütüphanesi, {m['count']} yama. En yeniler: {names}."
    return card(W, H, body, label=label, defs=defs, css=css, weights=[400, 500, 600, 700])


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else SRC.parent / "assets", "latest.svg", svg(manifest()))
