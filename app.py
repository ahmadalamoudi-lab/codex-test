from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from modules.config import get_default_settings
from modules.exporter import build_export_workbook
from modules.loader import read_table
from modules.reconcile import reconcile

st.set_page_config(page_title="Payroll Attendance Reconciliation", layout="wide")
st.title("Payroll Attendance Reconciliation Tool")

settings_path = Path("config/app_settings.json")
if settings_path.exists():
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
else:
    settings = get_default_settings()

with st.sidebar:
    st.header("Settings")
    settings["required_daily_hours"] = st.number_input(
        "Required daily hours",
        min_value=1.0,
        max_value=24.0,
        value=float(settings.get("required_daily_hours", 9)),
        step=0.5,
    )

time_card_file = st.file_uploader("Upload Time Card export (CSV/XLSX)", type=["csv", "xls", "xlsx"])
oracle_file = st.file_uploader(
    "Upload Oracle excuses/leave export (Optional, CSV/XLSX)",
    type=["csv", "xls", "xlsx"],
)

if st.button("Reconcile", type="primary"):
    if not time_card_file:
        st.error("Please upload the Time Card file first.")
    else:
        try:
            time_card_df = read_table(time_card_file)
            oracle_df = read_table(oracle_file) if oracle_file else None
            monthly_df, daily_df = reconcile(time_card_df, oracle_df, settings)

            if oracle_file:
                st.success("Reconciliation completed successfully.")
            else:
                st.info("Reconciliation completed without Oracle file (Oracle columns remain blank).")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Monthly Summary")
                st.dataframe(monthly_df, use_container_width=True)
            with col2:
                st.subheader("Daily Exceptions")
                st.dataframe(daily_df, use_container_width=True)

            workbook = build_export_workbook(monthly_df, daily_df)
            st.download_button(
                "Download Excel Report",
                data=workbook,
                file_name="payroll_reconciliation.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as exc:  # noqa: BLE001
            st.exception(exc)
