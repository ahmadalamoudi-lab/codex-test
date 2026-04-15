"""File loading utilities for uploaded attendance and oracle exports."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_table(path_or_buffer) -> pd.DataFrame:
    """Read CSV or Excel into a DataFrame."""
    suffix = ""
    if isinstance(path_or_buffer, (str, Path)):
        suffix = Path(path_or_buffer).suffix.lower()
    else:
        name = getattr(path_or_buffer, "name", "")
        suffix = Path(name).suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path_or_buffer)
    if suffix in {".xls", ".xlsx"}:
        return pd.read_excel(path_or_buffer)

    raise ValueError("Unsupported file format. Please upload CSV or Excel files.")
