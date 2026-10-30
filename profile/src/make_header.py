"""Builds the header: the question every visitor brings ("is there a Turkish patch?") and its answer with today's
count from the Launcher manifest, in the flowing brand gradient, over a slow brand-coloured sky.

Run: python profile/src/make_header.py [out_dir]  -> writes header.svg (default out_dir: profile/assets)
"""
import random
import sys

from catalog import manifest, tr_date
from common import BRAND, GOLD, MUTED, SRC, TEAL, TEXT, brand_gradient, card, logo_uri, text_width, wrap, write

W, H = 1000, 420
EASE = "cubic-bezier(.16,1,.3,1)"
LEAD = ("Makine Çeviri, kâr amacı gütmeyen ve gönüllülerle çalışan bir Türkçe oyun yerelleştirme topluluğu. Yamalar "
        "ücretsiz; Makine Launcher onları tek tıkla kurar ve önce değişecek dosyaların yedeğini alır.")


def sky(seed=4):
    rng = random.Random(seed)
    stars = "".join(f'<circle cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(0, H):.0f}" r="{rng.uniform(.5, 1.2):.1f}" '
                    f'class="star" style="animation-delay:-{rng.uniform(0, 6):.1f}s;animation-duration:{rng.uniform(3, 7):.1f}s"/>'
                    for _ in range(46))
    blobs = "".join(f'<ellipse class="blob" cx="{x}" cy="{y}" rx="{r}" ry="{r * .7:.0f}" fill="url(#b{i})" '
                    f'style="animation-duration:{d}s;animation-delay:-{i * 5}s"/>'
                    for i, (x, y, r, d) in enumerate([(130, 30, 360, 24), (860, 90, 320, 29), (760, 430, 380, 33)]))
    return blobs + stars


def svg(m):
    count, soon, newest = m["count"], m["soon"], m["recent"][0]["name"]
    line1, line2 = "Türkçe yaması var mı?", f"Launcher'da {count} tanesi hazır."
    size = min(58, 58 * 920 / text_width(line2, 58, 800, -.032))
    lead = wrap(LEAD, 700, 17)
    defs = (brand_gradient("brand", 40, 1040) + "".join(
        f'<radialGradient id="b{i}"><stop offset="0" stop-color="{c}" stop-opacity="{o}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
        for i, (c, o) in enumerate([(BRAND[0], .13), (BRAND[5], .10), (BRAND[3], .12)]))
        + f'<clipPath id="l1"><rect x="0" y="{148 - size}" width="{W}" height="{size * 1.25:.0f}"/></clipPath>'
        f'<clipPath id="l2"><rect x="0" y="{148 + size * .25:.0f}" width="{W}" height="{size * 1.28:.0f}"/></clipPath>')
    y1, y2 = 148, 148 + size * 1.12
    css = f"""  .blob {{ animation: drift ease-in-out infinite alternate; }}
  .star {{ fill: {TEXT}; animation: twinkle ease-in-out infinite alternate; }}
  .up {{ animation: up 1.15s {EASE} both; }}
  .fade {{ animation: fade 1s {EASE} both; }}
  .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2.4s ease-out infinite; }}
  .head {{ font-size: {size:.1f}px; font-weight: 800; letter-spacing: -.032em; }}
  .lead {{ font-size: 17px; fill: {MUTED}; }}
  .meta {{ font-size: 14px; font-weight: 500; fill: {MUTED}; }}
  .mark {{ font-size: 15px; letter-spacing: .14em; }}
  @keyframes drift {{ from {{ transform: translate(-30px, 12px); }} to {{ transform: translate(36px, -16px); }} }}
  @keyframes twinkle {{ from {{ opacity: .08; }} to {{ opacity: .45; }} }}
  @keyframes up {{ from {{ transform: translateY({size * 1.25:.0f}px); }} to {{ transform: translateY(0); }} }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes ping {{ from {{ transform: scale(.5); opacity: .9; }} to {{ transform: scale(1.9); opacity: 0; }} }}"""
    date = f"Katalog · {tr_date(m['generated'])}"
    count_w = text_width(f"{count} Türkçe yama", 14, 500)
    body = f"""  {sky()}
  <g class="fade" style="animation-delay:.05s">
    <image href="{logo_uri()}" x="38" y="30" width="32" height="32"/>
    <text x="80" y="52" class="mark"><tspan font-weight="800">MAKİNE</tspan><tspan font-weight="400" fill="{MUTED}"> ÇEVİRİ</tspan></text>
    <circle class="ping" cx="{W - 54 - text_width(date, 14, 500):.1f}" cy="47" r="6" fill="none" stroke="{TEAL}"/>
    <circle cx="{W - 54 - text_width(date, 14, 500):.1f}" cy="47" r="3.5" fill="{TEAL}"/>
    <text x="{W - 40}" y="52" text-anchor="end" class="meta">{date}</text>
  </g>
  <g clip-path="url(#l1)"><text x="37" y="{y1}" class="head up" style="animation-delay:.25s">{line1}</text></g>
  <g clip-path="url(#l2)"><text x="37" y="{y2:.0f}" class="head up" fill="url(#brand)" style="fill:url(#brand);animation-delay:.4s">{line2}</text></g>
  <g class="fade" style="animation-delay:.7s">
    {"".join(f'<text x="40" y="{y2 + 54 + k * 27:.0f}" class="lead">{t}</text>' for k, t in enumerate(lead))}
  </g>
  <line x1="40" y1="352" x2="{W - 40}" y2="352" stroke="rgba(222,218,212,.12)"/>
  <g class="fade" style="animation-delay:.95s">
    <text x="40" y="386" class="meta"><tspan fill="{GOLD}">{count} Türkçe yama</tspan>  ·  {soon} oyun yakında  ·  son eklenen: <tspan fill="{TEXT}">{newest}</tspan></text>
    <text x="{W - 40}" y="386" text-anchor="end" class="meta" fill="{TEXT}" style="fill:{TEXT}">makineceviri.org</text>
  </g>"""
    label = (f"Makine Çeviri. Türkçe yaması var mı? Launcher'da {count} tanesi hazır, {soon} oyun yakında; son eklenen {newest}. "
             + LEAD)
    return card(W, H, body, label=label, defs=defs, css=css, weights=[400, 500, 800])


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else SRC.parent / "assets", "header.svg", svg(manifest()))
