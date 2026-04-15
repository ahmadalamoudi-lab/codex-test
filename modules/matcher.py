"""Matching logic for attendance and oracle entries."""

from __future__ import annotations

import pandas as pd


def prepare_oracle_with_date(oracle_df: pd.DataFrame) -> pd.DataFrame:
    prepared = oracle_df.copy()
    prepared["start_datetime"] = pd.to_datetime(prepared.get("start_datetime"), errors="coerce")
    prepared["attendance_date"] = prepared["start_datetime"].dt.date
    return prepared


def match_attendance(time_card_df: pd.DataFrame, oracle_df: pd.DataFrame) -> pd.DataFrame:
    oracle_prepared = prepare_oracle_with_date(oracle_df)

    merged_by_id = time_card_df.merge(
        oracle_prepared,
        on=["employee_id", "attendance_date"],
        how="left",
        suffixes=("", "_oracle"),
    )

    needs_fallback = merged_by_id["oracle_reason"].isna() & merged_by_id["employee_name"].notna()

    if needs_fallback.any() and not oracle_prepared.empty:
        by_name = time_card_df.loc[needs_fallback].merge(
            oracle_prepared,
            on=["employee_name", "attendance_date"],
            how="left",
            suffixes=("", "_oracle"),
        )
        fallback_map = by_name.set_index(time_card_df.loc[needs_fallback].index)
        for col in ["oracle_reason", "approval_status", "comments", "department_oracle", "employee_id_oracle"]:
            if col in fallback_map.columns:
                merged_by_id.loc[needs_fallback, col] = fallback_map[col]
        merged_by_id.loc[needs_fallback, "review_required"] = fallback_map["oracle_reason"].notna()

    merged_by_id["review_required"] = merged_by_id.get("review_required", False).fillna(False)
    return merged_by_id
