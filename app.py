"""
Harappan Script — Glyph Frequency Chart
=========================================
Visual analysis of two Harappan sign sets:
  Image 1 — Tree/Plant/Cross signs (Signs 1–20)
  Image 2 — Anthropomorphic (Human-form) signs (Signs 1–20)

Run:  streamlit run harappan_frequency_chart.py
"""

import streamlit as st
import streamlit.components.v1 as components
import math
from collections import Counter, defaultdict

st.set_page_config(
    page_title="Harappan Glyph Frequency",
    page_icon="𒀭",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════════════════════
# ── PRIMITIVE DEFINITIONS (visually derived from both images) ─────────────────
# ══════════════════════════════════════════════════════════════════════════════

PRIM_DESC = {
    # Linear
    "V":    ("Vertical stroke",           "#e05050"),
    "H":    ("Horizontal stroke",         "#e09030"),
    "DL":   ("Diagonal left ╲",           "#d4c030"),
    "DR":   ("Diagonal right ╱",          "#a0c030"),
    # Branching
    "Ar":   ("Arrow / upward point ↑",    "#50c870"),
    "Fk":   ("Fork / Y-shape",            "#30c0b0"),
    "Tri":  ("Trident / 3-prong ψ",       "#3090e0"),
    "Br":   ("Branch / comb side-prongs", "#7060e0"),
    "Comb": ("Full comb (many prongs)",   "#c060d0"),
    "Tree": ("Tree / fir (stacked Br)",   "#e040a0"),
    # Crossing
    "X":    ("Cross ✕",                   "#e06080"),
    "XX":   ("Double cross ✕✕",           "#c08030"),
    # Curved / Closed
    "C":    ("Curve / arc",               "#50a870"),
    "O":    ("Circle / oval",             "#2090c0"),
    "Sq":   ("Square / rectangle",        "#6060e0"),
    # Human body parts
    "HdB":  ("Head — basic circle",       "#e05050"),
    "HdT":  ("Head — triangle",           "#e09030"),
    "HdO":  ("Head — oval/diamond",       "#d4c030"),
    "Torso":("Torso / body line",         "#a0c030"),
    "Arms": ("Arms — horizontal spread",  "#50c870"),
    "ArUp": ("Arms raised ↑ spread",      "#30c0b0"),
    "Legs": ("Legs — spread V",           "#3090e0"),
    "LegX": ("Legs — crossed X",          "#7060e0"),
    "Tail": ("Tail / extra appendage",    "#c060d0"),
    "Dot":  ("Dot / small marker",        "#e040a0"),
    "Sc":   ("Scarf / shoulder drape",    "#e06080"),
    "Flag": ("Flag / banner on arm",      "#c08030"),
    "Rake": ("Rake / multi-finger hand",  "#50a870"),
    "Bow":  ("Bow / arc above head",      "#2090c0"),
    "Bkt":  ("Bracket ) curve",           "#6060e0"),
}

# ══════════════════════════════════════════════════════════════════════════════
# ── IMAGE 1: TREE / PLANT / CROSS SIGNS  (visual study of image 1)
# ══════════════════════════════════════════════════════════════════════════════
#  Observations from careful study:
#  - All signs built on a VERTICAL stem (V)
#  - Signs 1–3: arrow/upward topped verticals, different branch counts
#  - Signs 4–6: star-cross tops (X on vertical), sign 5 adds roof hat
#  - Signs 7–8: Y-fork and trident tops
#  - Signs 9–10: circle-cap + trident; marks/dots added
#  - Signs 11–14: comb/rake bases; tree forms
#  - Signs 15–18: double-X forms (XX)
#  - Signs 19–20: simple arrow, spoon/lollipop

IMG1_SIGNS = [
    # num, label,  primitives,                  visual_notes
    (1,  "Sign 1",  ["V","Ar"],                  "Simple vertical + upward arrow tip"),
    (2,  "Sign 2",  ["V","Fk","Bkt","Bkt"],      "Central V with Y-fork top + two bracket curves flanking"),
    (3,  "Sign 3",  ["V","Ar","Br"],             "Vertical + arrow tip + one side branch pair"),
    (4,  "Sign 4",  ["V","X"],                   "Vertical stem + star-cross top (X on V)"),
    (5,  "Sign 5",  ["V","X","H"],               "Vertical + cross top + roof/hat horizontal bar"),
    (6,  "Sign 6",  ["V","X","DL"],              "Vertical + cross + extra diagonal slash"),
    (7,  "Sign 7",  ["V","Fk"],                  "Vertical + simple Y-fork top"),
    (8,  "Sign 8",  ["V","Tri"],                 "Vertical + trident/3-prong top"),
    (9,  "Sign 9",  ["V","Tri","O"],             "Vertical + trident + circular cap above"),
    (10, "Sign 10", ["V","Tri","Dot","Dot"],      "Vertical + trident + two small dots/marks"),
    (11, "Sign 11", ["V","Fk","Comb"],           "Vertical + Y-fork top + full comb base"),
    (12, "Sign 12", ["V","Fk","Comb","Legs"],    "Y-fork + comb base + leg-like lower prongs"),
    (13, "Sign 13", ["V","Br","Br","Br"],        "Vertical + 3 tiered branch pairs — tree form"),
    (14, "Sign 14", ["V","Tree"],                "Vertical + many stacked horizontal branches — fir tree"),
    (15, "Sign 15", ["XX","V"],                  "Double overlapping X + vertical connector"),
    (16, "Sign 16", ["XX"],                      "Clean large double-X, no extra strokes"),
    (17, "Sign 17", ["XX","Br","Ar"],            "Double-X + extra branch + arrow marker"),
    (18, "Sign 18", ["XX","V","Ar"],             "Double-X + vertical pin + upward arrow"),
    (19, "Sign 19", ["V","Ar"],                  "Simple vertical + upward arrow (plain arrow)"),
    (20, "Sign 20", ["V","O"],                   "Vertical stem + circle/lollipop head"),
]

# ══════════════════════════════════════════════════════════════════════════════
# ── IMAGE 2: ANTHROPOMORPHIC (HUMAN-FORM) SIGNS  (visual study of image 2)
# ══════════════════════════════════════════════════════════════════════════════
#  All signs share a human body grammar:
#  HdB/HdT/HdO = head shape | Torso = body | Arms/ArUp = arm spread
#  Legs/LegX = leg form | extras = Tail, Rake, Bow, Sc, Flag, Dot, O, X
IMG2_SIGNS = [
    (1,  "Anth 1",  ["HdB","Torso","Arms","Legs"],            "Basic human figure — round head, spread arms, V-legs"),
    (2,  "Anth 2",  ["HdT","Torso","Arms","Legs"],            "Triangle-head figure with spread arms + V-legs"),
    (3,  "Anth 3",  ["HdT","Torso","Arms","Legs","Bkt"],      "Triangle-head + bracket curve at side"),
    (4,  "Anth 4",  ["HdB","Torso","Arms","Legs","Sq"],       "Figure with square/box torso addition"),
    (5,  "Anth 5",  ["HdT","Torso","Arms","Legs","HdT"],      "Figure with two triangle elements (head + top ornament)"),
    (6,  "Anth 6",  ["HdB","Torso","ArUp","Legs","O","O"],    "Figure with raised arms + two oval loops"),
    (7,  "Anth 7",  ["HdB","Torso","ArUp","Legs","O","O"],    "Similar to 6, oval loops at sides"),
    (8,  "Anth 8",  ["HdB","Torso","ArUp","Legs","O","O","H"],"Loops + horizontal bar across top"),
    (10, "Anth 10", ["HdB","Torso","Arms","Legs","Tree"],     "Figure with fir-tree / decorated torso centre"),
    (11, "Anth 11", ["HdB","Torso","Arms","Legs","O","X"],    "Figure with circle + cross on body"),
    (12, "Anth 12", ["HdB","Torso","Arms","Legs","Ar"],       "Figure with one raised arm / arrow"),
    (13, "Anth 13", ["HdB","Torso","Arms","Legs","Rake"],     "Figure with rake/multi-prong hand"),
    (14, "Anth 14", ["HdB","Torso","Arms","LegX","Rake","X"], "Rake hand + crossed legs + X feet"),
    (15, "Anth 15", ["HdB","Torso","Arms","Legs"],            "Simpler clean human figure"),
    (16, "Anth 16", ["V","V","Torso","Legs"],                 "Two parallel vertical bodies — twin figure"),
    (17, "Anth 17", ["HdB","Torso","Arms","Legs","X","Dot"],  "Figure with X-marker + dot at feet"),
    (18, "Anth 18", ["HdB","Torso","ArUp","Legs","Bow"],      "Figure with raised arms + bow arch above head"),
    (20, "Anth 20", ["HdB","Torso","Arms","Legs","Flag"],     "Figure with flag/banner on arm"),
]

# ══════════════════════════════════════════════════════════════════════════════
# ── COLOUR MAPPING
# ══════════════════════════════════════════════════════════════════════════════
def pcolor(p):
    return PRIM_DESC.get(p, ("?","#888888"))[1]

def pname(p):
    return PRIM_DESC.get(p, (p,"#888888"))[0]

# ══════════════════════════════════════════════════════════════════════════════
# ── SVG PRIMITIVE RENDERER
# ══════════════════════════════════════════════════════════════════════════════
def _s(p, sx, sy, r, sc, sw=2.6):
    """Draw a single primitive centred at (sx,sy) with radius r."""
    a = r * 0.88
    def L(x1,y1,x2,y2):
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>'
    def PL(pts, close=False):
        s=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        tag = "polygon" if close else "polyline"
        return f'<{tag} points="{s}" fill="none" stroke="{sc}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'

    if p=="V":    return L(sx,sy-a*1.15,sx,sy+a*1.15)
    if p=="H":    return L(sx-a*1.2,sy,sx+a*1.2,sy)
    if p=="DL":   return L(sx-a,sy-a,sx+a,sy+a)
    if p=="DR":   return L(sx+a,sy-a,sx-a,sy+a)
    if p=="X":    return L(sx-a,sy-a,sx+a,sy+a)+L(sx+a,sy-a,sx-a,sy+a)
    if p=="XX":
        return (L(sx-a*.6,sy-a,sx+a*.6,sy+a)+L(sx+a*.6,sy-a,sx-a*.6,sy+a)+
                L(sx-a*1.1,sy-a*.8,sx+a*1.1,sy+a*.8)+L(sx+a*1.1,sy-a*.8,sx-a*1.1,sy+a*.8))
    if p=="Ar":
        return L(sx,sy+a*.5,sx,sy-a*.8)+PL([(sx-a*.5,sy-a*.3),(sx,sy-a*.8),(sx+a*.5,sy-a*.3)])
    if p=="Fk":   return L(sx,sy+a*.5,sx,sy-a*.2)+L(sx,sy-a*.2,sx-a*.7,sy-a*.9)+L(sx,sy-a*.2,sx+a*.7,sy-a*.9)
    if p=="Tri":
        return (L(sx,sy+a*.5,sx,sy-a*.1)+
                L(sx,sy-a*.1,sx-a*.65,sy-a*.9)+L(sx,sy-a*.1,sx,sy-a*.9)+L(sx,sy-a*.1,sx+a*.65,sy-a*.9))
    if p=="Br":
        return L(sx,sy-a*.3,sx,sy+a*.3)+L(sx-a*.8,sy-a*.6,sx+a*.8,sy-a*.6)+L(sx-a*.8,sy,sx+a*.8,sy)
    if p=="Comb":
        base_y=sy+a*.3
        out=L(sx-a,base_y,sx+a,base_y)
        for dx in [-a*.7,-a*.35,0,a*.35,a*.7]:
            out+=L(sx+dx,base_y,sx+dx,sy-a*.6)
        return out
    if p=="Tree":
        out=L(sx,sy+a,sx,sy-a)
        for i,width in enumerate([a*.9,a*.65,a*.4,a*.2]):
            yy=sy+a*.4-i*a*.6
            out+=L(sx-width,yy,sx+width,yy)
        return out
    if p=="C":    return f'<path d="M{sx+r*.35:.1f},{sy-r:.1f} A{r:.1f},{r:.1f} 0 0,0 {sx+r*.35:.1f},{sy+r:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>'
    if p=="O":    return f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{r*.78:.1f}" ry="{r:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}"/>'
    if p=="Sq":   s2=r*.8; return f'<rect x="{sx-s2:.1f}" y="{sy-s2:.1f}" width="{2*s2:.1f}" height="{2*s2:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}"/>'
    if p=="Bkt":  return f'<path d="M{sx-r*.2:.1f},{sy-r:.1f} A{r:.1f},{r:.1f} 0 0,1 {sx-r*.2:.1f},{sy+r:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>'
    if p=="Dot":  return f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sw+0.5:.1f}" fill="{sc}"/>'
    # Human body primitives
    if p=="HdB":  return f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r*.55:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}"/>'
    if p=="HdT":  return PL([(sx-r*.55,sy+r*.45),(sx,sy-r*.6),(sx+r*.55,sy+r*.45)])
    if p=="HdO":  return f'<ellipse cx="{sx:.1f}" cy="{sy:.1f}" rx="{r*.45:.1f}" ry="{r*.55:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}"/>'
    if p=="Torso": return L(sx,sy-a*.8,sx,sy+a*.8)
    if p=="Arms":  return L(sx-a*1.1,sy-a*.1,sx+a*1.1,sy-a*.1)
    if p=="ArUp":  return L(sx-a*1.1,sy+a*.3,sx,sy-a*.5)+L(sx,sy-a*.5,sx+a*1.1,sy+a*.3)
    if p=="Legs":  return L(sx,sy,sx-a*.65,sy+a*1.0)+L(sx,sy,sx+a*.65,sy+a*1.0)
    if p=="LegX":  return L(sx-a*.6,sy,sx+a*.6,sy+a)+L(sx+a*.6,sy,sx-a*.6,sy+a)
    if p=="Tail":  return L(sx+a*.3,sy,sx+a,sy+a*.6)
    if p=="Sc":    return f'<path d="M{sx-a:.1f},{sy-a*.4:.1f} Q{sx:.1f},{sy-a*1.2:.1f} {sx+a:.1f},{sy-a*.4:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>'
    if p=="Flag":  return L(sx+a*.2,sy-a*.6,sx+a*.2,sy+a*.4)+L(sx+a*.2,sy-a*.6,sx+a*1.0,sy-a*.2)+L(sx+a*1.0,sy-a*.2,sx+a*.2,sy)
    if p=="Rake":
        out=L(sx+a*.1,sy,sx+a,sy)
        for dy in [-a*.5,-a*.15,a*.2,a*.55]:
            out+=L(sx+a,sy+dy,sx+a,sy+dy+a*.1)
        return out
    if p=="Bow":  return f'<path d="M{sx-a:.1f},{sy:.1f} A{a:.1f},{a:.1f} 0 0,1 {sx+a:.1f},{sy:.1f}" fill="none" stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>'
    return ""

def mini_prim_svg(p, w=36, h=32, bg="#0d0b08", sc=None):
    col = sc if sc is not None else pcolor(p)
    cx,cy=w/2,h/2; r=min(w,h)*.28
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{bg}" rx="3"/>{_s(p,cx,cy,r,col)}</svg>')

def sign_svg(prims, w=68, h=72, bg="#0d0b08", sc="#f5c842"):
    """Render a full sign from its primitives using layout logic."""
    cx,cy=w/2,h/2; r=min(w,h)*.13; paths=[]
    from collections import Counter as C2
    cc=C2(prims)

    # ── Image 1 sign layouts (plant/tree/cross) ──
    if "XX" in cc:
        paths.append(_s("XX",cx,cy,r*1.3,sc))
        for p in prims:
            if p not in ("XX",):
                paths.append(_s(p,cx,cy+r*2.2,r*.8,sc))
    elif "Tree" in cc:
        paths.append(_s("Tree",cx,cy,r*1.4,sc))
    elif "V" in cc or "Torso" in cc:
        # vertical-based plant signs
        stem_y = cy
        # draw vertical stem first
        paths.append(f'<line x1="{cx:.1f}" y1="{h*.08:.1f}" x2="{cx:.1f}" y2="{h*.92:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
        top_prims = [p for p in prims if p not in ("V","Torso","Legs","LegX","Comb")]
        bot_prims = [p for p in prims if p in ("Comb","Legs","LegX")]
        # top ornament at top of stem
        if "X" in top_prims:   paths.append(_s("X",cx,h*.22,r*1.3,sc))
        if "XX" in top_prims:  paths.append(_s("XX",cx,h*.22,r*1.4,sc))
        if "Ar" in top_prims:  paths.append(_s("Ar",cx,h*.18,r*1.1,sc))
        if "Fk" in top_prims:  paths.append(_s("Fk",cx,h*.22,r*1.2,sc))
        if "Tri" in top_prims: paths.append(_s("Tri",cx,h*.22,r*1.2,sc))
        if "Br" in top_prims:
            for i,yy in enumerate([h*.28,h*.4,h*.52]):
                paths.append(_s("Br",cx,yy,r*1.1,sc))
        if "H" in top_prims:   paths.append(_s("H",cx,h*.12,r*1.2,sc))
        if "DL" in top_prims:  paths.append(_s("DL",cx+r*.6,h*.26,r*.8,sc))
        if "O" in top_prims:   paths.append(_s("O",cx,h*.14,r*1.0,sc))
        if "Bkt" in top_prims:
            paths.append(_s("Bkt",cx-r*1.8,cy,r*1.1,sc))
            paths.append(f'<path d="M{cx+r*1.0:.1f},{h*.12:.1f} A{r*1.1:.1f},{r*1.1:.1f} 0 0,0 {cx+r*1.0:.1f},{h*.92:.1f}" fill="none" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
        dot_count = cc.get("Dot",0)
        for di in range(dot_count):
            dx = cx + (di-dot_count/2+0.5)*r*1.2
            paths.append(_s("Dot",dx,h*.35,r*.5,sc))
        if "Comb" in bot_prims:
            # comb at bottom
            by=h*.82
            paths.append(f'<line x1="{cx-r*1.6:.1f}" y1="{by:.1f}" x2="{cx+r*1.6:.1f}" y2="{by:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
            for ddx in [-r*1.2,-r*.6,0,r*.6,r*1.2]:
                paths.append(f'<line x1="{cx+ddx:.1f}" y1="{by:.1f}" x2="{cx+ddx:.1f}" y2="{by+r*1.0:.1f}" stroke="{sc}" stroke-width="2.5" stroke-linecap="round"/>')
        if "O" in bot_prims and "O" not in top_prims:
            paths.append(_s("O",cx,h*.82,r*.9,sc))

    # ── Image 2 sign layouts (human figures) ──
    elif any(p in cc for p in ["HdB","HdT","HdO"]):
        head_y  = h*.14
        neck_y  = h*.23
        chest_y = h*.38
        hip_y   = h*.56
        foot_y  = h*.88

        # Head
        if "HdB" in cc:  paths.append(_s("HdB",cx,head_y,r*1.15,sc))
        elif "HdT" in cc:paths.append(_s("HdT",cx,head_y,r*1.15,sc))
        else:             paths.append(_s("HdO",cx,head_y,r*1.15,sc))

        # Torso line
        paths.append(f'<line x1="{cx:.1f}" y1="{neck_y:.1f}" x2="{cx:.1f}" y2="{hip_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')

        # Arms
        arm_y = chest_y
        if "ArUp" in cc:
            paths.append(f'<line x1="{cx:.1f}" y1="{arm_y:.1f}" x2="{cx-w*.34:.1f}" y2="{h*.28:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
            paths.append(f'<line x1="{cx:.1f}" y1="{arm_y:.1f}" x2="{cx+w*.34:.1f}" y2="{h*.28:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
        elif "Arms" in cc:
            paths.append(f'<line x1="{cx-w*.38:.1f}" y1="{arm_y:.1f}" x2="{cx+w*.38:.1f}" y2="{arm_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')

        # Legs
        if "LegX" in cc:
            paths.append(f'<line x1="{cx:.1f}" y1="{hip_y:.1f}" x2="{cx-w*.26:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
            paths.append(f'<line x1="{cx:.1f}" y1="{hip_y:.1f}" x2="{cx+w*.26:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
            paths.append(f'<line x1="{cx-w*.26:.1f}" y1="{foot_y:.1f}" x2="{cx+w*.26:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.5" stroke-linecap="round"/>')
        elif "Legs" in cc:
            paths.append(f'<line x1="{cx:.1f}" y1="{hip_y:.1f}" x2="{cx-w*.26:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
            paths.append(f'<line x1="{cx:.1f}" y1="{hip_y:.1f}" x2="{cx+w*.26:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
        elif "V" in cc and "V" in cc:
            paths.append(f'<line x1="{cx-r:.1f}" y1="{neck_y:.1f}" x2="{cx-r:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')
            paths.append(f'<line x1="{cx+r:.1f}" y1="{neck_y:.1f}" x2="{cx+r:.1f}" y2="{foot_y:.1f}" stroke="{sc}" stroke-width="2.8" stroke-linecap="round"/>')

        # Body extras
        if "O" in cc:
            cnt_o = cc["O"]
            for oi in range(min(cnt_o,2)):
                ox = cx + (oi*2-1)*r*2.2 if cnt_o>1 else cx
                oy = hip_y - r*0.6
                paths.append(_s("O",ox,oy,r*1.2,sc,sw=2.2))
        if "X" in cc:   paths.append(_s("X",cx,hip_y+r,r*.7,sc,sw=2.0))
        if "Sq" in cc:  paths.append(_s("Sq",cx,chest_y,r*1.0,sc,sw=2.0))
        if "Dot" in cc: paths.append(_s("Dot",cx,hip_y+r*.8,r*.5,sc))
        if "Rake" in cc:paths.append(_s("Rake",cx+r*2.0,arm_y-r*.3,r*1.0,sc,sw=2.0))
        if "Tree" in cc:paths.append(_s("Tree",cx,chest_y,r*1.1,sc,sw=2.0))
        if "Bow" in cc: paths.append(_s("Bow",cx,head_y-r*1.5,r*1.4,sc,sw=2.2))
        if "Flag" in cc:paths.append(_s("Flag",cx+r*1.6,arm_y-r*.6,r*1.0,sc,sw=2.0))
        if "Bkt" in cc: paths.append(f'<path d="M{cx+w*.38:.1f},{neck_y:.1f} A{r*2:.1f},{r*2:.1f} 0 0,1 {cx+w*.38:.1f},{hip_y:.1f}" fill="none" stroke="{sc}" stroke-width="2.5" stroke-linecap="round"/>')
        if "H" in cc:   paths.append(f'<line x1="{cx-w*.42:.1f}" y1="{h*.05:.1f}" x2="{cx+w*.42:.1f}" y2="{h*.05:.1f}" stroke="{sc}" stroke-width="2.5" stroke-linecap="round"/>')
        if "HdT" in cc and cc["HdT"]>1:
            paths.append(_s("HdT",cx,head_y-r*1.8,r*.9,sc,sw=2.0))
        if "Ar" in cc:  paths.append(_s("Ar",cx+r*2.0,arm_y,r*.9,sc,sw=2.0))
        if "Sc" in cc:  paths.append(_s("Sc",cx,neck_y+r*.3,r*1.3,sc,sw=2.0))
    else:
        # fallback generic
        for i,p in enumerate(prims[:4]):
            paths.append(_s(p,cx+(i-len(prims)/2)*r*1.4,cy,r,sc))

    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{bg}" rx="4"/>{"".join(paths)}</svg>')

# ══════════════════════════════════════════════════════════════════════════════
# ── DERIVED STATS
# ══════════════════════════════════════════════════════════════════════════════
def derive_stats(signs):
    freq    = Counter(p for _,_,prims,_ in signs for p in prims)
    g2s     = defaultdict(list)
    s2g     = {}
    for num,lbl,prims,note in signs:
        s2g[lbl] = Counter(prims)
        for p in set(prims):
            g2s[p].append(lbl)
    return freq, g2s, s2g

freq1, g2s1, s2g1 = derive_stats(IMG1_SIGNS)
freq2, g2s2, s2g2 = derive_stats(IMG2_SIGNS)

ALL_PRIMS1 = [p for p in PRIM_DESC if freq1.get(p,0)>0]
ALL_PRIMS2 = [p for p in PRIM_DESC if freq2.get(p,0)>0]

# ══════════════════════════════════════════════════════════════════════════════
# ── CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=JetBrains+Mono:wght@300;400;600&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#050403;font-family:'Cinzel',serif;color:#e8d8b8;padding:10px;}
.ttl{font-size:.95rem;font-weight:700;color:#f0c050;margin-bottom:8px;border-bottom:1px solid #2e2810;padding-bottom:3px;letter-spacing:.05em;}
.sub{font-size:10px;color:#6a5828;font-family:'JetBrains Mono',monospace;margin-bottom:6px;}
.legend{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px;}
.li{display:flex;align-items:center;gap:3px;font-size:10px;color:#8a7040;font-family:'JetBrains Mono',monospace;}
.lsq{width:10px;height:10px;border-radius:2px;flex-shrink:0;}
</style>"""

# ── Heatmap ──
def build_heatmap(signs, all_prims, freq, s2g, title):
    cell_w, cell_h = 46, 52
    lbl_w,  head_h = 72, 58
    W = lbl_w + len(all_prims)*cell_w + 4
    H = head_h + len(signs)*cell_h + 4
    rows=[]

    # Column headers
    for gi,g in enumerate(all_prims):
        col = pcolor(g)
        cx  = lbl_w + gi*cell_w + cell_w//2
        psvg= mini_prim_svg(g,w=30,h=26,bg="#111008")
        pin = psvg.split(">",1)[1].rsplit("</svg>",1)[0]
        rows.append(f'<g transform="translate({lbl_w+gi*cell_w},2)">'
                    f'<rect width="{cell_w}" height="{head_h-2}" fill="#111008" rx="2" stroke="#2e2810" stroke-width=".6"/>'
                    f'<g transform="translate({(cell_w-30)//2},3)">{pin}</g>'
                    f'<text x="{cell_w//2}" y="{head_h-9}" text-anchor="middle" font-size="7.5" fill="{col}" font-family="monospace" font-weight="bold">{g}</text>'
                    f'</g>')

    # Rows
    for li,(num,lbl,prims,note) in enumerate(signs):
        y   = head_h + li*cell_h
        gc  = s2g[lbl]
        svgs= sign_svg(prims,w=60,h=cell_h-4,bg="#141008")
        inn = svgs.split(">",1)[1].rsplit("</svg>",1)[0]
        rows.append(f'<g transform="translate(0,{y})">'
                    f'<rect width="{lbl_w}" height="{cell_h}" fill="#141008" rx="0" stroke="#2e2810" stroke-width=".4"/>'
                    f'<text x="3" y="14" font-size="10" fill="#f0c050" font-family="monospace" font-weight="bold">{num}</text>'
                    f'<g transform="translate(1,2)">{inn}</g>'
                    f'</g>')
        for gi,g in enumerate(all_prims):
            x   = lbl_w + gi*cell_w
            cnt = gc.get(g,0)
            col = pcolor(g)
            if cnt>0:
                alpha= min(0.3+cnt*0.35,1.0)
                rows.append(f'<g transform="translate({x},{y})">'
                             f'<rect width="{cell_w}" height="{cell_h}" fill="{col}" opacity="{alpha:.2f}" rx="0" stroke="#2e2810" stroke-width=".4"/>'
                             f'<text x="{cell_w//2}" y="{cell_h//2+5}" text-anchor="middle" font-size="{"14" if cnt==1 else "12"}" fill="#fff" font-family="monospace" font-weight="bold">{"✓" if cnt==1 else cnt}</text>'
                             f'</g>')
            else:
                rows.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="#090807" stroke="#1e1a10" stroke-width=".3"/>')

    # grid lines
    for li in range(len(signs)+1):
        yy=head_h+li*cell_h
        rows.append(f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="#2e2810" stroke-width=".5"/>')
    for gi in range(len(all_prims)+1):
        xx=lbl_w+gi*cell_w
        rows.append(f'<line x1="{xx}" y1="0" x2="{xx}" y2="{H}" stroke="#2e2810" stroke-width=".5"/>')

    svg=(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
         f'<rect width="{W}" height="{H}" fill="#050403"/>{"".join(rows)}</svg>')

    legend="".join(f'<div class="li"><div class="lsq" style="background:{pcolor(g)};"></div><span style="color:{pcolor(g)};">{g}</span> {pname(g)}</div>' for g in all_prims)

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{BASE_CSS}</head><body>
<div class="ttl">{title} — Sign × Glyph Heatmap</div>
<div class="sub">Each cell: ✓ = primitive present, number = times repeated</div>
{svg}
<div class="legend">{legend}</div>
</body></html>""", H+80


# ── Frequency bar chart ──
def build_freq_bar(signs, all_prims, freq, g2s, title):
    sorted_p = sorted(all_prims, key=lambda g:-freq.get(g,0))
    max_f    = max(freq.values()) if freq else 1
    bar_max  = 380; row_h=44; lbl_w=78
    W=lbl_w+bar_max+160; H=len(sorted_p)*row_h+50
    rows=[]
    rows.append(f'<text x="2" y="22" font-size="12" font-weight="700" fill="#f0c050" font-family="serif">Glyph Frequency — {title}</text>')
    for i,g in enumerate(sorted_p):
        cnt=freq.get(g,0)
        col=pcolor(g)
        bw=max(3,round(cnt/max_f*bar_max))
        y=32+i*row_h
        psvg=mini_prim_svg(g,w=30,h=26,sc=col,bg="#050403")
        pin=psvg.split(">",1)[1].rsplit("</svg>",1)[0]
        rows.append(f'<g transform="translate(2,{y+6})">{pin}</g>')
        rows.append(f'<text x="35" y="{y+17}" font-size="10" fill="{col}" font-family="monospace" font-weight="bold">{g}</text>')
        rows.append(f'<text x="35" y="{y+28}" font-size="8" fill="#5a4820" font-family="monospace">{pname(g)[:20]}</text>')
        rows.append(f'<rect x="{lbl_w}" y="{y+4}" width="{bar_max}" height="{row_h-10}" fill="#111008" rx="3"/>')
        rows.append(f'<rect x="{lbl_w}" y="{y+4}" width="{bw}" height="{row_h-10}" fill="{col}" opacity=".82" rx="3"/>')
        rows.append(f'<text x="{lbl_w+bw+6}" y="{y+19}" font-size="13" fill="{col}" font-family="monospace" font-weight="bold">{cnt}</text>')
        signs_str=", ".join(g2s.get(g,[]))[:50]
        rows.append(f'<text x="{lbl_w+bw+28}" y="{y+19}" font-size="8" fill="#5a4820" font-family="monospace">{signs_str}</text>')

    svg=(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
         f'<rect width="{W}" height="{H}" fill="#050403"/>{"".join(rows)}</svg>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{BASE_CSS}</head><body>
<div class="ttl">Glyph Primitive Frequency — {title}</div>{svg}
</body></html>""", H+30


# ── Per-sign breakdown ──
def build_breakdown(signs, title, sort_by="order"):
    if sort_by=="complexity": signs=sorted(signs,key=lambda x:-len(x[2]))
    cell_h=60; W=1000; H=len(signs)*cell_h+44
    rows=[]
    rows.append(f'<text x="2" y="22" font-size="12" font-weight="700" fill="#f0c050" font-family="serif">Per-Sign Glyph Breakdown — {title}</text>')
    for i,(num,lbl,prims,note) in enumerate(signs):
        y   = 32+i*cell_h
        svgs= sign_svg(prims,w=54,h=cell_h-4,bg="#141008")
        inn = svgs.split(">",1)[1].rsplit("</svg>",1)[0]
        rows.append(f'<rect x="0" y="{y}" width="{W}" height="{cell_h}" fill="#{"1a1200" if i%2==0 else "121008"}" rx="2" stroke="#2e2810" stroke-width=".5"/>')
        rows.append(f'<g transform="translate(2,{y+2})">{inn}</g>')
        rows.append(f'<text x="58" y="{y+18}" font-size="12" fill="#f0c050" font-family="monospace" font-weight="700">{num}</text>')
        rows.append(f'<text x="58" y="{y+30}" font-size="8" fill="#6a5828" font-family="monospace">{note[:48]}</text>')
        px=100
        for p,cnt in Counter(prims).items():
            col=pcolor(p); pill_w=46+(10 if cnt>1 else 0)
            psvg=mini_prim_svg(p,w=26,h=22,sc=col,bg="#1a1208")
            pin=psvg.split(">",1)[1].rsplit("</svg>",1)[0]
            rows.append(f'<rect x="{px}" y="{y+8}" width="{pill_w}" height="26" fill="#1a1208" rx="4" stroke="{col}" stroke-width="1"/>')
            rows.append(f'<g transform="translate({px+2},{y+10})">{pin}</g>')
            rows.append(f'<text x="{px+30}" y="{y+24}" font-size="9.5" fill="{col}" font-family="monospace" font-weight="bold">{p}</text>')
            if cnt>1: rows.append(f'<text x="{px+pill_w-10}" y="{y+14}" font-size="8" fill="#f0c050" font-family="monospace">×{cnt}</text>')
            px+=pill_w+5
        rows.append(f'<text x="{px+4}" y="{y+24}" font-size="9" fill="#3a2e10" font-family="monospace">={len(prims)} strokes</text>')

    svg=(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
         f'<rect width="{W}" height="{H}" fill="#050403"/>{"".join(rows)}</svg>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{BASE_CSS}</head><body>
<div class="ttl">Per-Sign Breakdown — {title}</div>{svg}
</body></html>""", H+30


# ── Co-occurrence matrix ──
def build_comat(signs, all_prims, title):
    comat=defaultdict(int)
    for _,_,prims,_ in signs:
        gs=list(set(prims))
        for i in range(len(gs)):
            for j in range(i+1,len(gs)):
                k=tuple(sorted([gs[i],gs[j]])); comat[k]+=1
        for g in gs: comat[(g,g)]+=freq1.get(g,0) if "Anth" not in title else freq2.get(g,0)
    n=len(all_prims); cell=34
    W=n*cell+76; H=n*cell+76
    rows=[]
    max_co=max((v for k,v in comat.items() if k[0]!=k[1]),default=1)
    for i,g in enumerate(all_prims):
        col=pcolor(g)
        psvg=mini_prim_svg(g,w=26,h=22,sc=col,bg="#111008")
        pin=psvg.split(">",1)[1].rsplit("</svg>",1)[0]
        cx2=72+i*cell+cell//2
        rows.append(f'<g transform="translate({cx2-13},2)">{pin}</g>')
        rows.append(f'<text x="{cx2}" y="38" text-anchor="middle" font-size="7" fill="{col}" font-family="monospace" font-weight="bold">{g}</text>')
        y2=68+i*cell+cell//2
        rows.append(f'<g transform="translate(2,{y2-11})">{pin}</g>')
        rows.append(f'<text x="40" y="{y2+4}" text-anchor="end" font-size="7" fill="{col}" font-family="monospace" font-weight="bold">{g}</text>')

    for i,ga in enumerate(all_prims):
        for j,gb in enumerate(all_prims):
            x=72+j*cell; y=68+i*cell
            k=tuple(sorted([ga,gb])); cnt=comat.get(k,0)
            if i==j:
                col=pcolor(ga)
                rows.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{col}" opacity=".5" rx="2" stroke="#2e2810" stroke-width=".4"/>')
                rows.append(f'<text x="{x+cell//2}" y="{y+cell//2+4}" text-anchor="middle" font-size="8" fill="#fff" font-family="monospace">{cnt}</text>')
            elif cnt>0:
                alpha=0.15+cnt/max_co*.7; col=pcolor(ga)
                rows.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{col}" opacity="{alpha:.2f}" rx="2" stroke="#2e2810" stroke-width=".4"/>')
                rows.append(f'<text x="{x+cell//2}" y="{y+cell//2+4}" text-anchor="middle" font-size="8" fill="#fff" font-family="monospace">{cnt}</text>')
            else:
                rows.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="#090807" rx="2" stroke="#1e1a10" stroke-width=".3"/>')
    rows.insert(0,f'<text x="2" y="16" font-size="12" font-weight="700" fill="#f0c050" font-family="serif">Co-occurrence Matrix — {title}</text>')
    svg=(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
         f'<rect width="{W}" height="{H}" fill="#050403"/>{"".join(rows)}</svg>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{BASE_CSS}</head><body>
<div class="ttl">Co-occurrence Matrix — {title}</div>
<div class="sub">Diagonal = individual frequency. Off-diagonal = signs where both glyphs co-occur.</div>
{svg}
</body></html>""", H+40


# ── Distribution donut ──
def build_donut(freq, all_prims, title):
    W,H=780,360; cx,cy,R,Ri=170,185,145,72
    rows=[]
    total=sum(freq.get(g,0) for g in all_prims)
    angle=-math.pi/2
    sorted_p=sorted(all_prims,key=lambda g:-freq.get(g,0))
    for g in sorted_p:
        cnt=freq.get(g,0)
        if cnt==0: continue
        theta=2*math.pi*cnt/total
        x1s=cx+R*math.cos(angle);y1s=cy+R*math.sin(angle)
        x1e=cx+Ri*math.cos(angle);y1e=cy+Ri*math.sin(angle)
        a2=angle+theta
        x2s=cx+R*math.cos(a2);y2s=cy+R*math.sin(a2)
        x2e=cx+Ri*math.cos(a2);y2e=cy+Ri*math.sin(a2)
        la=1 if theta>math.pi else 0
        col=pcolor(g)
        rows.append(f'<path d="M{x1e:.1f},{y1e:.1f} L{x1s:.1f},{y1s:.1f} A{R},{R} 0 {la},1 {x2s:.1f},{y2s:.1f} L{x2e:.1f},{y2e:.1f} A{Ri},{Ri} 0 {la},0 {x1e:.1f},{y1e:.1f} Z" fill="{col}" opacity=".85" stroke="#050403" stroke-width="1.2"/>')
        if theta>0.16:
            ma=angle+theta/2; lx=cx+(R+18)*math.cos(ma); ly=cy+(R+18)*math.sin(ma)
            rows.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="8.5" fill="{col}" font-family="monospace" font-weight="bold">{g}</text>')
        angle=a2

    rows.append(f'<text x="{cx}" y="{cy-8}" text-anchor="middle" font-size="20" font-weight="700" fill="#f0c050" font-family="monospace">{total}</text>')
    rows.append(f'<text x="{cx}" y="{cy+10}" text-anchor="middle" font-size="10" fill="#6a5828" font-family="serif">tokens</text>')
    rows.append(f'<text x="{cx}" y="{cy+24}" text-anchor="middle" font-size="10" fill="#6a5828" font-family="serif">{len([g for g in all_prims if freq.get(g,0)>0])} types</text>')

    bx=350
    rows.append(f'<text x="{bx}" y="22" font-size="11" font-weight="700" fill="#f0c050" font-family="serif">Ranking</text>')
    for i,g in enumerate(sorted_p):
        cnt=freq.get(g,0)
        if cnt==0: continue
        col=pcolor(g); bw=max(2,round(cnt/max(freq.values())*340))
        y2=32+i*17; psvg=mini_prim_svg(g,w=12,h=12,sc=col,bg="#050403")
        pin=psvg.split(">",1)[1].rsplit("</svg>",1)[0]
        rows.append(f'<g transform="translate({bx-14},{y2-1})">{pin}</g>')
        rows.append(f'<text x="{bx}" y="{y2+9}" font-size="8.5" fill="{col}" font-family="monospace" font-weight="bold">{g}</text>')
        rows.append(f'<rect x="{bx+26}" y="{y2}" width="{bw}" height="11" fill="{col}" opacity=".8" rx="2"/>')
        rows.append(f'<text x="{bx+bw+30}" y="{y2+9}" font-size="8.5" fill="{col}" font-family="monospace">{cnt}</text>')

    rows.insert(0,f'<text x="2" y="17" font-size="12" font-weight="700" fill="#f0c050" font-family="serif">Distribution — {title}</text>')
    svg=(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
         f'<rect width="{W}" height="{H}" fill="#050403"/>{"".join(rows)}</svg>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{BASE_CSS}</head><body>
<div class="ttl">Glyph Distribution — {title}</div>{svg}
</body></html>""", H+30

# ── Sign gallery ──
def build_gallery(signs, title):
    cols=5; cell_w=110; cell_h=110
    rows_n=math.ceil(len(signs)/cols)
    W=cols*cell_w; H=rows_n*cell_h+36
    rows=[]
    rows.append(f'<text x="2" y="22" font-size="12" font-weight="700" fill="#f0c050" font-family="serif">Sign Gallery — {title}</text>')
    for i,(num,lbl,prims,note) in enumerate(signs):
        ro,co=divmod(i,cols)
        ox,oy=co*cell_w,ro*cell_h+30
        svgs=sign_svg(prims,w=cell_w-8,h=cell_h-24,bg="#141008",sc="#f0c050")
        inn=svgs.split(">",1)[1].rsplit("</svg>",1)[0]
        pstr="+".join(dict.fromkeys(prims))
        rows.append(f'<g transform="translate({ox+4},{oy+2})">'
                    f'<rect width="{cell_w-8}" height="{cell_h-4}" fill="#141008" rx="5" stroke="#2e2810" stroke-width="1.2"/>'
                    f'{inn}'
                    f'<text x="{(cell_w-8)//2}" y="{cell_h-18}" text-anchor="middle" font-size="10" fill="#f0c050" font-family="monospace" font-weight="bold">{num}</text>'
                    f'<text x="{(cell_w-8)//2}" y="{cell_h-7}" text-anchor="middle" font-size="7.5" fill="#5a4820" font-family="monospace">{pstr[:20]}</text>'
                    f'</g>')
    svg=(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
         f'<rect width="{W}" height="{H}" fill="#050403"/>{"".join(rows)}</svg>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{BASE_CSS}</head><body>
<div class="ttl">Sign Gallery — {title}</div>{svg}
</body></html>""", H+24

# ══════════════════════════════════════════════════════════════════════════════
# ── APP UI
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{font-family:'Cinzel',serif;color:#e8d8b8;background:#050403;}
.stApp{background:#050403;}
.block-container{padding:1rem 1.4rem;max-width:1700px;}
h1{font-size:1.9rem!important;color:#f0c050!important;text-align:center;letter-spacing:.08em;}
h2,h3{color:#f0c050!important;}
section[data-testid="stSidebar"]{background:#030302!important;border-right:1px solid #2e2810;}
section[data-testid="stSidebar"] *{color:#e8d8b8!important;}
section[data-testid="stSidebar"] label{color:#f0c050!important;font-weight:600;}
.stTabs [data-baseweb="tab-list"]{background:#030302!important;border-bottom:2px solid #2e2810!important;gap:2px;}
.stTabs [data-baseweb="tab"]{background:#050403!important;color:#6a5828!important;font-family:'Cinzel',serif!important;font-size:.88rem!important;font-weight:600!important;border-radius:5px 5px 0 0!important;padding:7px 13px!important;border:1px solid #2e2810!important;border-bottom:none!important;}
.stTabs [aria-selected="true"]{background:#1a1208!important;color:#f0c050!important;border-color:#4a380e!important;}
.stTabs [data-baseweb="tab-panel"]{background:#111008!important;border:1px solid #2e2810;border-top:none;border-radius:0 0 7px 7px;padding:14px!important;}
hr{border-color:#2e2810!important;}
.stRadio label{color:#e8d8b8!important;}
.stCheckbox label{color:#e8d8b8!important;}
.stSelectbox>div>div{background:#111008!important;border:1px solid #3a2e10!important;color:#e8d8b8!important;}
.stSlider>div{color:#e8d8b8!important;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>𒀭 Harappan Script — Glyph Frequency Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#5a4820;font-size:.88rem;margin-bottom:10px;font-family:monospace;'>Two sign sets from Indus Valley script images · Primitive decomposition · 6 chart types</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-size:1rem;font-weight:700;color:#f0c050;border-bottom:1px solid #2e2810;padding-bottom:4px;margin-bottom:10px;'>⚙ Options</div>", unsafe_allow_html=True)
    sort_mode = st.radio("Breakdown sort", ["original order","by complexity ↓"], index=0)
    sort_key  = "order" if "original" in sort_mode else "complexity"

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.9rem;font-weight:700;color:#f0c050;margin-bottom:6px;'>📊 Quick Stats</div>", unsafe_allow_html=True)
    for label,signs,freq in [("Image 1 — Plant/Cross",IMG1_SIGNS,freq1),("Image 2 — Anthropomorph",IMG2_SIGNS,freq2)]:
        tot=sum(freq.values())
        top=freq.most_common(1)[0] if freq else ("—",0)
        st.markdown(f"""<div style='background:#111008;border:1px solid #2e2810;border-radius:5px;padding:8px;margin-bottom:8px;font-family:monospace;font-size:10px;color:#a08040;'>
        <b style='color:#f0c050;'>{label}</b><br>
        Signs: <b style='color:#f0c050;'>{len(signs)}</b> &nbsp;|&nbsp;
        Unique prims: <b style='color:#f0c050;'>{len(freq)}</b><br>
        Total tokens: <b style='color:#f0c050;'>{tot}</b><br>
        Most used: <b style='color:#f0c050;'>{top[0]} ({top[1]}×)</b>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.9rem;font-weight:700;color:#f0c050;margin-bottom:6px;'>Primitive Colour Key</div>", unsafe_allow_html=True)
    all_used = list(dict.fromkeys([p for _,_,pr,_ in IMG1_SIGNS+IMG2_SIGNS for p in pr]))
    for p in all_used:
        col=pcolor(p)
        psvg=mini_prim_svg(p,w=18,h=16,sc=col,bg="#030302")
        pin=psvg.split(">",1)[1].rsplit("</svg>",1)[0]
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:5px;margin:2px 0;'>"
            f"<svg width='18' height='16' xmlns='http://www.w3.org/2000/svg'>{pin}</svg>"
            f"<span style='font-family:monospace;font-size:10px;color:{col};font-weight:600;'>{p}</span>"
            f"<span style='font-size:9px;color:#5a4820;'>{pname(p)}</span>"
            f"</div>", unsafe_allow_html=True)

# ── Two image tabs at top ─────────────────────────────────────────────────────
img_tab1, img_tab2 = st.tabs(["🌿 Image 1 — Plant / Cross Signs", "🧍 Image 2 — Anthropomorphic Signs"])

def render_image_section(signs, all_prims, freq, g2s, s2g, title, sort_key):
    c1,c2,c3,c4,c5,c6 = st.tabs(["🖼 Gallery","🔥 Heatmap","📊 Freq Bar","🔡 Breakdown","🔗 Co-occur","🍩 Distribution"])
    with c1:
        html,h = build_gallery(signs, title)
        components.html(html, height=h, scrolling=False)
    with c2:
        html,h = build_heatmap(signs, all_prims, freq, s2g, title)
        components.html(html, height=h, scrolling=True)
    with c3:
        html,h = build_freq_bar(signs, all_prims, freq, g2s, title)
        components.html(html, height=h, scrolling=False)
    with c4:
        html,h = build_breakdown(signs, title, sort_by=sort_key)
        components.html(html, height=h, scrolling=True)
    with c5:
        html,h = build_comat(signs, all_prims, title)
        components.html(html, height=h, scrolling=True)
    with c6:
        html,h = build_donut(freq, all_prims, title)
        components.html(html, height=h, scrolling=False)

with img_tab1:
    render_image_section(IMG1_SIGNS, ALL_PRIMS1, freq1, g2s1, s2g1, "Plant/Cross Signs", sort_key)

with img_tab2:
    render_image_section(IMG2_SIGNS, ALL_PRIMS2, freq2, g2s2, s2g2, "Anthropomorphic Signs", sort_key)

# ── Cross-image comparison ────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='font-size:1rem;font-weight:700;color:#f0c050;border-bottom:1px solid #2e2810;padding-bottom:3px;margin-bottom:12px;'>⚡ Cross-Image Primitive Comparison</div>", unsafe_allow_html=True)

shared = set(freq1.keys()) & set(freq2.keys())
only1  = set(freq1.keys()) - set(freq2.keys())
only2  = set(freq2.keys()) - set(freq1.keys())

cc1,cc2,cc3 = st.columns(3)
with cc1:
    st.markdown(f"""<div style='background:#1a1200;border:1px solid #c8920a;border-radius:7px;padding:11px;font-size:12px;color:#c8a060;'>
    <b style='color:#f0c050;'>Shared Primitives ({len(shared)})</b><br><br>
    {"<br>".join(f'<span style="color:{pcolor(p)};">■</span> {p} — {pname(p)} &nbsp; <span style="color:#f0c050;">img1:{freq1[p]} img2:{freq2[p]}</span>' for p in sorted(shared,key=lambda x:-(freq1.get(x,0)+freq2.get(x,0))))}
    </div>""", unsafe_allow_html=True)
with cc2:
    st.markdown(f"""<div style='background:#001a0a;border:1px solid #2a7a3a;border-radius:7px;padding:11px;font-size:12px;color:#80c890;'>
    <b style='color:#60bf80;'>Image 1 Only ({len(only1)})</b><br><br>
    {"<br>".join(f'<span style="color:{pcolor(p)};">■</span> {p} — {pname(p)} &nbsp; <span style="color:#60bf80;">×{freq1[p]}</span>' for p in sorted(only1,key=lambda x:-freq1.get(x,0)))}
    </div>""", unsafe_allow_html=True)
with cc3:
    st.markdown(f"""<div style='background:#0a001a;border:1px solid #3a2a7a;border-radius:7px;padding:11px;font-size:12px;color:#8890d0;'>
    <b style='color:#8090ef;'>Image 2 Only ({len(only2)})</b><br><br>
    {"<br>".join(f'<span style="color:{pcolor(p)};">■</span> {p} — {pname(p)} &nbsp; <span style="color:#8090ef;">×{freq2[p]}</span>' for p in sorted(only2,key=lambda x:-freq2.get(x,0)))}
    </div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#3a2e10;font-size:10px;font-family:monospace;'>Harappan Glyph Frequency · Image 1: Plant/Cross (20 signs) · Image 2: Anthropomorphic (19 signs) · 6 chart views each</p>", unsafe_allow_html=True)
