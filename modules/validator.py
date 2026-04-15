"""Validation for input schemas."""

from __future__ import annotations

from modules.schemas import ORACLE_REQUIRED_COLUMNS, TIME_CARD_REQUIRED_COLUMNS


def _missing_columns(columns: set[str], required: set[str]) -> list[str]:
    return sorted(required - columns)


def validate_time_card_columns(columns: list[str]) -> None:
    missing = _missing_columns(set(columns), TIME_CARD_REQUIRED_COLUMNS)
    if missing:
        raise ValueError(f"Time Card file is missing required columns: {', '.join(missing)}")


def validate_oracle_columns(columns: list[str]) -> None:
    missing = _missing_columns(set(columns), ORACLE_REQUIRED_COLUMNS)
    if missing:
        raise ValueError(f"Oracle file is missing required columns: {', '.join(missing)}")
