"""Builds the open-source cards: one wide card for Makine Launcher that also carries the section's title, and one
card per plugin repository, each its own SVG so each links to its repository. Stars and last-push dates are live.

Run: GH_TOKEN=... python profile/src/make_repos.py [out_dir]  -> writes repo-*.svg (default out_dir: profile/assets)
"""
import sys

from catalog import repos, tr_short
from common import FAINT, GOLD, MUTED, SRC, TEXT, brand_gradient, card, logo_uri, text_width, wrap, write

EASE = "cubic-bezier(.16,1,.3,1)"
LICENSE = "AGPL-3.0 + Commons Clause"
LANG = {"C++": "#f34b7d", "Python": "#3572A5", "JSON": "#cbcb41"}
LAUNCHER = ("Makine-Launcher", "Türkçe yamaları bulan, kuran ve kaldıran masaüstü uygulaması. Steam, Epic ve GOG "
            "kütüphanelerini tarar; Qt 6, QML ve C++23 ile yazıldı.", "C++")
PLUGINS = [
    ("Makine-LauncherPlugin-Live", "Ekrandaki metni gerçek zamanlı okur (OCR) ve çeviriyi oyunun üstünde gösterir.", "C++"),
    ("Makine-LauncherPlugin-Hook", "Oyun metnine dosyadan ve bellekten ulaşır: Unity, Unreal, Bethesda, GameMaker ve Ren'Py.", "C++"),
    ("Makine-LauncherPlugin-Template", "Kendi Launcher eklentinizi yazmanız için şablon: C ABI, manifest ve paketleme betiği.", "Python"),
    ("Makine-LauncherPlugins", "Resmî ve topluluk eklentilerinin kayıt defteri; her paket SHA-256 ile doğrulanır.", "JSON"),
]
GX, GY = 8, 6  # inner gutters of the 2x2 grid; outer edges stay flush with the wide card

CSS = f"""  .fade {{ animation: fade 1s {EASE} both; }}
  .h1 {{ font-size: 40px; font-weight: 800; letter-spacing: -.032em; }}
  .lead {{ font-size: 15px; fill: {MUTED}; }}
  .repo {{ font-size: 24px; font-weight: 700; letter-spacing: -.02em; }}
  .prepo {{ font-size: 18px; font-weight: 700; letter-spacing: -.015em; }}
  .desc {{ font-size: 15px; fill: {MUTED}; }}
  .pdesc {{ font-size: 14px; fill: {MUTED}; }}
  .meta {{ font-size: 12.5px; font-weight: 500; fill: {FAINT}; }}
  .star {{ fill: {GOLD}; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}"""


def meta(x, y, lang, info, show_stars):
    """Language dot, licence, stars (when there are any) and the last push, as one quiet line."""
    parts, cx = [], x
    parts.append(f'<circle cx="{cx + 5}" cy="{y - 4.5}" r="5" fill="{LANG[lang]}"/>')
    parts.append(f'<text x="{cx + 16}" y="{y}" class="meta">{lang}</text>')
    cx += 16 + text_width(lang, 12.5, 500) + 18
    parts.append(f'<text x="{cx}" y="{y}" class="meta">{LICENSE}</text>')
    cx += text_width(LICENSE, 12.5, 500) + 18
    if show_stars and info["stars"]:
        parts.append(f'<path transform="translate({cx} {y - 11.5}) scale(.58)" class="star" '
                     f'd="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17l-6.1 3.4 1.5-6.8L2.2 9l6.9-.7z"/>')
        parts.append(f'<text x="{cx + 18}" y="{y}" class="meta" style="fill:{TEXT}">{info["stars"]}</text>')
        cx += 18 + text_width(str(info["stars"]), 12.5, 500) + 18
    parts.append(f'<text x="{cx}" y="{y}" class="meta">güncellendi {tr_short(info["pushed"])}</text>')
    return "".join(parts)


def launcher(info):
    W, H = 1000, 344
    name, desc, lang = LAUNCHER
    lines = wrap(desc, 700, 15)
    lead = wrap("Launcher ve eklentileri GitHub'da açık; hata bildirimi ve katkı için depolara göz atabilirsiniz.", 330, 15)
    body = f"""  <g class="fade" style="animation-delay:.05s">
    <text x="38" y="86" class="h1">Açık kaynak</text>
    <text x="38" y="134" class="h1" style="fill:url(#brand)">Launcher ve eklentileri.</text>
  </g>
  <g class="fade" style="animation-delay:.2s">
    {"".join(f'<text x="{W - 370}" y="{102 + k * 24}" class="lead">{t}</text>' for k, t in enumerate(lead))}
  </g>
  <line x1="40" y1="176" x2="{W - 40}" y2="176" stroke="rgba(222,218,212,.1)"/>
  <g class="fade" style="animation-delay:.35s">
    <image href="{logo_uri()}" x="40" y="204" width="52" height="52"/>
    <text x="112" y="228" class="repo">{name}</text>
    {"".join(f'<text x="112" y="{256 + k * 22}" class="desc">{t}</text>' for k, t in enumerate(lines))}
    {meta(112, 256 + len(lines) * 22 + 14, lang, info, True)}
    <circle cx="{W - 66}" cy="226" r="20" fill="none" stroke="rgba(222,218,212,.14)"/>
    <path d="M{W - 71} 231l10 -10M{W - 69} 221h8v8" stroke="{GOLD}" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  </g>"""
    label = f"Açık kaynak: Launcher ve eklentileri. {name}: {desc} Lisans {LICENSE}, {info['stars']} yıldız."
    return card(W, H, body, label=label, defs=brand_gradient("brand", 40, 640), css=CSS, weights=[400, 500, 700, 800])


def plugin(i, name, desc, lang, info):
    W, H = 500, 196
    col, row = i % 2, i // 2
    x0, y0 = (GX if col else 0), (GY if row else 0)
    inset = (x0, y0, 0 if col else GX, 0 if row else GY)
    lines = wrap(desc, W - GX - 56, 14)
    d = .1 + i * .1
    body = f"""  <g class="fade" style="animation-delay:{d:.2f}s">
    <text x="{x0 + 26}" y="{y0 + 48}" class="prepo">{name}</text>
    {"".join(f'<text x="{x0 + 26}" y="{y0 + 80 + k * 21}" class="pdesc">{t}</text>' for k, t in enumerate(lines))}
    {meta(x0 + 26, y0 + 160, lang, info, True)}
  </g>"""
    label = f"{name}: {desc} {lang}, lisans {LICENSE}."
    return card(W, H, body, label=label, css=CSS, weights=[400, 500, 700], inset=inset)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else SRC.parent / "assets"
    info = repos()
    write(out, "repo-launcher.svg", launcher(info[LAUNCHER[0]]))
    for i, (name, desc, lang) in enumerate(PLUGINS):
        slug = {"Makine-LauncherPlugins": "registry"}.get(name, name.rsplit("-", 1)[-1].lower())
        write(out, f"repo-{slug}.svg", plugin(i, name, desc, lang, info[name]))
