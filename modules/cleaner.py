"""Data cleaning helpers."""

from __future__ import annotations

import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized.columns = [str(c).strip().lower().replace(" ", "_") for c in normalized.columns]
    return normalized


def normalize_common_fields(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()

    if "employee_id" in normalized.columns:
        normalized["employee_id"] = normalized["employee_id"].astype("string").str.strip()
    if "employee_name" in normalized.columns:
        normalized["employee_name"] = normalized["employee_name"].astype("string").str.strip()
    if "attendance_date" in normalized.columns:
        normalized["attendance_date"] = pd.to_datetime(normalized["attendance_date"], errors="coerce").dt.date
    if "start_datetime" in normalized.columns:
        normalized["start_datetime"] = pd.to_datetime(normalized["start_datetime"], errors="coerce")
    if "end_datetime" in normalized.columns:
        normalized["end_datetime"] = pd.to_datetime(normalized["end_datetime"], errors="coerce")

    for col in ["late_duration", "early_leave_duration", "worked_hours"]:
        if col in normalized.columns:
            normalized[col] = pd.to_numeric(normalized[col], errors="coerce").fillna(0)

    return normalized
