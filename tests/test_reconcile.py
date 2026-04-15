import pandas as pd

from modules.reconcile import reconcile


def _sample_time_card() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "employee_id": "100",
                "employee_name": "Alice",
                "attendance_date": "2026-04-01",
                "department": "HR",
                "scheduled_start": "09:00",
                "scheduled_end": "18:00",
                "clock_in": "09:05",
                "clock_out": "18:00",
                "worked_hours": 8.9,
                "late_duration": 5,
                "early_leave_duration": 0,
            },
            {
                "employee_id": "200",
                "employee_name": "Bob",
                "attendance_date": "2026-04-01",
                "department": "IT",
                "scheduled_start": "09:00",
                "scheduled_end": "18:00",
                "clock_in": None,
                "clock_out": "18:00",
                "worked_hours": 0,
                "late_duration": 0,
                "early_leave_duration": 0,
            },
        ]
    )


def _sample_oracle() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "employee_id": "200",
                "employee_name": "Bob",
                "oracle_reason": "sick leave",
                "approval_status": "approved",
                "start_datetime": "2026-04-01 00:00:00",
                "end_datetime": "2026-04-01 23:59:59",
                "department": "IT",
                "comments": "approved leave",
            }
        ]
    )


def _settings() -> dict:
    return {
        "required_daily_hours": 9,
        "work_mission_reasons": ["work mission", "official assignment"],
        "leave_reasons": ["annual leave", "sick leave", "unpaid leave"],
    }


def test_reconcile_basic_flow_with_oracle():
    monthly, daily = reconcile(_sample_time_card(), _sample_oracle(), _settings())

    assert not monthly.empty
    assert not daily.empty
    assert {"final_status", "penalty_percent", "oracle_value"}.issubset(daily.columns)
    bob_row = daily[daily["employee_name"] == "Bob"].iloc[0]
    assert bob_row["final_status"] == "Leave"


def test_reconcile_without_oracle_file():
    _, daily = reconcile(_sample_time_card(), None, _settings())

    assert not daily.empty
    assert daily["oracle_reason"].fillna("").eq("").all()
