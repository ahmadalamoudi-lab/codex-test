"""Configuration loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_default_settings() -> dict[str, Any]:
    return {
        "required_daily_hours": 9,
        "approved_status_values": ["approved"],
        "lateness_justifier_reasons": ["medical excuse", "official permission"],
        "work_mission_reasons": ["work mission", "official assignment"],
        "leave_reasons": ["annual leave", "sick leave", "unpaid leave"],
    }
