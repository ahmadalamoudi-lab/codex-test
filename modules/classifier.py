"""Status classification rules."""

from __future__ import annotations

import pandas as pd


APPROVED = "approved"


def _is_approved(value: str) -> bool:
    return str(value or "").strip().lower() == APPROVED


def classify_row(row: pd.Series, settings: dict) -> tuple[str, bool, str]:
    worked_hours = float(row.get("worked_hours", 0) or 0)
    oracle_reason = str(row.get("oracle_reason", "") or "").strip().lower()
    approved = _is_approved(row.get("approval_status"))
    clock_in = row.get("clock_in")
    clock_out = row.get("clock_out")

    work_mission_reasons = {r.lower() for r in settings.get("work_mission_reasons", [])}
    leave_reasons = {r.lower() for r in settings.get("leave_reasons", [])}

    if pd.isna(clock_in) or pd.isna(clock_out):
        if approved and oracle_reason in leave_reasons:
            return "Leave", False, "Approved leave with missing punch"
        return "Missing Punch", True, "Missing check-in or check-out"

    if worked_hours <= 0 and not approved:
        return "Absent", False, "No attendance and no approved reason"

    if approved and oracle_reason in work_mission_reasons:
        return "Paid Present", False, "Approved work mission"

    if approved and oracle_reason in leave_reasons:
        return "Leave", False, "Approved leave"

    if worked_hours > 0 and approved and oracle_reason:
        return "Review Required", True, "Attendance conflicts with approved Oracle reason"

    return "Present", bool(row.get("review_required", False)), "Regular attendance"


def classify_daily(df: pd.DataFrame, settings: dict) -> pd.DataFrame:
    result = df.copy()
    statuses = result.apply(lambda r: classify_row(r, settings), axis=1)
    result["final_status"] = statuses.apply(lambda v: v[0])
    result["review_required"] = statuses.apply(lambda v: v[1])
    result["exception_note"] = statuses.apply(lambda v: v[2])
    return result
