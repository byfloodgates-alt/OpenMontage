"""Generate the blocky-game pasta composition (index.html). Usage: build_blocky.py <out.html>"""
import sys

INK = "#1d1d1d"
SW = 'stroke="#1d1d1d" stroke-width="6" stroke-linejoin="round"'

S = [0, 3.0, 7.0, 11.2, 15.4, 20.0, 24.2]
D = [3.0, 4.0, 4.2, 4.2, 4.6, 4.2, 5.8]
TC = [None, 2.9, 2.6, 2.7, 3.2, 2.8, 2.7]  # step-complete offsets (match SFX)

def block(x, y, w, h, front, side, top, d=40, extra="", id_=""):
    """Faux-3D block: front rect + right side + top face, depth d (up-right)."""
    idattr = f' id="{id_}"' if id_ else ""
    return f'''<g{idattr} {extra}>
  <polygon points="{x+w},{y} {x+w+d},{y-d} {x+w+d},{y+h-d} {x+w},{y+h}" fill="{side}" {SW}/>
  <polygon points="{x},{y} {x+d},{y-d} {x+w+d},{y-d} {x+w},{y}" fill="{top}" {SW}/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{front}" {SW}/>
</g>'''

def stove(p):
    flames = ""
    cols = ["#ff6a00", "#ffc400", "#ff6a00", "#ffc400", "#ff6a00"]
    for k, cx in enumerate([520, 600, 680, 760, 840]):
        flames += f'<rect id="{p}-f{k}" x="{cx}" y="806" width="40" height="44" fill="{cols[k]}" {SW}/>'
    return block(440, 850, 500, 40, "#4a4a4a", "#2f2f2f", "#6a6a6a", d=30) + flames

def pot(p, water=True):
    w = ('<polygon points="492,596 538,570 906,570 860,596" fill="#45b4f0" stroke="#1d1d1d" stroke-width="4"/>' if water else "")
    return f'''<g id="{p}-pot">
  <rect x="425" y="640" width="45" height="34" fill="#7d93a6" {SW}/>
  {block(470, 600, 400, 200, "#a9bccb", "#7d93a6", "#cfdbe5", d=40)}
  {w}
  <rect x="495" y="625" width="26" height="150" fill="#e6eef4" opacity="0.7"/>
</g>'''

def avatar():
    return f'''<g id="av">
  <g id="av-legs">
    <rect x="152" y="760" width="56" height="130" fill="#2d4a8a" {SW}/>
    <rect x="214" y="760" width="56" height="130" fill="#2d4a8a" {SW}/>
  </g>
  <g id="av-body">
    {block(130, 600, 160, 170, "#ffffff", "#d9d9d9", "#f2f2f2", d=22)}
    <rect x="152" y="640" width="116" height="130" fill="#e2452c" {SW}/>
    <rect x="186" y="680" width="48" height="34" fill="#c22f1a" {SW}/>
  </g>
  <g id="av-larm"><rect x="84" y="604" width="46" height="150" fill="#ffd9a8" {SW}/><rect x="84" y="604" width="46" height="50" fill="#ffffff" {SW}/></g>
  <g id="av-rarm"><rect x="290" y="604" width="46" height="150" fill="#ffd9a8" {SW}/><rect x="290" y="604" width="46" height="50" fill="#ffffff" {SW}/></g>
  <g id="av-head">
    {block(140, 462, 140, 134, "#ffd9a8", "#e8b985", "#ffe7c7", d=22)}
    <rect x="172" y="505" width="20" height="30" fill="{INK}"/>
    <rect x="228" y="505" width="20" height="30" fill="{INK}"/>
    <path d="M180 556 q30 24 60 0" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
    <g id="av-hat">
      <rect x="146" y="420" width="128" height="44" fill="#ffffff" {SW}/>
      <rect x="138" y="352" width="62" height="72" fill="#ffffff" {SW}/>
      <rect x="190" y="330" width="62" height="94" fill="#ffffff" {SW}/>
      <rect x="240" y="352" width="54" height="72" fill="#ffffff" {SW}/>
    </g>
  </g>
</g>'''

def scene(i, art, step, title, chat):
    steplabel = f'<span class="step">STEP {step}/6</span>' if step else '<span class="step gold">NEW QUEST</span>'
    return f'''
      <section id="s{i}" class="clip scene" data-start="{S[i]}" data-duration="{D[i]}" data-track-index="1">
        <div class="wrap" id="s{i}-wrap">
          <svg class="world" id="s{i}-art" viewBox="0 0 1080 990">{art}</svg>
          <div class="copy" id="s{i}-copy">
            {steplabel}
            <span class="title" id="s{i}-title">{title}</span>
          </div>
          <div class="chat" id="s{i}-chat"><span class="who">ChefBlox:</span> {chat}</div>
          <div class="xp" id="s{i}-xp">+50 XP</div>
        </div>
      </section>'''

# ---------- per-scene art ----------
rays = "".join(
    f'<polygon points="700,560 {700+600*__import__("math").cos(a)},{560+600*__import__("math").sin(a)} {700+600*__import__("math").cos(a+0.2)},{560+600*__import__("math").sin(a+0.2)}" fill="#fff6b0" opacity="0.55"/>'
    for a in [k * 0.5236 for k in range(12)]
)
art0 = f'''
<g id="s0-rays">{rays}</g>
<g id="s0-item">
  {block(540, 560, 300, 150, "#f2f2f2", "#cfcfcf", "#ffffff", d=40)}
  <rect x="560" y="500" width="22" height="80" fill="#f5c24c" {SW}/>
  <rect x="600" y="480" width="22" height="100" fill="#f5c24c" {SW}/>
  <rect x="640" y="495" width="22" height="85" fill="#f5c24c" {SW}/>
  <rect x="740" y="490" width="22" height="90" fill="#f5c24c" {SW}/>
  <rect x="780" y="505" width="22" height="75" fill="#f5c24c" {SW}/>
  {block(660, 470, 80, 80, "#e2452c", "#b8301c", "#ff6a52", d=24)}
  <rect x="690" y="430" width="30" height="40" fill="#3f9d3a" {SW}/>
</g>
<rect x="560" y="620" width="260" height="22" fill="#4aa8e8" {SW}/>
'''

steam1 = "".join(f'<rect id="s1-st{k}" x="{x}" y="470" width="34" height="34" fill="#ffffff" opacity="0.85" {SW}/>' for k, x in enumerate([560, 680, 800]))
bub1 = "".join(f'<rect id="s1-b{k}" x="{x}" y="{y}" width="22" height="22" fill="#ffffff" stroke="#1d1d1d" stroke-width="4"/>' for k, (x, y) in enumerate([(560, 575), (640, 580), (720, 574), (800, 580), (680, 584)]))
art1 = stove("s1") + pot("s1") + bub1 + steam1

grains = "".join(f'<rect id="s2-g{k}" x="{x}" y="300" width="18" height="18" fill="#ffffff" stroke="#1d1d1d" stroke-width="4"/>' for k, x in enumerate([650, 680, 705, 665, 695, 720]))
art2 = stove("s2") + pot("s2") + grains + f'''
<g id="s2-shaker">
  {block(620, 150, 110, 160, "#ffffff", "#d0d0d0", "#f4f4f4", d=26)}
  {block(620, 110, 110, 40, "#a9bccb", "#7d93a6", "#cfdbe5", d=26)}
  <rect x="648" y="190" width="54" height="80" fill="#e8e8e8" {SW}/>
  <text x="675" y="252" text-anchor="middle" font-family="Lilita One" font-size="64" fill="#e2452c">S</text>
</g>
<text id="s2-flavor" x="330" y="250" text-anchor="middle" font-family="Lilita One" font-size="70" fill="#7dff6a" stroke="#1d1d1d" stroke-width="10" paint-order="stroke">+10 FLAVOR</text>
'''

sticks = "".join(f'<rect x="{x}" y="250" width="20" height="330" fill="#f5c24c" {SW} transform="rotate({r} {x+10} 415)"/>' for x, r in [(600, -12), (640, -6), (680, 0), (720, 5), (760, 11)])
art3 = stove("s3") + f'<g id="s3-sticks">{sticks}</g>' + pot("s3", water=False) + f'''
<g id="s3-spoon">
  <rect x="850" y="330" width="30" height="300" fill="#b9773e" {SW}/>
  {block(830, 300, 70, 60, "#b9773e", "#8f5a2c", "#d08b4f", d=18)}
</g>
'''

art4 = f'''
<g id="s4-box">
  {block(480, 300, 300, 520, "#e2452c", "#b8301c", "#ff6a52", d=50)}
  <rect x="505" y="330" width="250" height="90" fill="#ffffff" {SW}/>
  <text x="630" y="392" text-anchor="middle" font-family="Lilita One" font-size="52" fill="#1d1d1d">SPAGHETTI</text>
  <g fill="#f5c24c" stroke="#1d1d1d" stroke-width="4">
    <rect x="525" y="450" width="16" height="140"/><rect x="560" y="450" width="16" height="140"/><rect x="595" y="450" width="16" height="140"/>
    <rect x="630" y="450" width="16" height="140"/><rect x="665" y="450" width="16" height="140"/><rect x="700" y="450" width="16" height="140"/>
  </g>
  <rect x="505" y="630" width="250" height="160" fill="#1d1d1d" {SW}/>
  <text id="s4-t10" x="630" y="740" text-anchor="middle" font-family="Lilita One" font-size="92" fill="#ff5b5b">10:00</text>
  <text id="s4-t9" x="630" y="740" text-anchor="middle" font-family="Lilita One" font-size="92" fill="#7dff6a">9:00</text>
</g>
<g id="s4-badge">
  <rect x="390" y="150" width="480" height="100" rx="18" fill="#ffd23f" {SW}/>
  <text x="630" y="218" text-anchor="middle" font-family="Lilita One" font-size="54" fill="#1d1d1d">AL DENTE UNLOCKED</text>
</g>
'''

art5 = f'''
<g id="s5-mug">
  <rect x="800" y="600" width="70" height="40" fill="#ffffff" {SW}/>
  <rect x="840" y="600" width="40" height="160" fill="#ffffff" {SW}/>
  <rect x="800" y="720" width="70" height="40" fill="#ffffff" {SW}/>
  {block(540, 560, 260, 330, "#ffffff", "#d6d6d6", "#f4f4f4", d=36)}
  <g clip-path="url(#s5-clip)"><rect id="s5-fill" x="546" y="600" width="248" height="284" fill="#ead9b0"/></g>
  <defs><clipPath id="s5-clip"><rect x="546" y="566" width="248" height="318"/></clipPath></defs>
</g>
<g transform="translate(0 -75)"><g id="s5-card">
  <rect x="380" y="90" width="560" height="380" rx="26" fill="#2a1f4a" stroke="#ffd23f" stroke-width="12"/>
  <text x="660" y="160" text-anchor="middle" font-family="Lilita One" font-size="44" fill="#ffd23f">LEGENDARY ITEM</text>
  {block(600, 210, 110, 130, "#ead9b0", "#c9b48a", "#f6ead0", d=24)}
  <text x="660" y="420" text-anchor="middle" font-family="Lilita One" font-size="52" fill="#ffffff">Pasta Water</text>
</g></g>
'''

conf_cols = ["#e2452c", "#ffd23f", "#45b4f0", "#7dff6a", "#ff7ad9", "#ffffff"]
confetti = "".join(
    f'<rect id="s6-c{k}" x="690" y="520" width="26" height="26" fill="{conf_cols[k % 6]}" stroke="#1d1d1d" stroke-width="4"/>'
    for k in range(14)
)
art6 = f'''
<g id="s6-toss">
  <rect x="580" y="560" width="22" height="90" fill="#f5c24c" {SW} transform="rotate(-25 591 605)"/>
  <rect x="630" y="540" width="22" height="100" fill="#f5c24c" {SW} transform="rotate(15 641 590)"/>
  <rect x="690" y="550" width="22" height="95" fill="#f5c24c" {SW} transform="rotate(-10 701 597)"/>
  <rect x="750" y="545" width="22" height="100" fill="#f5c24c" {SW} transform="rotate(30 761 595)"/>
  {block(640, 560, 90, 70, "#e2452c", "#b8301c", "#ff6a52", d=22)}
</g>
<g id="s6-pan">
  <rect x="910" y="760" width="150" height="34" fill="#2f2f2f" {SW}/>
  {block(470, 720, 440, 110, "#3a3a3a", "#262626", "#555555", d=40)}
  <polygon points="495,716 535,688 885,688 845,716" fill="#e2452c" stroke="#1d1d1d" stroke-width="4"/>
</g>
{confetti}
'''

SCENES = [
    (art0, 0, "COOK THE<br>PERFECT PASTA", "Yo! New quest unlocked. Cook the perfect pasta!"),
    (art1, 1, "BOIL THE WATER", "Fill a big pot and bring it to a rolling boil."),
    (art2, 2, "SALT IT!", "Salt the water. Generously! +10 flavor."),
    (art3, 3, "ADD + STIR", "Drop in the pasta and stir so it doesn't stick."),
    (art4, 4, "1 MIN LESS", "Cook 1 minute less than the box says."),
    (art5, 5, "SAVE THE WATER", "Save a mug of pasta water. Secret item!"),
    (art6, 6, "TOSS WITH SAUCE", "Toss with sauce + a splash of that water."),
]

clouds = ""
for k, (x, y, s) in enumerate([(80, 330, 1.0), (640, 240, 1.3), (380, 520, 0.8)]):
    clouds += f'''<div class="cloud" id="cl{k}" style="left:{x}px;top:{y}px;width:{int(260*s)}px;height:{int(110*s)}px">
      <i style="left:0;top:{int(40*s)}px;width:{int(260*s)}px;height:{int(70*s)}px"></i>
      <i style="left:{int(50*s)}px;top:0;width:{int(110*s)}px;height:{int(80*s)}px"></i>
      <i style="left:{int(140*s)}px;top:{int(15*s)}px;width:{int(80*s)}px;height:{int(70*s)}px"></i></div>'''

counters = "".join(f'<span class="qn" id="q{k}">{k}/6</span>' for k in range(7))

html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Pasta Quest</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Lilita One"; src: url("assets/fonts/LilitaOne.ttf") format("truetype"); }}
      @font-face {{ font-family: "Fredoka"; font-weight: 700; src: url("assets/fonts/Fredoka-700.ttf") format("truetype"); }}
      body {{ margin: 0; background: #5fc4ff; font-family: "Fredoka", sans-serif; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .bg {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .sky {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1150px; background: linear-gradient(#3fb0ff, #9fdcff 70%, #c9ecff); }}
      .ground {{ position: absolute; left: 0; top: 1150px; width: 1080px; height: 770px;
        background-color: #4cb848;
        background-image: radial-gradient(circle at 50% 45%, #6fd16a 0 13px, #3c9a39 14px 17px, transparent 18px);
        background-size: 54px 54px; border-top: 10px solid #2f7d2c; box-sizing: border-box; }}
      .cloud {{ position: absolute; display: block; }}
      .cloud i {{ position: absolute; display: block; background: #ffffff; border: 6px solid #1d1d1d; box-sizing: border-box; }}
      .hud {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .quest {{ position: absolute; left: 50px; right: 50px; top: 60px; height: 170px; box-sizing: border-box;
        background: rgba(20, 20, 35, 0.78); border: 6px solid #1d1d1d; border-radius: 26px; padding: 22px 32px; }}
      .qtitle {{ display: block; font-family: "Lilita One"; font-size: 52px; color: #ffd23f; letter-spacing: 1px; }}
      .qbar {{ position: absolute; left: 32px; right: 170px; bottom: 26px; height: 40px; background: #3a3a55; border: 5px solid #1d1d1d; border-radius: 12px; overflow: hidden; }}
      .qfill {{ position: absolute; left: 0; top: 0; display: block; width: 100%; height: 100%; background: linear-gradient(#8dff7a, #3fcf3a); }}
      .qn {{ position: absolute; right: 32px; bottom: 18px; display: block; width: 120px; text-align: right; font-family: "Lilita One"; font-size: 54px; color: #ffffff; }}
      .lvl {{ position: absolute; right: 32px; top: 22px; display: block; font-family: "Lilita One"; font-size: 40px; color: #1d1d1d; background: #7dff6a; border: 5px solid #1d1d1d; border-radius: 14px; padding: 2px 16px; }}
      .avwrap {{ position: absolute; left: 0; top: 260px; width: 1080px; height: 990px; }}
      .world {{ position: absolute; left: 0; top: 260px; display: block; width: 1080px; height: 990px; }}
      .avwrap svg {{ display: block; width: 1080px; height: 990px; }}
      .scene, .wrap {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      .copy {{ position: absolute; left: 40px; right: 40px; top: 1290px; height: 260px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
      .step {{ display: block; font-family: "Lilita One"; font-size: 40px; color: #1d1d1d; background: #ffffff; border: 5px solid #1d1d1d; border-radius: 14px; padding: 4px 22px; }}
      .step.gold {{ background: #ffd23f; }}
      .title {{ display: block; margin-top: 18px; font-family: "Lilita One"; font-size: 118px; line-height: 0.95; color: #ffffff;
        text-shadow: 6px 0 0 #1d1d1d, -6px 0 0 #1d1d1d, 0 6px 0 #1d1d1d, 0 -6px 0 #1d1d1d, 5px 5px 0 #1d1d1d, -5px 5px 0 #1d1d1d, 5px -5px 0 #1d1d1d, -5px -5px 0 #1d1d1d, 0 14px 0 #1d1d1d; }}
      #s0 .title {{ color: #ffd23f; font-size: 104px; }}
      .chat {{ position: absolute; left: 60px; right: 60px; top: 1600px; box-sizing: border-box; padding: 26px 34px;
        background: rgba(15, 15, 28, 0.8); border: 6px solid #1d1d1d; border-radius: 24px; font-size: 46px; line-height: 1.25; color: #ffffff; }}
      .who {{ color: #6fd3ff; }}
      .xp {{ position: absolute; left: 0; right: 0; top: 700px; display: block; text-align: center; font-family: "Lilita One"; font-size: 96px; color: #7dff6a;
        text-shadow: 6px 0 0 #1d1d1d, -6px 0 0 #1d1d1d, 0 6px 0 #1d1d1d, 0 -6px 0 #1d1d1d, 0 12px 0 #1d1d1d; }}
      #s0-xp {{ display: none; }}
      .done {{ position: absolute; left: 0; right: 0; top: 330px; display: flex; flex-direction: column; align-items: center; }}
      .done-big {{ display: block; font-family: "Lilita One"; font-size: 150px; line-height: 0.92; color: #ffd23f; text-align: center;
        text-shadow: 8px 0 0 #1d1d1d, -8px 0 0 #1d1d1d, 0 8px 0 #1d1d1d, 0 -8px 0 #1d1d1d, 6px 6px 0 #1d1d1d, -6px 6px 0 #1d1d1d, 6px -6px 0 #1d1d1d, -6px -6px 0 #1d1d1d, 0 18px 0 #1d1d1d; }}
      .lvlup {{ display: block; margin-top: 36px; font-family: "Lilita One"; font-size: 64px; color: #1d1d1d; background: #7dff6a; border: 6px solid #1d1d1d; border-radius: 18px; padding: 6px 30px; }}
      .toast {{ position: absolute; left: 90px; right: 90px; top: 1290px; height: 250px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: center; align-items: center;
        background: #2a1f4a; border: 8px solid #ffd23f; border-radius: 26px; }}
      .toast b {{ display: block; font-family: "Lilita One"; font-weight: 400; font-size: 46px; color: #ffd23f; }}
      .toast span {{ display: block; margin-top: 8px; font-family: "Lilita One"; font-size: 84px; color: #ffffff; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="30">
      <div id="bg" class="clip bg" data-start="0" data-duration="30" data-track-index="0">
        <div class="sky"></div>{clouds}
        <div class="ground"></div>
      </div>


      {"".join(scene(i, *SCENES[i]) for i in range(7))}

      <div id="avlayer" class="clip avwrap" data-start="0" data-duration="30" data-track-index="3">
        <svg viewBox="0 0 1080 990"><ellipse cx="215" cy="895" rx="120" ry="16" fill="#1d1d1d" opacity="0.25"/>{avatar()}</svg>
      </div>

      <div id="hud" class="clip hud" data-start="0" data-duration="30" data-track-index="5">
        <div class="quest" id="quest">
          <span class="qtitle">QUEST: PERFECT PASTA</span>
          <span class="lvl" id="lvl1">LVL 1</span>
          <span class="lvl" id="lvl2">LVL 2</span>
          <div class="qbar"><span class="qfill" id="qfill"></span></div>
          {counters}
        </div>
      </div>

      <div id="finale" class="clip hud" data-start="27.4" data-duration="2.6" data-track-index="6">
        <div class="done"><span class="done-big" id="done-big">QUEST<br>COMPLETE!</span><span class="lvlup" id="lvlup">LEVEL UP!</span></div>
        <div class="toast" id="toast"><b>ACHIEVEMENT UNLOCKED</b><span>Pasta Pro</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="30" data-track-index="10" data-volume="1"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const S = {S};
      const D = {D};
      const TC = {str(TC).replace("None", "null")};
      const C = "50% 50%";

      // ---- ambient: clouds drift, avatar idle bob ----
      tl.to("#cl0", {{ x: 120, duration: 30, ease: "none" }}, 0);
      tl.to("#cl1", {{ x: -140, duration: 30, ease: "none" }}, 0);
      tl.to("#cl2", {{ x: 90, duration: 30, ease: "none" }}, 0);
      tl.to("#av", {{ y: -10, duration: 0.45, repeat: 59, yoyo: true, ease: "sine.inOut" }}, 0);

      // ---- HUD ----
      tl.from("#quest", {{ y: -260, duration: 0.5, ease: "back.out(1.6)" }}, 0.05);
      tl.fromTo("#qfill", {{ scaleX: 0 }}, {{ scaleX: 0.001, duration: 0.01, transformOrigin: "0% 50%" }}, 0);
      for (let i = 1; i <= 6; i++) {{
        const t = S[i] + TC[i];
        tl.to("#qfill", {{ scaleX: i / 6, duration: 0.35, ease: "power2.out", transformOrigin: "0% 50%" }}, t);
        tl.to(`#q${{i-1}}`, {{ opacity: 0, duration: 0.05 }}, t);
        tl.fromTo(`#q${{i}}`, {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", transformOrigin: C }}, t);
        tl.fromTo(`#s${{i}}-xp`, {{ opacity: 0, y: 40, scale: 0.6 }}, {{ opacity: 1, y: -60, scale: 1, duration: 0.45, ease: "back.out(2)", transformOrigin: C }}, t + 0.05);
        tl.to(`#s${{i}}-xp`, {{ opacity: 0, y: -140, duration: 0.3, ease: "power2.in" }}, t + 0.75);
      }}
      tl.to("#lvl1", {{ opacity: 0, duration: 0.05 }}, 27.75);
      tl.fromTo("#lvl2", {{ opacity: 0, scale: 2 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)", transformOrigin: C }}, 27.75);

      // ---- per-scene in/out ----
      for (let i = 0; i <= 6; i++) {{
        tl.from(`#s${{i}}-art`, {{ scale: 0.8, opacity: 0, duration: 0.45, ease: "back.out(1.7)", transformOrigin: "65% 70%" }}, S[i] + 0.02);
        tl.from(`#s${{i}} .step`, {{ scale: 0, duration: 0.3, ease: "back.out(2.5)", transformOrigin: C }}, S[i] + 0.12);
        tl.from(`#s${{i}}-title`, {{ y: 80, scale: 0.6, opacity: 0, duration: 0.4, ease: "back.out(2)", transformOrigin: C }}, S[i] + 0.18);
        tl.from(`#s${{i}}-chat`, {{ x: -120, opacity: 0, duration: 0.35, ease: "power3.out" }}, S[i] + 0.3);
        if (i < 6) tl.to(`#s${{i}}-wrap`, {{ opacity: 0, x: -80, duration: 0.22, ease: "power2.in" }}, S[i] + D[i] - 0.22);
      }}

      // ---- avatar gestures ----
      tl.to("#av-rarm", {{ rotation: -150, duration: 0.25, ease: "power2.out", svgOrigin: "313 615" }}, 0.3);
      tl.to("#av-rarm", {{ rotation: -120, duration: 0.18, repeat: 5, yoyo: true, ease: "sine.inOut", svgOrigin: "313 615" }}, 0.55);
      tl.to("#av-rarm", {{ rotation: 0, duration: 0.25, ease: "power2.in", svgOrigin: "313 615" }}, 1.7);
      for (let i = 1; i <= 6; i++) {{  // point at the object each step
        tl.to("#av-rarm", {{ rotation: -75, duration: 0.25, ease: "back.out(2)", svgOrigin: "313 615" }}, S[i] + 0.35);
        tl.to("#av-rarm", {{ rotation: 0, duration: 0.25, ease: "power2.in", svgOrigin: "313 615" }}, S[i] + 1.5);
        tl.to("#av-head", {{ rotation: 6, duration: 0.2, repeat: 1, yoyo: true, svgOrigin: "210 595" }}, S[i] + 0.4);
      }}

      // ---- S0 hook ----
      tl.to("#s0-rays", {{ rotation: 45, duration: 3, ease: "none", svgOrigin: "700 560" }}, 0);
      tl.to("#s0-item", {{ y: -24, duration: 0.5, repeat: 5, yoyo: true, ease: "sine.inOut" }}, 0.3);

      // ---- S1 boil ----
      for (let k = 0; k < 5; k++) {{
        tl.to(`#s1-f${{k}}`, {{ scaleY: 1.35, duration: 0.16 + k * 0.02, repeat: 21, yoyo: true, ease: "steps(2)", transformOrigin: "50% 100%" }}, S[1] + 0.1);
        tl.fromTo(`#s1-b${{k}}`, {{ scale: 0 }}, {{ scale: 1.2, duration: 0.4, repeat: 7, yoyo: true, ease: "steps(3)", transformOrigin: C }}, S[1] + 0.3 + k * 0.12);
      }}
      for (let k = 0; k < 3; k++) {{
        tl.fromTo(`#s1-st${{k}}`, {{ y: 40, opacity: 0.9 }}, {{ y: -200, opacity: 0, duration: 1.2, repeat: 2, ease: "power1.out" }}, S[1] + 0.4 + k * 0.3);
      }}
      tl.to("#s1-pot", {{ y: -5, duration: 0.1, repeat: 29, yoyo: true, ease: "steps(1)" }}, S[1] + 0.5);

      // ---- S2 salt ----
      for (let k = 0; k < 5; k++) tl.to(`#s2-f${{k}}`, {{ scaleY: 1.3, duration: 0.18, repeat: 21, yoyo: true, ease: "steps(2)", transformOrigin: "50% 100%" }}, S[2]);
      tl.from("#s2-shaker", {{ y: -400, duration: 0.45, ease: "bounce.out" }}, S[2] + 0.1);
      tl.to("#s2-shaker", {{ rotation: 160, duration: 0.35, ease: "back.out(1.5)", svgOrigin: "688 210" }}, S[2] + 0.62);
      tl.to("#s2-shaker", {{ y: "+=26", duration: 0.12, repeat: 11, yoyo: true, ease: "sine.inOut" }}, S[2] + 1.0);
      for (let k = 0; k < 6; k++) tl.fromTo(`#s2-g${{k}}`, {{ y: -40, opacity: 0 }}, {{ y: 280, opacity: 1, duration: 0.55, repeat: 3, ease: "power2.in" }}, S[2] + 1.0 + k * 0.08);
      tl.fromTo("#s2-flavor", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(2.5)" }}, S[2] + 1.7);

      // ---- S3 add + stir ----
      for (let k = 0; k < 5; k++) tl.to(`#s3-f${{k}}`, {{ scaleY: 1.3, duration: 0.18, repeat: 21, yoyo: true, ease: "steps(2)", transformOrigin: "50% 100%" }}, S[3]);
      tl.from("#s3-sticks", {{ y: -560, duration: 0.5, ease: "power3.in" }}, S[3] + 0.35);
      tl.to("#s3-sticks", {{ y: 200, duration: 1.3, ease: "power2.out" }}, S[3] + 0.9);
      tl.from("#s3-spoon", {{ y: -500, duration: 0.4, ease: "bounce.out" }}, S[3] + 1.1);
      tl.fromTo("#s3-spoon", {{ rotation: -18 }}, {{ rotation: 18, duration: 0.3, repeat: 9, yoyo: true, ease: "sine.inOut", svgOrigin: "865 640" }}, S[3] + 1.5);

      // ---- S4 timer ----
      tl.from("#s4-box", {{ y: -600, duration: 0.5, ease: "bounce.out" }}, S[4] + 0.05);
      tl.to("#s4-t10", {{ opacity: 0, duration: 0.05, repeat: 5, yoyo: true }}, S[4] + 1.0);
      tl.to("#s4-t10", {{ opacity: 0, duration: 0.05 }}, S[4] + 1.6);
      tl.fromTo("#s4-t9", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", svgOrigin: "630 710" }}, S[4] + 1.6);
      tl.fromTo("#s4-badge", {{ scale: 0, rotation: -10 }}, {{ scale: 1, rotation: -3, duration: 0.4, ease: "back.out(2.5)", svgOrigin: "630 200" }}, S[4] + 2.2);

      // ---- S5 pasta water ----
      tl.from("#s5-mug", {{ y: -600, duration: 0.5, ease: "bounce.out" }}, S[5] + 0.05);
      tl.fromTo("#s5-fill", {{ y: 290 }}, {{ y: 0, duration: 1.3, ease: "steps(8)" }}, S[5] + 0.6);
      tl.fromTo("#s5-card", {{ opacity: 0, y: -120 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "back.out(2)" }}, S[5] + 1.9);
      tl.to("#s5-card", {{ y: -12, duration: 0.3, repeat: 3, yoyo: true, ease: "sine.inOut" }}, S[5] + 2.4);

      // ---- S6 toss + finale ----
      tl.from("#s6-pan", {{ y: -600, duration: 0.5, ease: "bounce.out" }}, S[6] + 0.05);
      tl.from("#s6-toss", {{ opacity: 0, duration: 0.2 }}, S[6] + 0.4);
      [0.8, 1.7].forEach((t0, n) => {{
        tl.to("#s6-toss", {{ y: -260, rotation: n ? -20 : 20, duration: 0.35, ease: "power2.out", svgOrigin: "690 600" }}, S[6] + t0);
        tl.to("#s6-toss", {{ y: 0, rotation: 0, duration: 0.35, ease: "power2.in", svgOrigin: "690 600" }}, S[6] + t0 + 0.35);
        tl.to("#s6-pan", {{ y: 14, duration: 0.08, repeat: 1, yoyo: true }}, S[6] + t0 + 0.7);
      }});
      const E = 27.4;
      tl.to(["#s6-copy", "#s6-chat"], {{ opacity: 0, duration: 0.2 }}, E);
      tl.from("#done-big", {{ scale: 0.2, opacity: 0, duration: 0.45, ease: "back.out(2.2)", transformOrigin: C }}, E + 0.1);
      tl.from("#lvlup", {{ scale: 0, duration: 0.35, ease: "back.out(2.5)", transformOrigin: C }}, E + 0.35);
      tl.from("#toast", {{ y: 400, opacity: 0, duration: 0.45, ease: "back.out(1.6)" }}, E + 0.55);
      const dirs = [[-320,-380],[-220,-460],[-90,-520],[60,-500],[200,-470],[320,-380],[-380,-200],[380,-220],[-260,-120],[260,-140],[-140,-300],[140,-320],[-30,-420],[30,-260]];
      dirs.forEach(([dx, dy], k) => {{
        tl.fromTo(`#s6-c${{k}}`, {{ x: 0, y: 0, rotation: 0, opacity: 0 }}, {{ x: dx, y: dy, rotation: 180 + k * 40, opacity: 1, duration: 0.6, ease: "power2.out", svgOrigin: "703 533" }}, E + 0.3);
        tl.to(`#s6-c${{k}}`, {{ y: dy + 260, opacity: 0, duration: 1.2, ease: "power1.in" }}, E + 0.9);
      }});
      tl.to("#av", {{ y: -140, duration: 0.3, ease: "power2.out" }}, E + 0.35);
      tl.to("#av", {{ y: 0, duration: 0.3, ease: "power2.in" }}, E + 0.65);
      tl.to("#av", {{ y: -90, duration: 0.25, ease: "power2.out" }}, E + 1.0);
      tl.to("#av", {{ y: 0, duration: 0.25, ease: "power2.in" }}, E + 1.25);
      tl.to(["#av-larm", "#av-rarm"], {{ rotation: (i) => (i ? -160 : 160), duration: 0.25, ease: "back.out(2)", svgOrigin: (i) => (i ? "313 615" : "107 615") }}, E + 0.35);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(sys.argv[1], "w").write(html)
print("wrote", sys.argv[1])
