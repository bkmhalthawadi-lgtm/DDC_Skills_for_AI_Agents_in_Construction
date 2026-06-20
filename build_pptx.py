from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
import copy

# ── Colour palette ──────────────────────────────────────────────────────────
NAVY       = RGBColor(0x0D, 0x2B, 0x55)   # dark navy – titles / headers
STEEL      = RGBColor(0x1B, 0x4F, 0x72)   # medium blue
ACCENT     = RGBColor(0xE8, 0x4C, 0x3C)   # red accent – critical
ORANGE     = RGBColor(0xF3, 0x9C, 0x12)   # amber – warning
GREEN      = RGBColor(0x1E, 0x87, 0x56)   # green – approved
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY = RGBColor(0xF4, 0xF6, 0xF7)
MID_GREY   = RGBColor(0xD5, 0xDB, 0xDB)
DARK_GREY  = RGBColor(0x2C, 0x3E, 0x50)
YELLOW_BG  = RGBColor(0xFF, 0xF3, 0xCD)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]   # completely blank layout

# ── Helper utilities ─────────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill=None, line=None, line_w=Pt(0)):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.width = line_w
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
        shape.line.width = line_w
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=12, bold=False, color=DARK_GREY,
             align=PP_ALIGN.LEFT, wrap=True, italic=False,
             v_anchor=None):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    if v_anchor:
        tf.vertical_anchor = v_anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def add_multiline_text(slide, lines, l, t, w, h,
                       font_size=11, bold=False, color=DARK_GREY,
                       align=PP_ALIGN.LEFT, leading_bold=False):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    for i, (txt, bld) in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = txt
        run.font.size  = Pt(font_size)
        run.font.bold  = bld
        run.font.color.rgb = color
    return txb


def slide_header(slide, title, subtitle=None):
    # top navy bar
    add_rect(slide, 0, 0, 13.33, 1.1, fill=NAVY)
    add_text(slide, title, 0.35, 0.12, 11, 0.55,
             font_size=24, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, subtitle, 0.35, 0.65, 11, 0.38,
                 font_size=12, color=RGBColor(0xAE, 0xD6, 0xF1))
    # bottom footer bar
    add_rect(slide, 0, 7.1, 13.33, 0.4, fill=STEEL)
    add_text(slide, "PROJECT P159  |  RFI EXECUTIVE SUMMARY  |  20 JUNE 2026",
             0.3, 7.13, 10, 0.28, font_size=9, color=WHITE)
    add_text(slide, "CONFIDENTIAL", 11, 7.13, 2, 0.28,
             font_size=9, color=WHITE, align=PP_ALIGN.RIGHT)


def section_divider(slide, label, l, t, w=12.6):
    add_rect(slide, l, t, w, 0.28, fill=STEEL)
    add_text(slide, label, l+0.12, t+0.02, w-0.2, 0.24,
             font_size=10, bold=True, color=WHITE)


def kpi_box(slide, l, t, w, h, heading, value, unit, bg_color, icon=""):
    add_rect(slide, l, t, w, h, fill=bg_color, line=MID_GREY, line_w=Pt(1))
    add_text(slide, icon + " " + heading if icon else heading,
             l+0.12, t+0.1, w-0.2, 0.3,
             font_size=9, bold=True, color=WHITE)
    add_text(slide, value, l+0.12, t+0.38, w-0.2, 0.55,
             font_size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, unit, l+0.12, t+0.88, w-0.2, 0.22,
             font_size=8, color=RGBColor(0xD5, 0xDB, 0xDB), align=PP_ALIGN.CENTER)


def table_header_row(slide, cols, l, t, h=0.32):
    x = l
    for (label, w) in cols:
        add_rect(slide, x, t, w, h, fill=NAVY)
        add_text(slide, label, x+0.05, t+0.04, w-0.08, h-0.06,
                 font_size=8.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        x += w


def table_row(slide, cells, col_widths, l, t, h=0.38, bg=WHITE, text_size=8):
    x = l
    for i, (val, w) in enumerate(zip(cells, col_widths)):
        add_rect(slide, x, t, w, h, fill=bg, line=MID_GREY, line_w=Pt(0.5))
        clr = DARK_GREY
        bld = False
        # colour coded status values
        if val in ("HIGH", "🔴 HIGH"):
            clr = ACCENT; bld = True
        elif val in ("MEDIUM-HIGH",):
            clr = RGBColor(0xC0, 0x39, 0x2B); bld = True
        elif val in ("MEDIUM",):
            clr = ORANGE; bld = True
        elif val in ("LOW", "LOW-MEDIUM"):
            clr = GREEN
        add_text(slide, str(val), x+0.05, t+0.04, w-0.08, h-0.06,
                 font_size=text_size, color=clr, bold=bld, wrap=True)
        x += w


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE SLIDE
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, fill=NAVY)
# diagonal accent strip
add_rect(sl, 0, 5.2, 13.33, 0.08, fill=ACCENT)
add_rect(sl, 0, 5.28, 13.33, 2.22, fill=STEEL)

add_text(sl, "RFI EXECUTIVE SUMMARY REPORT", 0.8, 1.4, 11.5, 1.0,
         font_size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Civil & MEP Discipline — Impact Analysis, Improvement Recommendations & Structured Tables",
         0.8, 2.45, 11.5, 0.6,
         font_size=15, color=RGBColor(0xAE, 0xD6, 0xF1), align=PP_ALIGN.CENTER)

add_rect(sl, 4.5, 3.3, 4.33, 0.05, fill=ACCENT)

add_text(sl, "Project Reference: P159", 0.8, 3.7, 11.5, 0.38,
         font_size=13, color=MID_GREY, align=PP_ALIGN.CENTER)
add_text(sl, "Report Date: 20 June 2026", 0.8, 4.08, 11.5, 0.38,
         font_size=13, color=MID_GREY, align=PP_ALIGN.CENTER)
add_text(sl, "Total RFIs Analysed: 27  |  Floors: B1 – 12F", 0.8, 4.46, 11.5, 0.38,
         font_size=13, color=MID_GREY, align=PP_ALIGN.CENTER)

add_text(sl, "CONFIDENTIAL  |  Prepared: AI-Assisted Construction PM Analysis",
         0.8, 5.5, 11.5, 0.38,
         font_size=11, color=RGBColor(0xD5, 0xDB, 0xDB), align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — OVERVIEW / KPI DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Overview — RFI Dashboard", "Project P159 | 27 RFIs across B1–12F")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

# KPI boxes
kpi_box(sl, 0.3,  1.3, 2.8, 1.3, "TOTAL RFIs",        "27",  "entries analysed",    NAVY)
kpi_box(sl, 3.3,  1.3, 2.8, 1.3, "CRITICAL (Open)",    "2",   "unresolved / blocked", ACCENT)
kpi_box(sl, 6.3,  1.3, 2.8, 1.3, "REJECTED",           "3+",  "requiring re-submission", ORANGE)
kpi_box(sl, 9.3,  1.3, 2.8, 1.3, "FLOORS AFFECTED",   "14",  "B1 through 12F",      STEEL)

kpi_box(sl, 0.3,  2.85, 2.8, 1.3, "CIVIL RFIs",         "10",  "structural clashes",  STEEL)
kpi_box(sl, 3.3,  2.85, 2.8, 1.3, "MEP RFIs",           "15",  "drainage / services", STEEL)
kpi_box(sl, 6.3,  2.85, 2.8, 1.3, "ID COORD NEEDED",   "14",  "RFIs require ID sign-off", ORANGE)
kpi_box(sl, 9.3,  2.85, 2.8, 1.3, "MAX DELAY RISK",    "8wk", "drop panel package",  ACCENT)

# Dominant themes
section_divider(sl, "DOMINANT CLASH THEMES", 0.3, 4.35)
themes = [
    ("Insufficient shaft sizes", "MEP risers (drainage + chilled water) cannot fit in existing shaft openings across 7F–12F"),
    ("Unauthorised beam penetrations", "Pipes proposed through structural beams without sleeves — consultant rejections at 9F/10F"),
    ("Floor drain / drop panel clashes", "Floor traps located above structural drop panels — must be relocated before tiling"),
    ("Multi-trade coordination gap", "14 of 27 RFIs blocked pending ID sub-contractor sign-off — no dedicated coordinator"),
]
x_positions = [0.3, 3.45, 6.6, 9.75]
for i, (title, desc) in enumerate(themes):
    x = x_positions[i]
    add_rect(sl, x, 4.7, 3.0, 1.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))
    add_rect(sl, x, 4.7, 3.0, 0.28, fill=STEEL)
    add_text(sl, title, x+0.1, 4.72, 2.8, 0.26, font_size=9, bold=True, color=WHITE)
    add_text(sl, desc,  x+0.1, 5.04, 2.8, 1.48, font_size=9, color=DARK_GREY, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — CRITICAL RFI #1
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Critical RFI #1 — ARC_CRC_KA_042 + ARC_054",
             "7F / 8F (ARC_042)  &  9F / 10F (ARC_054)  |  STATUS: DESIGN DISCUSSION ON-GOING")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

# Red alert banner
add_rect(sl, 0.3, 1.2, 12.73, 0.42, fill=ACCENT)
add_text(sl, "🔴  HIGHEST PRIORITY — FOUR FLOORS BLOCKED — DESIGN INSTRUCTION REQUIRED WITHIN 3 WORKING DAYS",
         0.5, 1.24, 12.4, 0.35, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Two column layout
add_rect(sl, 0.3, 1.72, 6.1, 4.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))
add_rect(sl, 6.55, 1.72, 6.48, 4.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))

# Left col – Issue detail
add_rect(sl, 0.3, 1.72, 6.1, 0.3, fill=NAVY)
add_text(sl, "ISSUE DETAIL", 0.4, 1.74, 5.9, 0.26, font_size=9, bold=True, color=WHITE)

issue_lines = [
    ("What is the problem?", True),
    ("The existing MEP shaft at 7F/8F is undersized. It cannot simultaneously accommodate the DN160 soil/waste drainage riser AND the chilled water pipe riser.", False),
    ("", False),
    ("Structural Impact:", True),
    ("Beam L7-B-08 must be physically shifted 500mm downward to clear the BTU meter. This affects:", False),
    ("  •  Reinforcement schedule: 8LT16@100 + 2LT20@125 bars", False),
    ("  •  Post-tensioned slab drawings (DM submission)", False),
    ("  •  Interior design ceiling heights in occupied zones", False),
    ("", False),
    ("Proposed Solution:", True),
    ("Enlarge shaft to 1,200 × 450mm clear internal dimension.", False),
    ("", False),
    ("Linked RFI:", True),
    ("ARC_054 (9F/10F) carries identical open status — same resolution required.", False),
]
y = 2.1
for (txt, bld) in issue_lines:
    add_text(sl, txt, 0.45, y, 5.8, 0.22, font_size=9, bold=bld, color=DARK_GREY)
    y += 0.21

# Right col – Risk & action
add_rect(sl, 6.55, 1.72, 6.48, 0.3, fill=NAVY)
add_text(sl, "RISK & REQUIRED ACTION", 6.65, 1.74, 6.28, 0.26, font_size=9, bold=True, color=WHITE)

risks = [
    ("Schedule Risk", "HIGH", ACCENT),
    ("Cost Risk", "HIGH", ACCENT),
    ("Floors Blocked", "4 floors (7F, 8F, 9F, 10F)", ORANGE),
    ("Delay Estimate", "3 – 6 weeks", ORANGE),
]
y = 2.1
for (label, val, clr) in risks:
    add_rect(sl, 6.6, y, 6.35, 0.32, fill=LIGHT_GREY, line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, label, 6.72, y+0.04, 2.5, 0.26, font_size=9, bold=True, color=DARK_GREY)
    add_text(sl, val, 9.3, y+0.04, 3.55, 0.26, font_size=9, bold=True, color=clr)
    y += 0.38

y += 0.1
add_rect(sl, 6.55, y, 6.48, 0.28, fill=STEEL)
add_text(sl, "ACTIONS REQUIRED", 6.65, y+0.04, 6.28, 0.22, font_size=9, bold=True, color=WHITE)
y += 0.34
actions = [
    "1.  Escalate to Design Consultant — issue a formal RFI close-out within 3 working days.",
    "2.  Obtain written structural engineer instruction confirming beam shift is acceptable.",
    "3.  Revise PT drawings to reflect new beam position and shaft dimensions.",
    "4.  Update DM submission package before next scheduled authority review.",
    "5.  Simultaneously close ARC_054 (9F/10F) with the same instruction.",
]
for act in actions:
    add_text(sl, act, 6.65, y, 6.2, 0.26, font_size=9, color=DARK_GREY)
    y += 0.3


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — CRITICAL RFI #2
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Critical RFI #2 — ARC_CRC_KA_056",
             "Floors 9F & 10F  |  STATUS: ❌ FORMALLY REJECTED — RE-SUBMISSION REQUIRED")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

add_rect(sl, 0.3, 1.2, 12.73, 0.42, fill=RGBColor(0xC0, 0x39, 0x2B))
add_text(sl, "🔴  CONSULTANT REJECTION — BOTH POINTS NOT ACCEPTED — REVISED PROPOSAL REQUIRED WITHIN 7 DAYS",
         0.5, 1.24, 12.4, 0.35, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_rect(sl, 0.3, 1.72, 6.1, 4.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))
add_rect(sl, 6.55, 1.72, 6.48, 4.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))

add_rect(sl, 0.3, 1.72, 6.1, 0.3, fill=NAVY)
add_text(sl, "CONSULTANT REJECTION DETAIL", 0.4, 1.74, 5.9, 0.26, font_size=9, bold=True, color=WHITE)

left_lines = [
    ("Contractor Proposal:", True),
    ("Route Ø110mm drainage pipe directly through a structural beam without a sleeve.", False),
    ("", False),
    ("Consultant Response — Point 1:", True),
    ('"NOT ACCEPTED. 6" sleeve to be provided for 110 pipe inside beam. Follow the approved structural detail around provided sleeve."', False),
    ("", False),
    ("Consultant Response — Point 2:", True),
    ('"NOT ACCEPTED. 6" sleeve to be provided near the proposal for 110 pipe inside beam. Follow the approved structural detail around provided sleeve."', False),
    ("", False),
    ("Pattern Risk:", True),
    ("Similar non-compliant proposals exist at ARC_057, ARC_058, and ARC_059 — a systemic issue across multiple floors.", False),
]
y = 2.1
for (txt, bld) in left_lines:
    add_text(sl, txt, 0.45, y, 5.8, 0.22, font_size=9, bold=bld,
             color=ACCENT if "NOT ACCEPTED" in txt else DARK_GREY, italic='"' in txt)
    y += 0.25

add_rect(sl, 6.55, 1.72, 6.48, 0.3, fill=NAVY)
add_text(sl, "RISK & REQUIRED ACTION", 6.65, 1.74, 6.28, 0.26, font_size=9, bold=True, color=WHITE)

risks = [
    ("Schedule Risk", "MEDIUM-HIGH", RGBColor(0xC0, 0x39, 0x2B)),
    ("Cost Risk", "MEDIUM", ORANGE),
    ("Re-submission Timeline", "7 days", ORANGE),
    ("Delay per Floor", "2 – 4 weeks", ORANGE),
]
y = 2.1
for (label, val, clr) in risks:
    add_rect(sl, 6.6, y, 6.35, 0.32, fill=LIGHT_GREY, line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, label, 6.72, y+0.04, 2.8, 0.26, font_size=9, bold=True, color=DARK_GREY)
    add_text(sl, val, 9.55, y+0.04, 3.3, 0.26, font_size=9, bold=True, color=clr)
    y += 0.38

y += 0.1
add_rect(sl, 6.55, y, 6.48, 0.28, fill=STEEL)
add_text(sl, "WHAT MUST BE SUBMITTED", 6.65, y+0.04, 6.28, 0.22, font_size=9, bold=True, color=WHITE)
y += 0.34
items = [
    "1.  Revised shop drawings showing 6\" sleeve embedded in beam at correct location.",
    "2.  Structural reinforcement detail around sleeve (pre-approved standard detail).",
    "3.  MEP sub-contractor sign-off confirming pipe routing remains functional.",
    "4.  Audited check of ARC_057, ARC_058, ARC_059 for identical violations — ",
    "     batch re-submission recommended to avoid repeat cycles.",
]
for item in items:
    add_text(sl, item, 6.65, y, 6.2, 0.28, font_size=9, color=DARK_GREY)
    y += 0.3


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — CRITICAL RFI #3
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Critical RFI #3 — ARC_CRC_KA_058",
             "Floors 9F & 10F  |  STATUS: ⚠️ CONDITIONAL — 4-DOCUMENT PACKAGE REQUIRED")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

add_rect(sl, 0.3, 1.2, 12.73, 0.42, fill=ORANGE)
add_text(sl, "⚠️  STRUCTURAL DROP PANEL PENETRATIONS — MULTI-PARTY SUBMISSION BOTTLENECK — 4–8 WEEK DELAY RISK",
         0.5, 1.24, 12.4, 0.35, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_rect(sl, 0.3, 1.72, 6.1, 4.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))
add_rect(sl, 6.55, 1.72, 6.48, 4.9, fill=WHITE, line=MID_GREY, line_w=Pt(1))

add_rect(sl, 0.3, 1.72, 6.1, 0.3, fill=NAVY)
add_text(sl, "ISSUE DETAIL", 0.4, 1.74, 5.9, 0.26, font_size=9, bold=True, color=WHITE)

left_lines = [
    ("Location:", True),
    ("Structural drop panel at 9F/10F — the most critical load-bearing zone in a PT flat plate.", False),
    ("", False),
    ("Pipe Penetrations Required:", True),
    ("  •  Ø160 Soil Pipe  →  8\" sleeve", False),
    ("  •  Ø110 Vent Pipe  →  6\" sleeve", False),
    ("  •  Ø160 Waste Pipe  →  8\" sleeve", False),
    ("", False),
    ("Consultant Condition (not yet approved):", True),
    ("A 4-document package must be submitted simultaneously by three separate parties:", False),
    ("  1.  Tile layout drawing (Tiling Contractor)", False),
    ("  2.  Distance from vertical elements (Structural Engineer)", False),
    ("  3.  Structural sleeve reinforcement details (Structural Engineer)", False),
    ("  4.  Final MEP pipe distribution (MEP Sub-contractor)", False),
    ("", False),
    ("Repeat Risk:", True),
    ("Same issue exists at 7F, 8F, 11F, 12F (ARC_041, ARC_066, ARC_069).", False),
]
y = 2.1
for (txt, bld) in left_lines:
    add_text(sl, txt, 0.45, y, 5.8, 0.2, font_size=9, bold=bld, color=DARK_GREY)
    y += 0.21

add_rect(sl, 6.55, 1.72, 6.48, 0.3, fill=NAVY)
add_text(sl, "RISK & REQUIRED ACTION", 6.65, 1.74, 6.28, 0.26, font_size=9, bold=True, color=WHITE)

risks = [
    ("Schedule Risk", "HIGH", ACCENT),
    ("Cost Risk", "HIGH", ACCENT),
    ("Delay Estimate", "4 – 8 weeks", ORANGE),
    ("Floors at Risk", "7F, 8F, 9F, 10F, 11F, 12F", ORANGE),
]
y = 2.1
for (label, val, clr) in risks:
    add_rect(sl, 6.6, y, 6.35, 0.32, fill=LIGHT_GREY, line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, label, 6.72, y+0.04, 2.6, 0.26, font_size=9, bold=True, color=DARK_GREY)
    add_text(sl, val, 9.35, y+0.04, 3.5, 0.26, font_size=9, bold=True, color=clr)
    y += 0.38

y += 0.1
add_rect(sl, 6.55, y, 6.48, 0.28, fill=STEEL)
add_text(sl, "ACTIONS REQUIRED", 6.65, y+0.04, 6.28, 0.22, font_size=9, bold=True, color=WHITE)
y += 0.34
actions = [
    "1.  Convene multi-party coordination meeting within 5 working days:",
    "     MEP sub-contractor + Structural Engineer + Tiling Contractor.",
    "2.  Appoint a document coordinator to chase all 4 submissions in parallel.",
    "3.  Do NOT commence any penetration or sleeve-fixing before written",
    "     consultant approval is received — structural failure risk.",
    "4.  Apply same process to 7F, 8F, 11F, 12F proactively (batch submission).",
]
for act in actions:
    add_text(sl, act, 6.65, y, 6.2, 0.26, font_size=9, color=DARK_GREY)
    y += 0.28


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — RFI LANGUAGE IMPROVEMENT
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "RFI Language Improvement — Before vs. After",
             "Rewriting vague RFI text for faster consultant response")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

# Headers
add_rect(sl, 0.3,  1.25, 2.5, 0.28, fill=ACCENT)
add_text(sl, "RFI REFERENCE", 0.4, 1.27, 2.3, 0.24, font_size=9, bold=True, color=WHITE)
add_rect(sl, 2.85, 1.25, 4.9, 0.28, fill=RGBColor(0x7B, 0x7D, 0x7D))
add_text(sl, "ORIGINAL (UNCLEAR) LANGUAGE", 2.95, 1.27, 4.7, 0.24, font_size=9, bold=True, color=WHITE)
add_rect(sl, 7.8,  1.25, 5.2, 0.28, fill=GREEN)
add_text(sl, "RECOMMENDED (CLEAR) LANGUAGE", 7.9, 1.27, 5.0, 0.24, font_size=9, bold=True, color=WHITE)

rows = [
    (
        "ARC_042\n7F/8F\nShaft + Beam",
        "SHAFT TO BE 1200x450mm TO ACCOMMODATE DRAINAGE AND CHILLED WATER PIPES RISERS",
        "The shaft at Grid [XX-YY], 7F/8F is undersized for the DN160 soil riser and DN[XX] chilled water riser. Contractor proposes 1,200×450mm clear. Please confirm approval and whether beam L7-B-08 shift 500mm downward is structurally acceptable. Response required by [date] to avoid slab pour delay."
    ),
    (
        "ARC_069\n11F\nBeam Penetrations",
        "THE HIGHLIGTED SHAFT WILL REQUIRED VERTICAL AND HORIZONTAL PENETRATIONS FOR THE BEAM, POINT 2 TO BE RESTRICTED AND COORDINATED WITH MEP CONTRACTOR",
        "MEP shaft at Grid [XX], 11F requires beam penetrations for: Ø160 SP (6\" sleeve), Ø110 VP (6\" sleeve), Ø160 WP (8\" sleeve) — see Engineer's Dwg [Ref.]. Please confirm sleeve sizes, edge distances, and reinforcement detailing. MEP contractor requires approval by [date] to maintain programme."
    ),
    (
        "GEN_028\n2F–4F\nDrain Routing",
        "NO OBJECTION TO THE 50MM DRAIN PIPE RUNNING WITH THE FLOOR SCREED TO THE FLOOR TRAP SUBJECT TO PROPER SLOPE AND PROTECTION. HOWEVER THE KITCHEN FLOOR TRAP CURRENTLY LOCATED ABOVE THE DROP PANEL SHALL BE RELOCATED",
        "A Ø50mm drain runs within floor screed at 2F–4F serving the floor trap. Confirm: (a) minimum screed depth and pipe protection spec; (b) required fall/gradient. The kitchen FT at Grid [XX] is above the drop panel — not permitted. Revised FT location shown on Sketch [Ref.], relocated [X]mm from drop panel edge. Please confirm approval."
    ),
]

bg_alt = [WHITE, LIGHT_GREY, WHITE]
y = 1.6
for i, (ref, orig, good) in enumerate(rows):
    row_h = 1.5
    bg = bg_alt[i]
    add_rect(sl, 0.3,  y, 2.5,  row_h, fill=bg, line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, ref, 0.4, y+0.08, 2.3, row_h-0.12, font_size=8.5, bold=True, color=STEEL)
    add_rect(sl, 2.85, y, 4.9,  row_h, fill=YELLOW_BG, line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, orig, 2.95, y+0.06, 4.7, row_h-0.1, font_size=8, color=DARK_GREY, italic=True)
    add_rect(sl, 7.8,  y, 5.2,  row_h, fill=RGBColor(0xE9, 0xF7, 0xEF), line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, good, 7.9, y+0.06, 5.0, row_h-0.1, font_size=8, color=DARK_GREY)
    y += row_h + 0.05

# Guidelines box
y += 0.05
add_rect(sl, 0.3, y, 12.73, 0.28, fill=NAVY)
add_text(sl, "6 GOLDEN RULES FOR EFFECTIVE RFI WRITING", 0.4, y+0.04, 12.5, 0.22, font_size=9, bold=True, color=WHITE)
y += 0.32
rules = [
    "1. State dimensions and pipe sizes numerically — never 'as highlighted'",
    "2. Separate Background from Question — use distinct headed sections",
    "3. Always include a 'Response Required By' date referencing a programme activity",
    "4. Use sentence case — avoid ALL CAPS text in formal documents",
    "5. Reference related RFIs explicitly by number, not 'as per previous'",
    "6. Every RFI must reference a sketch or drawing — include drawing number",
]
x_r = [0.3, 4.55, 8.8]
for i, rule in enumerate(rules):
    col = i % 3
    row = i // 3
    xp = x_r[col]
    yp = y + row * 0.28
    add_rect(sl, xp, yp, 4.1, 0.26, fill=WHITE, line=MID_GREY, line_w=Pt(0.5))
    add_text(sl, rule, xp+0.08, yp+0.03, 3.95, 0.22, font_size=8, color=DARK_GREY)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — TABLE 1: CIVIL RFIs
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Table 1 — Civil-Specific RFIs",
             "Schedule & Cost Impact Summary  |  Project P159")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

cols = [
    ("RFI NUMBER",     1.6),
    ("LOCATION",       0.9),
    ("ISSUE SUMMARY",  3.2),
    ("STATUS",         1.5),
    ("SCHED. RISK",    0.88),
    ("COST RISK",      0.88),
    ("ACTION",         2.28),
]
col_widths = [c[1] for c in cols]
table_header_row(sl, cols, 0.3, 1.18)

civil_data = [
    ["ARC_042 + ARC_054", "7F/8F\n9F/10F", "Beam L7-B-08 shift 500mm + shaft enlarged to 1,200×450mm for drainage & CHW risers", "⚠️ Design Discussion\nOn-going", "HIGH", "HIGH", "Escalate to design team within 3 days. Formal instruction required."],
    ["ARC_CRC_KA_056",    "9F, 10F",       "Ø110 pipe through beam rejected. 6\" sleeve + structural detail required",            "❌ Not Accepted",           "MEDIUM-HIGH", "MEDIUM", "Re-submit with correct sleeve detail within 7 days"],
    ["ARC_CRC_KA_057",    "7F, 8F",        "Points 2 & 4 rejected: beam penetration not accepted; shaft extension to 500mm clear", "❌ Partially Rejected",    "MEDIUM",      "MEDIUM", "Revise points 2 & 4 per consultant comments and resubmit"],
    ["ARC_CRC_KA_058",    "9F, 10F",       "Ø160/Ø110 pipes through structural drop panel; 4-document package required",          "⚠️ Conditional",           "HIGH",        "HIGH",   "Multi-party meeting within 5 days. Do not penetrate before approval."],
    ["ARC_CRC_KA_059",    "10F",           "6\" slab sleeves require 4T16 reinforcement cage (T&B + diagonals) before DM sub.",    "✅ Cond. Approved",         "MEDIUM",      "LOW-MEDIUM", "Reflect in PT drawings before DM submission"],
    ["ARC_CRC_KA_069",    "11F",           "Shaft requires vertical & horizontal beam penetrations; MEP impact assessment needed", "⚠️ Pending MEP Assess.",   "MEDIUM-HIGH", "MEDIUM", "MEP contractor to submit full impact study within 7 days"],
    ["GEN_CRC_KA_028",    "2F–4F",         "Kitchen floor trap above drop panel — must relocate; 50mm drain in screed approved",  "✅ Cond. Approved",         "LOW-MEDIUM",  "LOW",    "Confirm revised FT location. Coordinate with tiling contractor"],
    ["ARC_CRC_KA_036",    "1F",            "Contractor proposal accepted; cavity must be damp-proofed",                           "✅ Cond. Approved",         "LOW",         "LOW",    "Specify damp-proof system and include in IFC drawings"],
    ["ARC_CRC_KA_041",    "7F, 8F",        "7 shaft modifications: widths extended 250–500mm; sleeves at multiple locations",     "✅ No Objection",           "MEDIUM",      "MEDIUM", "Coordinate with formwork; confirm all shaft dims before pour"],
    ["ARC_CRC_KA_033",    "1F",            "Civil interface — insufficient data in log; status unclear",                          "⚠️ No Response",           "LOW",         "LOW",    "Clarify status; re-submit if still pending"],
]

y = 1.52
alt = [LIGHT_GREY, WHITE]
for i, row_data in enumerate(civil_data):
    row_h = 0.52
    table_row(sl, row_data, col_widths, 0.3, y, h=row_h, bg=alt[i % 2], text_size=7.5)
    y += row_h


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — TABLE 2: MEP RFIs (part 1)
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Table 2 — MEP-Specific RFIs (Part 1 of 2)",
             "Schedule & Cost Impact Summary  |  Project P159")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

mep_cols = [
    ("RFI NUMBER",     1.55),
    ("LOCATION",       0.85),
    ("DISCIPLINE",     1.0),
    ("ISSUE SUMMARY",  3.0),
    ("STATUS",         1.35),
    ("SCHED.",         0.75),
    ("COST",           0.75),
    ("ACTION",         2.23),
]
mep_col_widths = [c[1] for c in mep_cols]
table_header_row(sl, mep_cols, 0.3, 1.18)

mep_data_1 = [
    ["ARC_CRC_KA_042\n(MEP aspect)", "7F, 8F",          "Plumbing /\nMechanical", "Shaft must fit DN160 drainage riser + chilled water riser simultaneously. Linked to beam shift.",                          "⚠️ On-going",       "HIGH",       "HIGH",       "Resolve simultaneously with Civil ARC_042 instruction"],
    ["ARC_CRC_KA_040",               "7F, 8F",          "Plumbing\n(Floor Traps)", "Floor traps moved from beam. ID layout affected. WC FT position needs ID sub-contractor confirmation.",                    "✅ No Objection",   "LOW-MEDIUM", "LOW",        "Formally notify ID sub-contractor; obtain written confirmation"],
    ["ARC_CRC_KA_053",               "B1, B2",          "MEP\n(All Services)",    "Clearance heights +2.70m / +2.50m confirmed in basements only. Separate RFI still needed for Mezzanine/GF.",             "✅ Approved\n(Basements)", "MEDIUM", "LOW",    "Submit Mezzanine/GF clearance RFI immediately"],
    ["ARC_CRC_KA_054",               "9F, 10F",         "Plumbing /\nMechanical", "Same shaft/beam clash as ARC_042. Open design discussion — four floors blocked.",                                          "⚠️ On-going",       "HIGH",       "HIGH",       "Resolve with ARC_042 — same instruction covers both"],
    ["ARC_CRC_KA_055",               "9F, 10F",         "Plumbing\n(Shafts)",     "Follow ARC_040 solution. Tiling coordination required at shaft perimeter on both floors.",                                 "✅ Cond. Approved", "LOW",        "LOW",        "Coordinate with tiling contractor; mark shaft edges on tile drawings"],
    ["ARC_CRC_KA_063",               "Multiple",        "Plumbing\n(Floor Drains)","Floor drain new locations clash with tile joint layout. Shifts required; tile layout approval is a prerequisite.",        "✅ Cond. Approved", "MEDIUM",     "LOW-MEDIUM", "Obtain approved tile layout before finalising floor drain positions"],
    ["ARC_CRC_KA_064",               "11F, 12F",        "Plumbing\n(Shaft)",      "Shaft undersized — extend to minimum 200×200mm clear internal.",                                                           "✅ Approved",       "LOW",        "LOW",        "Revise formwork drawings; confirm with MEP contractor"],
    ["ARC_CRC_KA_068",               "6F",              "MEP\n(All Services)",    "MEP sub-contractor must verify constructability and functionality before any work proceeds.",                              "⚠️ Pending MEP",   "MEDIUM",     "MEDIUM",     "Formally instruct MEP sub-contractor to submit verification within 7 days"],
]

y = 1.52
alt = [LIGHT_GREY, WHITE]
for i, row_data in enumerate(mep_data_1):
    row_h = 0.6
    table_row(sl, row_data, mep_col_widths, 0.3, y, h=row_h, bg=alt[i % 2], text_size=7.5)
    y += row_h


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — TABLE 2: MEP RFIs (part 2)
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Table 2 — MEP-Specific RFIs (Part 2 of 2)",
             "Schedule & Cost Impact Summary  |  Project P159")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

table_header_row(sl, mep_cols, 0.3, 1.18)

mep_data_2 = [
    ["ARC_CRC_KA_065",   "11F, 12F",              "Plumbing",           "Follow GEN_CRC_KA_026 solution and comments — cross-reference approval.",                                 "✅ Approved\n(by ref.)", "LOW",    "LOW",        "Apply GEN_026 solution; confirm applicability with MEP sub-contractor"],
    ["ARC_CRC_KA_066",   "11F",                   "Plumbing\n(FT)",     "6\" sleeve required for floor trap provision before slab pour.",                                          "✅ Approved",            "LOW",    "LOW",        "Procure and install sleeve before slab pour"],
    ["ARC_CRC_KA_044",   "7F–10F",                "Plumbing\n(Powder Rm)", "Powder room drainage approved subject to coordination with ID specialist. Include in IFC drawings.", "✅ No Objection",        "LOW-MEDIUM", "LOW",  "Issue coordination instruction to ID; incorporate in IFC"],
    ["GEN_CRC_KA_023",   "1F–6F",                 "Plumbing\n(Floor Drains)", "Floor drain repositioning across 5 floors. Multi-trade coordination with ID and flooring required.", "✅ No Objection",    "MEDIUM", "LOW-MEDIUM", "Convene multi-trade meeting; lock drain positions before tiling"],
    ["GEN_CRC_KA_024",   "2F–6F,\n11F–12F",       "Plumbing\n(Floor Drains)", "8-point floor drain relocation programme across 7 floors — subject to final approval.",           "✅ Cond. Approved",      "HIGH",   "MEDIUM",     "Submit coordinated drain layout drawing; assign dedicated coordinator"],
    ["GEN_CRC_KA_026",   "3F, 4F, 5F",            "MEP General",        "Updated layout with extra space submitted. Contractor must confirm clash is cleared.",                    "✅ Cond. Approved",      "LOW-MEDIUM", "LOW",  "Contractor to formally close out clash clearance check"],
    ["GEN_CRC_KA_027",   "2F–6F,\n11F–12F",       "MEP General /\nFaçade", "Contractor proposals approved subject to ID and façade coordination across 4 points.",              "✅ No Objection",        "MEDIUM", "MEDIUM",     "Initiate tri-party meeting: MEP + ID + Façade contractor"],
    ["GEN_CRC_KA_029",   "Multiple",              "MEP General",        "General coordination required with ID and all other disciplines. 2 open points.",                        "✅ No Objection",        "LOW",    "LOW",        "Issue coordination instruction; track on weekly RFI register"],
]

y = 1.52
alt = [LIGHT_GREY, WHITE]
for i, row_data in enumerate(mep_data_2):
    row_h = 0.6
    table_row(sl, row_data, mep_col_widths, 0.3, y, h=row_h, bg=alt[i % 2], text_size=7.5)
    y += row_h


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — PRIORITY ACTION REGISTER
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Priority Action Register",
             "7 Actions — Ranked P1 to P4 with Target Dates  |  Project P159")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

p_cols = [
    ("PRIORITY", 0.78),
    ("ACTION",   4.5),
    ("RFIs",     1.6),
    ("OWNER",    2.2),
    ("TARGET",   1.45),
    ("STATUS",   2.5),
]
table_header_row(sl, p_cols, 0.3, 1.18)

actions_data = [
    ["P1 — URGENT", "Escalate ARC_042 & ARC_054 — formal design instruction from consultant required to unblock beam relocation decision", "ARC_042\nARC_054", "Project Manager\n+ Design Manager", "3 working\ndays", "🔴 Immediate Escalation Required"],
    ["P1 — URGENT", "Convene multi-party coordination meeting (MEP sub-contractor, Structural Engineer, Tiling Contractor) for drop panel sleeve package", "ARC_058", "Construction\nManager", "5 working\ndays", "🔴 Meeting Not Yet Scheduled"],
    ["P2 — HIGH",   "Re-submit revised beam penetration proposals with correct 6\" sleeve and approved structural reinforcement detail", "ARC_056\nARC_057", "MEP Sub-contractor\n+ Struct. Engineer", "7 working\ndays", "⚠️ Re-submission Pending"],
    ["P2 — HIGH",   "MEP sub-contractor to submit constructability and functionality verification report (6F)", "ARC_068", "MEP\nSub-contractor", "7 working\ndays", "⚠️ Report Not Submitted"],
    ["P3 — MEDIUM", "Submit separate Mezzanine/GF MEP clearance height RFI (split from ARC_053 — basements only currently approved)", "ARC_053", "MEP\nSub-contractor", "10 working\ndays", "⚠️ RFI Not Yet Submitted"],
    ["P3 — MEDIUM", "Finalise coordinated floor drain location drawings for 2F–12F; submit for consultant approval", "GEN_024\nGEN_023", "MEP + Tiling\nCoordinator", "14 working\ndays", "⚠️ Drawings Pending"],
    ["P4 — ROUTINE","Issue formal ID coordination instructions for all 'NEED TO COORDINATE WITH ID' RFIs — track on weekly register", "ARC_040\nARC_044\nARC_055\nGEN_027", "Architect /\nID Manager", "Rolling —\nweekly", "🟡 Ongoing Coordination"],
]

p_col_widths = [c[1] for c in p_cols]
p_colors = [ACCENT, ACCENT, ORANGE, ORANGE, STEEL, STEEL, GREEN]
y = 1.52
for i, row_data in enumerate(actions_data):
    row_h = 0.71
    bg = [WHITE, LIGHT_GREY][i % 2]
    # Draw cells manually so priority gets colour coded
    x = 0.3
    for j, (val, w) in enumerate(zip(row_data, p_col_widths)):
        cell_bg = bg
        if j == 0:
            cell_bg = p_colors[i]
        add_rect(sl, x, y, w, row_h, fill=cell_bg, line=MID_GREY, line_w=Pt(0.5))
        txt_color = WHITE if j == 0 else DARK_GREY
        add_text(sl, str(val), x+0.06, y+0.05, w-0.1, row_h-0.08,
                 font_size=7.8, bold=(j == 0), color=txt_color, wrap=True)
        x += w
    y += row_h


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — KEY OBSERVATIONS & RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
slide_header(sl, "Key Observations & Strategic Recommendations",
             "Root Causes and Systemic Improvements  |  Project P159")
add_rect(sl, 0, 1.1, 13.33, 5.98, fill=LIGHT_GREY)

obs = [
    (ACCENT,  "1", "Systemic MEP–Civil Interface Failure",
     "The volume of beam penetration rejections (ARC_056, ARC_057, ARC_058) indicates that MEP shop drawings were not sufficiently coordinated with structural drawings before construction commenced. Recommendation: Conduct a formal BIM/Navisworks clash-detection workshop before proceeding to floors 13F and above to prevent the same pattern repeating."),
    (ACCENT,  "2", "Open Design Discussions During Construction",
     "RFIs ARC_042 and ARC_054 remain open with no resolution timeline — this is a primary cause of programme overruns in construction. Open design decisions must be formally closed with a consultant instruction within 72 hours of escalation. A weekly 'open design items' register should be maintained by the Design Manager."),
    (ORANGE,  "3", "Chain-Reference Risk",
     "Several RFIs close by referencing earlier RFIs (ARC_055 → ARC_040; ARC_065 → GEN_026) without standalone resolution. An error in the base RFI propagates to all referencing floors. All cross-referenced solutions must be formally verified as applicable before acceptance, not assumed equivalent."),
    (ORANGE,  "4", "ID Coordination as a Blocking Factor",
     '"NEED TO COORDINATE WITH ID" appears in 14 of 27 RFIs (52%). Interior design approval is a prerequisite for MEP finalisation on every floor. A dedicated MEP–ID Weekly Coordination Register must be established immediately, with a named coordinator accountable for tracking each item to closure.'),
    (GREEN,   "5", "DM Submission at Risk",
     "RFI ARC_059 explicitly requires that sleeve locations and reinforcement be reflected in PT (Post-Tensioned) drawings PRIOR to DM submission. Any delay resolving structural sleeve positions will hold the DM approval cycle for the entire floor plate — a regulatory risk with potential project-wide programme implications."),
]

y = 1.25
box_h = 1.08
for (clr, num, title, detail) in obs:
    add_rect(sl, 0.3, y, 0.42, box_h, fill=clr)
    add_text(sl, num, 0.3, y+0.28, 0.42, 0.5,
             font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(sl, 0.75, y, 12.28, box_h, fill=WHITE, line=MID_GREY, line_w=Pt(0.5))
    add_rect(sl, 0.75, y, 12.28, 0.26, fill=RGBColor(0xEA, 0xEC, 0xEE))
    add_text(sl, title, 0.88, y+0.03, 12.0, 0.22, font_size=9.5, bold=True, color=DARK_GREY)
    add_text(sl, detail, 0.88, y+0.3, 12.05, box_h-0.32, font_size=8.5, color=DARK_GREY, wrap=True)
    y += box_h + 0.04


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 12 — CLOSING SLIDE
# ═══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(BLANK)
add_rect(sl, 0, 0, 13.33, 7.5, fill=NAVY)
add_rect(sl, 0, 4.8, 13.33, 0.08, fill=ACCENT)
add_rect(sl, 0, 4.88, 13.33, 2.62, fill=STEEL)

add_text(sl, "SUMMARY", 0.8, 1.0, 11.5, 0.6,
         font_size=14, bold=True, color=RGBColor(0xAE, 0xD6, 0xF1), align=PP_ALIGN.CENTER)
add_text(sl, "Three RFIs Demand Immediate Escalation",
         0.8, 1.55, 11.5, 0.7,
         font_size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

summary_points = [
    ("ARC_042 + ARC_054", "Beam shift + shaft enlargement — 4 floors blocked — design instruction required within 3 days"),
    ("ARC_056",           "Beam penetration formally rejected — re-submit with correct sleeve detail within 7 days"),
    ("ARC_058",           "Drop panel sleeves — 4-party document package — convene coordination meeting within 5 days"),
]
y = 2.55
for (rfi, desc) in summary_points:
    add_rect(sl, 1.5, y, 10.33, 0.52, fill=RGBColor(0x17, 0x3B, 0x6B), line=ACCENT, line_w=Pt(1.5))
    add_text(sl, rfi,  1.65, y+0.08, 2.2, 0.38, font_size=10, bold=True, color=ACCENT)
    add_text(sl, desc, 3.95, y+0.08, 7.7, 0.38, font_size=10, color=WHITE)
    y += 0.62

add_text(sl, "Project P159  |  RFI Executive Summary  |  20 June 2026  |  CONFIDENTIAL",
         0.8, 5.2, 11.5, 0.38, font_size=11, color=MID_GREY, align=PP_ALIGN.CENTER)

out = "/home/user/DDC_Skills_for_AI_Agents_in_Construction/RFI_Executive_Summary_P159.pptx"
prs.save(out)
print(f"Saved: {out}")
