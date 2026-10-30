"""Builds 'Nasıl kurulur? / Üç adımda.': the website's three steps (HowItWorks.astro) on a rail that a gold line walks
along, step by step, lighting each one as it arrives.

Run: python profile/src/make_steps.py  -> writes profile/assets/steps.svg
"""
from common import BORDER, FAINT, GOLD, MUTED, SRC, TEAL, TEXT, brand_gradient, card, text_width, wrap, write

W, H = 1000, 452
EASE = "cubic-bezier(.16,1,.3,1)"
LEAD = ("Launcher oyununuzu bulur ve yamayı kurar, siz oyunu açarsınız. Kurmadan önce değişecek dosyaların yedeği alınır.")
STEPS = [
    ("Oyununuzu bulur", "Launcher, Steam, Epic ve GOG kütüphanelerinizi tarar ve Türkçe yaması olan oyunları listeler.",
     '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'),
    ("Yamayı kurar", 'Oyunun sayfasında "Türkçe Yama İndir"e basın. Launcher paketi indirir, değişecek dosyaların '
     'yedeğini alır ve yamayı kurar.',
     '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/>'),
    ("Siz oynarsınız", "Oyunu her zamanki gibi açın. Launcher'ın açık olması ya da internet bağlantısı gerekmez.",
     '<path d="M20 6 9 17l-5-5"/>'),
]
RAIL_Y, COL0, COL_W = 222, 40, 306  # rail height, first column, column pitch
CYCLE = 9.0


def svg():
    lead = wrap(LEAD, 330, 15)
    nodes, cols, frames = [], [], []
    n = len(STEPS)
    for i, (title, text, icon) in enumerate(STEPS):
        x = COL0 + i * COL_W
        on = 100 * i / n
        frames.append(f"@keyframes on{i} {{ 0%, {on:.1f}% {{ opacity: 0; }} {on + 3:.1f}% {{ opacity: 1; }} "
                      f"{on + 100 / n - 1:.1f}% {{ opacity: 1; }} {min(on + 100 / n + 3, 100):.1f}%, 100% {{ opacity: 0; }} }}")
        nodes.append(f'<circle cx="{x + 7}" cy="{RAIL_Y}" r="7" class="node"/>'
                     f'<circle cx="{x + 7}" cy="{RAIL_Y}" r="7" class="node-on" style="animation-name:on{i}"/>')
        body = wrap(text, COL_W - 40, 14.5)
        d = .45 + i * .14
        stroke = TEAL if i == n - 1 else MUTED
        cols.append(f'<g class="fade" style="animation-delay:{d:.2f}s">'
                    f'<rect x="{x}" y="{RAIL_Y + 30}" width="64" height="22" rx="4" class="chip"/>'
                    f'<rect x="{x}" y="{RAIL_Y + 30}" width="64" height="22" rx="4" class="chip-on" style="animation-name:on{i}"/>'
                    f'<text x="{x + 32}" y="{RAIL_Y + 45.5}" text-anchor="middle" class="chip-t">Adım 0{i + 1}</text>'
                    f'<g transform="translate({x + COL_W - 64} {RAIL_Y + 29}) scale(1)" fill="none" stroke="{stroke}" stroke-width="1.6" '
                    f'stroke-linecap="round" stroke-linejoin="round" opacity=".9">{icon}</g>'
                    f'<text x="{x}" y="{RAIL_Y + 90}" class="st">{title}</text>'
                    + "".join(f'<text x="{x}" y="{RAIL_Y + 118 + k * 22}" class="sx">{t}</text>' for k, t in enumerate(body))
                    + "</g>")
    rail_end = COL0 + (n - 1) * COL_W + 7
    defs = brand_gradient("brand", 40, 640) + f"""<linearGradient id="run" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".85" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>"""
    css = f"""  .fade {{ animation: fade 1s {EASE} both; }}
  .h1 {{ font-size: 44px; font-weight: 800; letter-spacing: -.032em; }}
  .lead {{ font-size: 15px; fill: {MUTED}; }}
  .rail {{ stroke: {BORDER}; stroke-width: 2; }}
  .walk {{ stroke: url(#run); stroke-width: 2; stroke-dasharray: 160 {rail_end * 2}; animation: walk {CYCLE}s linear infinite; }}
  .node {{ fill: #171C1E; stroke: rgba(222,218,212,.25); stroke-width: 1.5; }}
  .node-on, .chip-on {{ opacity: 0; animation-duration: {CYCLE}s; animation-iteration-count: infinite; animation-timing-function: ease-in-out; }}
  .node-on {{ fill: {GOLD}; stroke: {GOLD}; }}
  .chip {{ fill: rgba(222,218,212,.05); stroke: rgba(222,218,212,.14); }}
  .chip-on {{ fill: rgba(252,205,102,.14); stroke: rgba(252,205,102,.55); }}
  .chip-t {{ font-size: 11.5px; font-weight: 600; fill: {TEXT}; }}
  .st {{ font-size: 21px; font-weight: 600; letter-spacing: -.02em; }}
  .sx {{ font-size: 14.5px; fill: {MUTED}; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes walk {{ from {{ stroke-dashoffset: 160; }} to {{ stroke-dashoffset: -{rail_end - COL0:.0f}; }} }}
  {chr(10).join(frames)}"""
    body = f"""  <g class="fade" style="animation-delay:.05s">
    <text x="38" y="88" class="h1">Nasıl kurulur?</text>
    <text x="38" y="140" class="h1" style="fill:url(#brand)">Üç adımda.</text>
  </g>
  <g class="fade" style="animation-delay:.25s">
    {"".join(f'<text x="{W - 40 - 330}" y="{108 + k * 24}" class="lead">{t}</text>' for k, t in enumerate(lead))}
  </g>
  <line x1="{COL0 + 7}" y1="{RAIL_Y}" x2="{rail_end}" y2="{RAIL_Y}" class="rail"/>
  <line x1="{COL0 + 7}" y1="{RAIL_Y}" x2="{rail_end}" y2="{RAIL_Y}" class="walk"/>
  {"".join(nodes)}
  {"".join(cols)}"""
    label = "Nasıl kurulur? Üç adımda. " + LEAD + " " + " ".join(f"Adım {i + 1}, {t}: {x}" for i, (t, x, _) in enumerate(STEPS))
    return card(W, H, body, label=label, defs=defs, css=css, weights=[400, 600, 800])


if __name__ == "__main__":
    write(SRC.parent / "assets", "steps.svg", svg())
