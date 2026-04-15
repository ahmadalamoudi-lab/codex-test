"""Schema constants for logical columns used across the app."""

TIME_CARD_REQUIRED_COLUMNS = {
    "employee_id",
    "employee_name",
    "attendance_date",
    "department",
    "scheduled_start",
    "scheduled_end",
    "clock_in",
    "clock_out",
    "worked_hours",
    "late_duration",
    "early_leave_duration",
}

ORACLE_REQUIRED_COLUMNS = {
    "employee_id",
    "employee_name",
    "oracle_reason",
    "approval_status",
    "start_datetime",
    "end_datetime",
    "department",
    "comments",
}

OUTPUT_MONTHLY_COLUMNS = [
    "employee_id",
    "employee_name",
    "department",
    "present_days",
    "absent_days",
    "leave_days",
    "mission_days",
    "missing_punch_days",
    "review_days",
    "late_minutes_total",
    "late_hours_total",
    "oracle_value",
]

OUTPUT_DAILY_COLUMNS = [
    "employee_id",
    "employee_name",
    "attendance_date",
    "department",
    "clock_in",
    "clock_out",
    "worked_hours",
    "late_duration",
    "early_leave_duration",
    "oracle_reason",
    "approval_status",
    "final_status",
    "review_required",
    "late_minutes",
    "penalty_percent",
    "oracle_value",
    "exception_note",
]
