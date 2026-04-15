"""Output generation for monthly and daily sheets."""

from __future__ import annotations

from io import BytesIO

import pandas as pd

from modules.calculator import get_oracle_value
from modules.schemas import OUTPUT_DAILY_COLUMNS, OUTPUT_MONTHLY_COLUMNS


def build_monthly_summary(daily_df: pd.DataFrame) -> pd.DataFrame:
    grouped = daily_df.groupby(["employee_id", "employee_name", "department"], dropna=False)

    summary = grouped.agg(
        present_days=("final_status", lambda s: int((s == "Present").sum())),
        absent_days=("final_status", lambda s: int((s == "Absent").sum())),
        leave_days=("final_status", lambda s: int((s == "Leave").sum())),
        mission_days=("final_status", lambda s: int((s == "Paid Present").sum())),
        missing_punch_days=("final_status", lambda s: int((s == "Missing Punch").sum())),
        review_days=("review_required", lambda s: int(s.fillna(False).sum())),
        late_minutes_total=("late_minutes", "sum"),
    ).reset_index()

    summary["late_hours_total"] = summary["late_minutes_total"] / 60.0
    summary["oracle_value"] = summary["late_hours_total"].apply(get_oracle_value)

    for col in OUTPUT_MONTHLY_COLUMNS:
        if col not in summary.columns:
            summary[col] = 0

    return summary[OUTPUT_MONTHLY_COLUMNS]


def build_daily_exceptions(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.copy()
    daily["oracle_value"] = daily["late_minutes"].div(60).apply(get_oracle_value)

    for col in OUTPUT_DAILY_COLUMNS:
        if col not in daily.columns:
            daily[col] = ""

    return daily[OUTPUT_DAILY_COLUMNS]


def build_export_workbook(monthly_df: pd.DataFrame, daily_df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        monthly_df.to_excel(writer, sheet_name="monthly_summary", index=False)
        daily_df.to_excel(writer, sheet_name="daily_exceptions", index=False)
        pd.DataFrame({"event": ["reconciliation_completed"]}).to_excel(
            writer, sheet_name="processing_log", index=False
        )
    output.seek(0)
    return output.read()
