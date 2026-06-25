# CAD Drawing Audit Report
**File:** `dec8e4de-P159SDMEPMACCRCKA023GF_HL_Coordination.dwg`  
**Audited by:** Senior CAD Engineer / Design Auditor (AI-Assisted)  
**Audit Date:** 2026-06-25  
**Tool Used:** Binary DWG analysis (AC1032 / AutoCAD 2018–2020 format)

---

## 1. Document Overview

**Drawing Type:** Multi-Discipline MEP & Building Services Coordination Drawing (Highlighted Clash/Coordination Overlay)

**File Format:** AutoCAD DWG — Format version AC1032 (AutoCAD 2018/2019/2020 compatible), saved by **AutoCAD 2023 Build T.53.0.0 (x64)**

**Paper Size:** ISO A0 (841 mm × 1189 mm) — Full bleed layout

**Scale:** Mixed-scale coordination drawing. Primary reference scale appears to be **1:50 (Metric50)** based on embedded viewport/plot style names. Individual detail callouts vary.

**Units:** Metric (millimetres)

**Creation Date:** 2025-10-06  
**Last Modified:** 2026-06-16  
**File Size:** ~18.6 MB (large — contains embedded raster imagery and extensive block libraries)

**Description:**  
This is a project-level MEP coordination drawing for **Project P159** (reference code `P159SDMEP`). The `HL_Coordination` suffix denotes a **Highlighted Coordination** overlay — a composite drawing that superimposes all building services disciplines (Mechanical, Electrical, Plumbing, Structural, Drainage, Fire Protection) to identify and resolve spatial clashes before installation. The drawing covers multiple floor levels: **Basement 01, Basement 02, Ground Floor, First Floor, and Mezzanine Level**. An associated Revit model is referenced (`22_517-YMA-SD-XX-M3-0-00.rvt`), indicating a BIM-linked workflow.

---

## 2. Component Key (What It Stands For)

### Floor Levels
| Label | Meaning |
|---|---|
| `GROUND FLOOR PLAN` | Ground-level services layout |
| `FIRST FLOOR PLAN` | First floor level building services |
| `BASEMENT FLOOR PLAN / BASEMENT 01 / BASEMENT 02` | Below-grade mechanical/utility space plans |
| `MEZZANINE LEVEL FRAMING PLAN` | Intermediate structural level with framing layout |
| `-0.468 FFL/SSL` | Spot elevation: Finished Floor Level / Structural Slab Level at −468 mm below datum |

### Fire Protection & Detection Systems
| Symbol / Label | Meaning |
|---|---|
| `SMOKE DETECTOR` / `BH-SAD225` | Ceiling-mounted smoke detector (addressable), model SAD225 by BH brand |
| `HEAT DETECTOR` / `A) HEAT DETECTOR` | Thermal detector triggered by temperature rise |
| `MULTI DETECTOR` / `A) MULTI DETECTOR` | Combined smoke + heat detector in single unit |
| `DUCT SPRINKLER` | Sprinkler head inside ductwork for fire suppression |
| `CO2 5KG` | 5 kg CO₂ fire extinguisher (clean-agent suppression) |
| `Dry Powder FE-2` / `2.5KG DCP` | 2.5 kg Dry Chemical Powder portable extinguisher |
| `FHRC S TYPE` | Fire Hose Reel Cabinet — surface-mounted type |
| `ZCV` / `AZCV` | Zone Control Valve / Automatic Zone Control Valve (wet-pipe sprinkler zone isolation) |
| `BOP 3` / `BOP 3100` / `BOP 3050` / `BOP 2735` | Branch-Off Points with invert/centreline elevations (mm above datum) — sprinkler pipework |
| `65 SPj` | 65 mm diameter sprinkler pipe junction |
| `150 WRP F/B` | 150 mm Wet Riser Pipe — Feed/Branch connection |
| `WRP T/A` / `GCRP T/A` | Wet Riser Pipe / Gaseous Clean-agent Riser Pipe — Top/Access |
| `L/Z` / `F/B` | Lock/Zone valve; Feed/Branch configuration label |

### HVAC & Air Distribution
| Symbol / Label | Meaning |
|---|---|
| `GCE-AT-Slot Diffuser Side Conn Bottom Flow Supply - 1 Slot 16mm` | Linear slot ceiling diffuser, single slot, 16 mm opening, supply air |
| `GCE-AT-Slot Diffuser Side Conn Bottom Flow Supply - 2 Slot 20mm` | Linear slot ceiling diffuser, two slots, 20 mm opening, supply air |
| `GCE-AT-Slot Diffuser Side Conn Bottom Flow Return - 16mm / 6mm` | Linear slot diffuser for return air |
| `GCE-AT-RLBG Side Return Grille N - Standard` | Return air grille, sidewall/low-profile, standard neck |
| `GCE-AT-Slot Diffuser Side Conn Top Conn Supply` | Ceiling supply diffuser with top plenum connection |

### Plumbing & Drainage
| Symbol / Label | Meaning |
|---|---|
| `GCE-PX-Valve Chamber - Standard` | Prefabricated valve chamber/access pit for underground pipe network |
| `ISOLATION VALVE` | Shut-off valve for section isolation |
| `BIB TRAP` | Bibb trap — a plumbing syphon trap (typically at floor drain or sanitary connection) |
| `D-Riser` | Drainage riser pipe — vertical pipe carrying waste/drainage between floors |
| `GCE-DT-Breakline Pip - 100 Scale` | Drawing convention break-line symbol for pipe continuation at 1:100 scale |
| `13A SS IP65` | 13-amp stainless-steel switched socket with IP65 (weatherproof) rating |

### Electrical
| Symbol / Label | Meaning |
|---|---|
| `CABLE TRA[Y] -2 WITH COVER` | Cable tray, 2-unit width, with solid lid/cover (for protected wiring) |
| `150MM` (cable tray) | 150 mm wide cable tray |
| `ASL-CB-TYPE1` / `ASL-CB-TYPE4` | Cable bracket/support types 1 and 4 from ASL (cable support manufacturer) |
| `CRW-XX` | Cable runway/tray — size XX (parametric block with variable width) |
| `GCE-Electrical Fixture-Weather Proof 1` | Weatherproof electrical fitting (e.g., IP65 light fixture or junction box) |
| `MODEL_EARTHING SCHEMATIC DIAGRAM` | Earthing layout schematic embedded in the coordination model space |
| `SC-WA[LL]` | Surface conduit — wall-mounted |

### Structural Elements
| Symbol / Label | Meaning |
|---|---|
| `M_Concrete-Rectangular Column - 350x800` | Revit-family concrete column, 350 mm × 800 mm cross-section |
| `Spot Elevation` | Survey point showing finished floor or structural slab level |
| `V17-MEZZANINE LEVEL FRAMING PLAN` | Version 17 of the mezzanine structural framing plan |

### Drawing Standards & Linework
| Label | Meaning |
|---|---|
| `LINEAR` | Standard linear dimensioning style |
| `HATCH ANSI31` | ANSI steel/general material hatch (45° diagonal lines) |
| `HATCH ANSI37` | ANSI brass/bronze hatch pattern |
| `ISO_full_bleed_A0` | ISO standard A0 paper layout (full bleed, no border trim) |
| `CENTER (.5x)` | Centreline linetype at 0.5× global scale |
| `_BACKGROUND` | Background reference layer (non-plot or greyed-out XREF layer) |
| `PLOTST[YLE]` | Named plot style table assignment |
| `STANDARD` | Default text or dimension style |

### Block Library Prefixes
| Prefix | Meaning |
|---|---|
| `GCE-` | Generic Construction Element — parametric MEP families (Revit-to-AutoCAD converted blocks) |
| `ASL-CB-` | ASL Cable Bracket block family |
| `BH-` | Brand-specific detection equipment (e.g., BH-SAD225 detector) |
| `A1-New Title Sheet` | Title block template "A1 New" from ARCHCORP-AR standard library |
| `AecArchBase80` | AutoCAD Architecture 2007 legacy AEC object class (archi background) |

---

## 3. Design & Drafting Review

### Finding 1
**Status:** 🔴 Critical Error  
**Location/Element:** External Reference (XREF) Paths — All Floor Levels  
**Mistake Identified:**  
The drawing contains XREF references linked to a hard-coded network UNC path: `\\Ruel\...\MEP ENGINEERING 15.04.13\XREF\floor-...`. Two critical problems exist:  
(a) The path timestamp `15.04.13` indicates these XREFs were last confirmed on 13 April 2015 — **over 10 years old** relative to the drawing's 2025 creation date. The linked files may be outdated revisions or no longer represent the current design.  
(b) Drive letter fragments (`K:\`, `d:\D1`, `X:\\`) are also embedded, indicating absolute local-path XREFs that will fail to resolve on any machine other than the original workstation.  

**How to Solve:**  
1. In AutoCAD, open the **External References** palette: `XREF` → Enter (or `Ctrl+7`).  
2. For each XREF listed, right-click → **Change Path** → convert all to **Relative Paths** (project-root-relative).  
3. Alternatively use `ETRANSMIT` to bundle all XREFs and the host file into a self-contained transmittal package, which auto-corrects all paths.  
4. Verify each XREF is on the **correct issued revision** by cross-referencing the project document register.  
5. Remove stale path entries that point to pre-2020 folders.

---

### Finding 2
**Status:** 🔴 Critical Error  
**Location/Element:** Legacy AEC Objects — Architectural Background Layers  
**Mistake Identified:**  
The file contains `AecArchBase80` objects — AutoCAD Architecture 2007 AEC proxy objects. These are embedded in the drawing but will display as **simple rectangular placeholders (proxy graphics)** in any installation of AutoCAD that does not have AutoCAD Architecture 2007+ loaded. On standard AutoCAD 2023, users will see a "proxy object" warning and the elements (walls, slabs, windows, doors) will not display correctly or will appear as bounding boxes, corrupting the coordination check.  

**How to Solve:**  
1. Open the drawing in **AutoCAD Architecture** (same or newer version than 2007).  
2. Use `AECEXPLODETOSOLID` or `EXPLODE` on AEC objects to convert them to standard AutoCAD geometry (lines, polylines, hatches).  
3. Alternatively, in AutoCAD 2023: type `PROXYGRAPHICS` → set to `1` to store proxy graphics so the shapes display in non-Architecture installs, though they remain non-editable.  
4. For a clean coordination drawing, export the architectural background as a plain DWG (no AEC objects) from AutoCAD Architecture using **File → Export → AutoCAD DWG** with the "Explode AEC Objects" option checked.

---

### Finding 3
**Status:** 🟡 Flagged  
**Location/Element:** Mixed 2D/3D Geometry — Modelspace  
**Mistake Identified:**  
The drawing contains `MemberElevationDesign`, `AecSpaceTriangleD`, `Sill`, and `Spot Elevation` entities — confirming a **mix of 2D plan-view geometry and 3D elements** in the same modelspace. In a coordination drawing, 3D solids or surfaces that are not consistently projected to a single Z-elevation (plan = Z=0) will cause:  
- Incorrect clash detection if overlaid without proper cut-plane heights  
- Viewport display anomalies (elements appearing at wrong locations in 2D paper space views)  
- Sluggish performance on large A0 sheets  

**How to Solve:**  
1. Type `FLATTEN` in AutoCAD to reduce all geometry to Z=0. **Before running:** confirm all 3D spot elevations and structural slab levels are recorded in annotation (TEXT/MTEXT) so data is not lost.  
2. Alternatively, use `PLAN` command to verify the drawing is viewed from the correct UCS plan before creating new viewports.  
3. Separate 3D coordination geometry into a distinct layer (e.g., `3D-COORD`) that can be frozen in 2D plan views.

---

### Finding 4
**Status:** 🟡 Flagged  
**Location/Element:** Font Substitution Risk — Text and Annotation  
**Mistake Identified:**  
The drawing references multiple font types:  
- `A_Swis721 Cn BT` (Bitstream Swiss 721 Condensed — commercial font, rarely installed on engineering workstations)  
- `ROMAN.shx` and `SIMPLE.shx` (AutoCAD SHX legacy fonts)  
- `Arial` (Windows TrueType)  
- `RomanS.shx` / `style4`  
  
When the drawing is opened on a system without `Swis721 Cn BT` installed, AutoCAD will **substitute a default font** (usually `txt.shx`), causing text to become wider/narrower, overwriting dimension strings, or colliding with other annotation — making the coordination notes unreadable.  

**How to Solve:**  
1. Open **Format → Text Style** in AutoCAD.  
2. Identify all text styles using `A_Swis721 Cn BT` and replace with `Arial Narrow` (closest freely-available equivalent) or an AutoCAD SHX font like `ROMANS.shx`.  
3. Run `STYLE` command and set a single standard text style (e.g., `STANDARD` using `Arial`) for all annotation text in the coordination drawing.  
4. Run `REGEN` and `REGENALL` to rebuild display after font changes.  
5. If the project standard requires Swis721, ensure it is included in the `ETRANSMIT` package or placed in the AutoCAD `Fonts` folder on all workstations.

---

### Finding 5
**Status:** 🟡 Flagged  
**Location/Element:** Hatch Patterns — Material Indication Throughout  
**Mistake Identified:**  
The drawing uses **ANSI31** (steel — US standard) and **ANSI37** (brass — US standard) hatch patterns for material indication. On a project using **ISO/BS metric standards** (confirmed by metric units and ISO A0 paper size), ANSI hatches are non-compliant. The correct ISO hatch equivalents should be used (`ISO` prefix hatches or BS1192-compliant patterns). Additionally, `ANSI37` (brass) is unusual in a concrete/steel MEP coordination context — it may have been applied incorrectly to masonry or insulation areas.  

**How to Solve:**  
1. Select all ANSI31 hatches using `QSELECT` → Entity type: `Hatch` → Property: Pattern Name = `ANSI31`.  
2. Use **Properties palette** (`Ctrl+1`) to change Pattern to `LINE` (ISO equivalent for general sections) or `EARTH` / `GRAVEL` as appropriate for the material.  
3. For ANSI37 hatches: investigate the intended material. If it represents insulation, use `INSUL` hatch. If structural steel, use `STEEL`. If masonry, use `AR-BRSTD` or `AR-CONC`.  
4. Document the hatch legend in a drawing notes table and cross-check against the project's drawing standards schedule.

---

### Finding 6
**Status:** 🟡 Flagged  
**Location/Element:** Structural Spot Elevation — `-0.468 FFL/SSL`  
**Mistake Identified:**  
A spot elevation of **−0.468 m (−468 mm)** is annotated as `FFL/SSL` (Finished Floor Level / Structural Slab Level). Using a single label for both FFL and SSL is ambiguous — these are typically different levels separated by the floor finishes build-up (screed, tile, etc., typically 75–150 mm). Conflating both into one annotation creates a coordination error: MEP services set to FFL may be coordinated at the wrong level relative to the structural slab, causing clashes with slab penetrations or downstand beams.  

**How to Solve:**  
1. Confirm the structural drawings (referenced Revit model `22_517-YMA-SD-XX-M3-0-00.rvt`) for the actual SSL and the architectural drawings for FFL.  
2. Separate the annotation into two distinct labels: `SSL = −0.xxx` and `FFL = −0.xxx` with the actual measured values for each.  
3. Update any MEP service invert levels, BOP elevations (BOP 3100, BOP 3050, BOP 2735), and drainage inverts in this drawing to be explicitly referenced to SSL or FFL — not both.

---

### Finding 7
**Status:** 🟡 Flagged  
**Location/Element:** Drawing Title Block — `A1-New Title Sheet` / ARCHCORP-AR  
**Mistake Identified:**  
The title block block name is `A1-New Title Sheet` referencing the `ARCHCORP-AR` library. However, the drawing's document number format (`P159SDMEPMACCRCKA023GF`) suggests a **multi-discipline MEP project**, not an architectural project. The title block may belong to the architectural consultant's template and may not contain correct MEP-specific fields (e.g., System Responsible Engineer, Discipline Code, MEP revision cloud tracking). Additionally, no discipline-specific stamp, consultant logo, or "ISSUED FOR COORDINATION" status stamp is visible in the metadata.  

**How to Solve:**  
1. Open the title block definition: `INSERT` panel → double-click the title block → enter the block editor.  
2. Verify all mandatory fields are filled: Project Name, Project Number (`P159`), Drawing Number, Revision, Date, Drawn By, Checked By, Approved By, Scale, Discipline (MEP/Building Services), Issue Status.  
3. Replace the `ARCHCORP-AR` title block with the MEP consultant's approved title block template if required by the project BEP (BIM Execution Plan).  
4. Add a "HIGHLIGHTED COORDINATION ISSUE" revision cloud and delta symbol wherever this drawing captures a live coordination clash.

---

### Finding 8
**Status:** 🟡 Flagged  
**Location/Element:** File Size & Embedded Raster Images — All Sheets  
**Mistake Identified:**  
At **18.6 MB**, this coordination DWG is significantly larger than a typical 2D MEP coordination drawing (usually 2–5 MB for A0 sheets). Binary analysis confirms **embedded PNG-format raster images** within the file (IDAT/IHDR signatures detected). Large embedded images:  
- Slow viewport regeneration and zooming  
- Cause crashes on older workstations with < 8 GB RAM  
- Bloat transmittal packages  
- Cannot be updated without re-embedding  

**How to Solve:**  
1. Type `IMAGEHIGHLIGHT` / `IMAGEFRAME` to locate all inserted raster images.  
2. Use `IMAGE` command (External References palette) to identify attached image files.  
3. For each embedded image: right-click → **Detach**, then re-attach as an external file reference (not embedded).  
4. If images must remain in the file, use `PURGE` (type `PURGE` → Purge All) to remove unused image definitions.  
5. After purging, use **Drawing Utilities → Audit** (`AUDIT` command → Y to fix errors) to check for database integrity.  
6. Consider splitting the coordination drawing into separate discipline sheets (M-sheet for Mechanical, E-sheet for Electrical, etc.) if the file size remains over 10 MB.

---

### Finding 9
**Status:** 🟡 Flagged  
**Location/Element:** Dynamic Block History Cache — Block Definitions  
**Mistake Identified:**  
The file contains `ACAD_ENHANCEDBLOCKHISTORY`, `ACAD_ENHANCEDBLOCKHISTORYDATA`, and `AcDbDynamicBlockRoundTripPurgePreventer` records. These are ghost-history records created when dynamic blocks are modified or round-tripped between different AutoCAD versions (including Revit export). They **cannot be purged through the standard PURGE command** and inflate the file size. In rare cases they cause file corruption warnings on open.  

**How to Solve:**  
1. In AutoCAD, type `BATTMAN` (Block Attribute Manager) — this refreshes the block table.  
2. Use the `PURGE` command with the **Purge Nested Items** checkbox enabled and run it **3–4 times** until nothing is removed (dynamic block history is sometimes nested).  
3. For thorough cleanup: `WBLOCK` (write block) the entire drawing content to a new file (`WBLOCK` → `*` for entire drawing) — this strips all orphaned database records including block history.  
4. Alternatively, use the **overkill** plugin (`OVERKILL` command) to eliminate duplicate and overlapping geometry, then save to a new file.

---

### Finding 10
**Status:** 🟢 Pass (Observation)  
**Location/Element:** MEP Block Library — GCE-* blocks  
**Observation:**  
The `GCE-` prefixed blocks (GCE-AT-Slot Diffuser, GCE-PX-Valve Chamber, GCE-DT-Breakline Pip, GCE-Fire Alarm-Smoke Detector, GCE-Electrical Fixture) follow a consistent, structured naming convention using discipline prefix codes (AT = Air Terminal, PX = Plumbing Fixture, DT = Duct/Drawing Tool, AT = Air Terminal). This is good practice and aligns with BS8541-1 Library Object Standards for construction BIM.  

**Recommendation:**  
Ensure that the GCE block library version matches the project's approved BIM Component Library version. Verify that each block contains correct `ATTDEF` attribute data (tag, prompt, default value) for downstream data extraction (e.g., equipment schedules, O&M manuals).

---

## 4. Summary Table

| # | Status | Issue | Priority |
|---|---|---|---|
| 1 | 🔴 Critical | Broken/absolute XREF paths — files will not load | Fix Immediately |
| 2 | 🔴 Critical | Legacy AEC proxy objects — display as blank shapes in AutoCAD | Fix Before Issue |
| 3 | 🟡 Flagged | Mixed 2D/3D geometry in modelspace — clash detection unreliable | Fix Before Coordination Review |
| 4 | 🟡 Flagged | Missing commercial font `Swis721 Cn BT` — text will corrupt on other machines | Fix Before Distribution |
| 5 | 🟡 Flagged | US ANSI hatch patterns on ISO metric project — non-compliant | Correct in Next Revision |
| 6 | 🟡 Flagged | FFL/SSL conflated in spot elevation — coordination ambiguity | Clarify Before MEP Set-Out |
| 7 | 🟡 Flagged | Architectural title block used on MEP document — incomplete/incorrect fields | Update in Next Revision |
| 8 | 🟡 Flagged | Oversized file with embedded raster images — performance/transmittal risk | Fix Before Next Issue |
| 9 | 🟡 Flagged | Orphaned dynamic block history records — database bloat and potential corruption | Fix via WBLOCK/PURGE |
| 10 | 🟢 Pass | GCE block naming is consistent and well-structured | No Action Required |

---

## 5. Recommended Immediate Actions (Priority Order)

1. **Run `AUDIT` + `PURGE` + `WBLOCK *`** to create a clean file copy, stripping AEC proxies, block history, and embedded images.
2. **Resolve all XREFs** using `ETRANSMIT` to create a self-contained package with relative paths — confirm every XREF is on the current project revision.
3. **Convert AEC objects** to standard AutoCAD geometry by opening in AutoCAD Architecture and exploding to standard entities before re-issuing.
4. **Fix font references**: Replace `Swis721 Cn BT` with `Arial Narrow` or `ROMANS.shx` across all text styles.
5. **Clarify spot elevation** `-0.468 FFL/SSL` by separating into `SSL` and `FFL` values sourced from the structural engineer.
6. **Reissue drawing** with correct MEP title block, adding "ISSUED FOR COORDINATION" status stamp and revision cloud markups for all flagged clashes.

---

*This report was generated using automated binary analysis of the DWG file. A full graphical review in AutoCAD or equivalent software is recommended to supplement this report, particularly for dimensioning completeness, clash clash visualization, and annotation legibility at plotted scale.*
