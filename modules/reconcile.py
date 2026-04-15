"""Reconciliation pipeline orchestration."""

from __future__ import annotations

import pandas as pd

from modules.calculator import apply_monthly_penalties
from modules.classifier import classify_daily
from modules.cleaner import normalize_columns, normalize_common_fields
from modules.exporter import build_daily_exceptions, build_monthly_summary
from modules.matcher import match_attendance
from modules.schemas import ORACLE_REQUIRED_COLUMNS
from modules.validator import validate_oracle_columns, validate_time_card_columns


def _empty_oracle_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=sorted(ORACLE_REQUIRED_COLUMNS))


def reconcile(
    time_card_df: pd.DataFrame,
    oracle_df: pd.DataFrame | None,
    settings: dict,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    time_card = normalize_common_fields(normalize_columns(time_card_df))
    validate_time_card_columns(list(time_card.columns))

    if oracle_df is None:
        oracle = _empty_oracle_frame()
    else:
        oracle = normalize_common_fields(normalize_columns(oracle_df))
        validate_oracle_columns(list(oracle.columns))

    merged = match_attendance(time_card, oracle)
    classified = classify_daily(merged, settings)
    with_penalties = apply_monthly_penalties(classified)

    daily = build_daily_exceptions(with_penalties)
    monthly = build_monthly_summary(daily)
    return monthly, daily
