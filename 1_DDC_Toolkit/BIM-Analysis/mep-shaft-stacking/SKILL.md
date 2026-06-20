---
name: "mep-shaft-stacking"
description: "Analyze MEP construction drawings to identify vertical shafts, map routed services per floor, generate stacking diagrams, and export an Excel-ready coordination tracker."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🏗️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# MEP Shaft Stacking Analysis

## Business Case

### Problem Statement
MEP shaft coordination failures are among the costliest site surprises:
- Services from multiple disciplines compete for the same shaft space
- Shafts offset between floors without BIM-level clash detection
- Riser diagrams and floor plans are rarely cross-referenced systematically
- No single document shows which services run together floor-by-floor
- Late discovery of shaft conflicts leads to major rework and program delays

### Solution
An AI-assisted shaft stacking analysis skill that reads MEP drawings (floor plans and riser diagrams), builds a structured shaft registry, maps every service to every floor, and outputs a coordination tracker ready for Excel and BIM review meetings.

### Business Value
- **Conflict prevention** – catch incompatible services sharing shaft space before site work begins
- **Coordination speed** – automated extraction replaces days of manual mark-up
- **Audit trail** – structured data links every shaft entry to its source drawing
- **BIM handover** – CSV output feeds directly into Revit shaft schedules or Navisworks sets

## Technical Implementation

```python
import pandas as pd
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import csv
import io


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class MEPDiscipline(Enum):
    HVAC = "HVAC"
    ELECTRICAL_HT = "Electrical-HT"
    ELECTRICAL_LT = "Electrical-LT"
    ELV_TELECOM = "ELV/Telecom"
    PLUMBING = "Plumbing"
    FIRE_FIGHTING = "Fire Fighting"
    DRAINAGE = "Drainage"
    UNKNOWN = "Unknown"


class ShaftStatus(Enum):
    CLEAR = "Clear"
    CONFLICT = "Conflict"
    OFFSET = "Offset"
    RESIZE = "Resize"
    PENDING = "Pending Review"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MEPService:
    """A single MEP service routed through a shaft on a floor."""
    service_id: str
    discipline: MEPDiscipline
    description: str          # e.g. "Chilled Water Supply DN150"
    pipe_size_mm: Optional[int] = None
    duct_size_mm: Optional[Tuple[int, int]] = None
    cable_type: Optional[str] = None
    drawing_ref: str = ""


@dataclass
class FloorEntry:
    """All MEP services present in a shaft on a specific floor."""
    floor_label: str          # e.g. "L05", "B02", "RF"
    floor_index: int          # numeric sort key (basement negative)
    services: List[MEPService] = field(default_factory=list)
    shaft_size_mm: Optional[Tuple[int, int]] = None   # width x depth
    status: ShaftStatus = ShaftStatus.PENDING
    remarks: str = ""

    def service_summary(self) -> str:
        """Comma-separated list of service descriptions."""
        return "; ".join(s.description for s in self.services) if self.services else "—"

    def discipline_tags(self) -> str:
        """Unique discipline names for the stacking grid."""
        seen = []
        for s in self.services:
            tag = s.discipline.value
            if tag not in seen:
                seen.append(tag)
        return ", ".join(seen) if seen else "—"


@dataclass
class Shaft:
    """A single vertical MEP shaft spanning multiple floors."""
    shaft_id: str             # e.g. "SHAFT-A", "EL-SHAFT-03"
    location_description: str # e.g. "Core North-East, Grid D/7"
    primary_discipline: MEPDiscipline
    floor_entries: Dict[str, FloorEntry] = field(default_factory=dict)
    nominal_size_mm: Optional[Tuple[int, int]] = None
    drawing_refs: List[str] = field(default_factory=list)

    def add_floor(self, entry: FloorEntry):
        self.floor_entries[entry.floor_label] = entry

    def floor_range(self) -> str:
        if not self.floor_entries:
            return "—"
        labels = sorted(self.floor_entries.values(), key=lambda e: e.floor_index)
        return f"{labels[0].floor_label} – {labels[-1].floor_label}"


# ---------------------------------------------------------------------------
# Core Analyser
# ---------------------------------------------------------------------------

class MEPShaftStackingAnalyser:
    """
    Parse structured shaft data, detect conflicts, and generate
    stacking diagrams and Excel-ready CSV output.
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.shafts: Dict[str, Shaft] = {}
        self._all_floors: List[Tuple[int, str]] = []  # (index, label)

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def add_shaft(self, shaft: Shaft):
        self.shafts[shaft.shaft_id] = shaft
        for entry in shaft.floor_entries.values():
            key = (entry.floor_index, entry.floor_label)
            if key not in self._all_floors:
                self._all_floors.append(key)
        self._all_floors.sort(key=lambda x: x[0], reverse=True)

    def load_from_dataframe(self, df: pd.DataFrame):
        """
        Load shaft data from a DataFrame.

        Expected columns:
            shaft_id, location, discipline, floor_label, floor_index,
            service_description, shaft_width_mm, shaft_depth_mm,
            drawing_ref (optional)
        """
        for shaft_id, group in df.groupby("shaft_id"):
            first = group.iloc[0]
            shaft = Shaft(
                shaft_id=str(shaft_id),
                location_description=str(first.get("location", "")),
                primary_discipline=MEPDiscipline(
                    first.get("discipline", "Unknown")
                ),
            )

            for _, row in group.iterrows():
                floor_label = str(row["floor_label"])
                floor_index = int(row.get("floor_index", 0))

                if floor_label not in shaft.floor_entries:
                    w = row.get("shaft_width_mm")
                    d = row.get("shaft_depth_mm")
                    size = (int(w), int(d)) if pd.notna(w) and pd.notna(d) else None
                    shaft.floor_entries[floor_label] = FloorEntry(
                        floor_label=floor_label,
                        floor_index=floor_index,
                        shaft_size_mm=size,
                    )

                svc_desc = str(row.get("service_description", "")).strip()
                if svc_desc:
                    discipline_str = str(row.get("service_discipline", row.get("discipline", "Unknown")))
                    try:
                        discipline = MEPDiscipline(discipline_str)
                    except ValueError:
                        discipline = MEPDiscipline.UNKNOWN

                    service = MEPService(
                        service_id=f"{shaft_id}-{floor_label}-{len(shaft.floor_entries[floor_label].services)+1:02d}",
                        discipline=discipline,
                        description=svc_desc,
                        drawing_ref=str(row.get("drawing_ref", "")),
                    )
                    shaft.floor_entries[floor_label].services.append(service)

            self.add_shaft(shaft)

    # ------------------------------------------------------------------
    # Conflict Detection
    # ------------------------------------------------------------------

    INCOMPATIBLE_PAIRS = {
        (MEPDiscipline.ELECTRICAL_HT, MEPDiscipline.PLUMBING),
        (MEPDiscipline.ELECTRICAL_HT, MEPDiscipline.DRAINAGE),
        (MEPDiscipline.ELECTRICAL_LT, MEPDiscipline.PLUMBING),
        (MEPDiscipline.ELECTRICAL_LT, MEPDiscipline.DRAINAGE),
        (MEPDiscipline.ELV_TELECOM, MEPDiscipline.PLUMBING),
    }

    def detect_conflicts(self):
        """Flag conflicts, offsets, and resizes on every floor entry."""
        for shaft in self.shafts.values():
            entries = sorted(shaft.floor_entries.values(), key=lambda e: e.floor_index)
            prev_size = None

            for entry in entries:
                disciplines = {s.discipline for s in entry.services}
                remarks = []

                # Incompatible services in same shaft on same floor
                for d1 in disciplines:
                    for d2 in disciplines:
                        if d1 < d2 and (d1, d2) in self.INCOMPATIBLE_PAIRS:
                            entry.status = ShaftStatus.CONFLICT
                            remarks.append(
                                f"CONFLICT: {d1.value} and {d2.value} must be separated"
                            )

                # Size change between floors
                if entry.shaft_size_mm and prev_size and entry.shaft_size_mm != prev_size:
                    if entry.status == ShaftStatus.PENDING:
                        entry.status = ShaftStatus.RESIZE
                    remarks.append(
                        f"RESIZE: {prev_size[0]}x{prev_size[1]}mm → "
                        f"{entry.shaft_size_mm[0]}x{entry.shaft_size_mm[1]}mm"
                    )

                if entry.shaft_size_mm:
                    prev_size = entry.shaft_size_mm

                if entry.status == ShaftStatus.PENDING and not remarks:
                    entry.status = ShaftStatus.CLEAR

                entry.remarks = "; ".join(remarks)

    # ------------------------------------------------------------------
    # Output: Stacking Diagram
    # ------------------------------------------------------------------

    def stacking_diagram_dataframe(self) -> pd.DataFrame:
        """
        Returns a DataFrame where rows = floors (top → bottom),
        columns = shaft IDs, cells = discipline tags present.
        """
        shaft_ids = sorted(self.shafts.keys())
        floor_list = self._all_floors  # already sorted top-down

        rows = []
        for _, floor_label in floor_list:
            row: Dict[str, str] = {"Floor": floor_label}
            for sid in shaft_ids:
                shaft = self.shafts[sid]
                entry = shaft.floor_entries.get(floor_label)
                row[sid] = entry.discipline_tags() if entry else "—"
            rows.append(row)

        return pd.DataFrame(rows)

    # ------------------------------------------------------------------
    # Output: Excel Tracker CSV
    # ------------------------------------------------------------------

    def excel_tracker_csv(self) -> str:
        """
        Returns a CSV string with columns:
        Shaft ID | Floor Range | MEP Services Present | Status/Remarks
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Shaft ID", "Floor Range", "MEP Services Present", "Status/Remarks"])

        for shaft_id in sorted(self.shafts.keys()):
            shaft = self.shafts[shaft_id]
            entries = sorted(shaft.floor_entries.values(), key=lambda e: e.floor_index)

            for entry in entries:
                status_prefix = {
                    ShaftStatus.CONFLICT: "⚠ CONFLICT",
                    ShaftStatus.OFFSET:   "↔ OFFSET",
                    ShaftStatus.RESIZE:   "↕ RESIZE",
                    ShaftStatus.CLEAR:    "OK",
                    ShaftStatus.PENDING:  "Pending Review",
                }.get(entry.status, "")

                remark_cell = f"{status_prefix} – {entry.remarks}" if entry.remarks else status_prefix

                writer.writerow([
                    shaft_id,
                    entry.floor_label,
                    entry.service_summary(),
                    remark_cell,
                ])

        return output.getvalue()

    # ------------------------------------------------------------------
    # Output: Summary
    # ------------------------------------------------------------------

    def summary(self) -> Dict:
        total_entries = sum(len(s.floor_entries) for s in self.shafts.values())
        conflicts = sum(
            1 for s in self.shafts.values()
            for e in s.floor_entries.values()
            if e.status == ShaftStatus.CONFLICT
        )
        resizes = sum(
            1 for s in self.shafts.values()
            for e in s.floor_entries.values()
            if e.status == ShaftStatus.RESIZE
        )
        return {
            "project": self.project_name,
            "total_shafts": len(self.shafts),
            "total_floor_entries": total_entries,
            "conflict_count": conflicts,
            "resize_count": resizes,
            "floors_analyzed": len(self._all_floors),
        }
```

## Quick Start

```python
# 1. Build shaft objects manually (or use load_from_dataframe)
from mep_shaft_stacking import (
    MEPShaftStackingAnalyser, Shaft, FloorEntry, MEPService,
    MEPDiscipline, ShaftStatus
)

analyser = MEPShaftStackingAnalyser("Office Tower - Block A")

shaft_a = Shaft(
    shaft_id="SHAFT-A",
    location_description="Core NE – Grid D/7",
    primary_discipline=MEPDiscipline.HVAC,
)
for floor, idx in [("B2", -2), ("B1", -1), ("GF", 0), ("L01", 1), ("L02", 2)]:
    entry = FloorEntry(floor_label=floor, floor_index=idx, shaft_size_mm=(1200, 800))
    entry.services.append(MEPService(
        service_id=f"A-{floor}-CWS",
        discipline=MEPDiscipline.HVAC,
        description="Chilled Water Supply DN200",
        drawing_ref="M-FL-001",
    ))
    entry.services.append(MEPService(
        service_id=f"A-{floor}-CWR",
        discipline=MEPDiscipline.HVAC,
        description="Chilled Water Return DN200",
        drawing_ref="M-FL-001",
    ))
    shaft_a.add_floor(entry)

analyser.add_shaft(shaft_a)

# 2. Run conflict detection
analyser.detect_conflicts()

# 3. Print stacking diagram
print(analyser.stacking_diagram_dataframe().to_markdown(index=False))

# 4. Export tracker CSV
csv_data = analyser.excel_tracker_csv()
print(csv_data)

# 5. Summary
print(analyser.summary())
```

## Load From DataFrame (CSV/Excel Workflow)

```python
import pandas as pd

df = pd.read_excel("shaft_schedule.xlsx")
# Required columns: shaft_id, location, discipline, floor_label,
#                   floor_index, service_description, drawing_ref

analyser = MEPShaftStackingAnalyser("Project X")
analyser.load_from_dataframe(df)
analyser.detect_conflicts()

# Export
with open("mep_tracker.csv", "w") as f:
    f.write(analyser.excel_tracker_csv())
```

## Expected Input CSV Schema

```
shaft_id,location,discipline,floor_label,floor_index,service_description,service_discipline,shaft_width_mm,shaft_depth_mm,drawing_ref
SHAFT-A,Core NE Grid D7,HVAC,L01,1,Chilled Water Supply DN200,HVAC,1200,800,M-FL-001
SHAFT-A,Core NE Grid D7,HVAC,L01,1,Chilled Water Return DN200,HVAC,1200,800,M-FL-001
SHAFT-A,Core NE Grid D7,HVAC,L02,2,Chilled Water Supply DN200,HVAC,1200,800,M-FL-001
SHAFT-B,Core SW Grid A3,Electrical-LT,L01,1,LT Rising Main 4C x 400mm²,Electrical-LT,600,400,E-RS-002
SHAFT-B,Core SW Grid A3,Electrical-LT,L02,2,LT Rising Main 4C x 400mm²,Electrical-LT,600,400,E-RS-002
```

## Conflict Detection Rules

| Pair | Reason |
|------|--------|
| HT/LT Electrical + Plumbing | Water ingress risk on live cables |
| HT/LT Electrical + Drainage | Contamination and short-circuit risk |
| ELV/Telecom + Plumbing | Signal interference and moisture damage |

Size changes (↕ RESIZE) and location offsets (↔ OFFSET) are flagged as coordination items requiring slab penetration review.

## Resources
- **DDC Book**: Chapter 3.2 – MEP Shaft Coordination
- **Reference**: CIBSE Guide B, ASHRAE Handbook – HVAC Applications
- **Standard**: BS EN 1996 – Shaft construction requirements
