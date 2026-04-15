"""Penalty and oracle value calculations."""

from __future__ import annotations

import pandas as pd


ORACLE_LATE_HOURS_MAP = {
    4: 0.37,
    8: 0.74,
    12: 1.11,
    16: 1.482,
    24: 2.22,
}


def late_duration_to_minutes(value: float) -> int:
    return int(round(float(value or 0)))


def get_oracle_value(total_late_hours: float) -> float:
    brackets = sorted(ORACLE_LATE_HOURS_MAP.keys())
    selected = 0
    for bracket in brackets:
        if total_late_hours >= bracket:
            selected = bracket
        else:
            break
    return ORACLE_LATE_HOURS_MAP.get(selected, 0.0)


def apply_penalty_band(late_minutes: int, occurrence_index: int) -> float:
    if late_minutes <= 0:
        return 0.0

    if late_minutes <= 15:
        return 0.0 if occurrence_index <= 3 else (25.0 if occurrence_index % 2 == 0 else 0.0)
    if late_minutes <= 30:
        return 10.0 if occurrence_index <= 2 else 25.0
    if late_minutes < 60:
        return 25.0 if occurrence_index == 1 else 50.0
    return 50.0 if occurrence_index == 1 else 100.0


def apply_monthly_penalties(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["late_minutes"] = result["late_duration"].apply(late_duration_to_minutes)
    result["penalty_percent"] = 0.0

    for employee_id, idx in result.groupby("employee_id").groups.items():
        employee_rows = result.loc[idx].sort_values("attendance_date")
        occurrence = 0
        for row_index, row in employee_rows.iterrows():
            if row["late_minutes"] > 0:
                occurrence += 1
                result.at[row_index, "penalty_percent"] = apply_penalty_band(row["late_minutes"], occurrence)

    return result
