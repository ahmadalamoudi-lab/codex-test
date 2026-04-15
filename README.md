# Payroll Attendance Reconciliation Tool

Internal payroll reconciliation web app that compares monthly **Time Card attendance** exports with **Oracle excuses/leave** exports, then produces payroll-ready outputs.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Objectives

The app automates monthly payroll attendance checks by detecting:

- Absences
- Lateness
- Early leave
- Missing punch cases
- Approved leave and excuses
- Work missions / official assignments
- Cases requiring manual review

## Current Stack

- Python
- Streamlit
- Pandas
- XlsxWriter
- Modular business logic under `modules/`

## Workflow

1. Upload monthly Time Card export
2. Upload monthly Oracle excuses/leave export (optional)
3. Match attendance by `employee_id + attendance_date`
4. Apply approved Oracle reasons (leave/excuse/mission, lateness override when configured)
5. Generate monthly and daily payroll outputs plus Excel export

## Core Rules

### Working Week

- Working days: Sunday to Thursday
- Weekend: Friday and Saturday

### Matching Rules

- Primary match: `employee_id + attendance_date`
- Fallback match: `employee_name` when ID is missing
- Fallback matches are flagged as low confidence (`review_required`)

### Status Rules

- No attendance + no approved Oracle reason → `Absent`
- Attendance below daily required hours (default 9h) is still `Present` (not absent)
- Missing check-in/check-out → `Missing Punch`
- Approved `Work Mission` → `Paid Present`
- Approved leave blocks absence deduction
- Attendance + conflicting approved Oracle excuse → `Review Required`

### Lateness Override

If an Oracle reason is approved and configured as a lateness justifier, lateness penalty is canceled.

### Required Hours

- Default standard daily hours: `9`
- Must be configurable from app settings

## Lateness Penalty Policy (Chronological, Monthly Cumulative)

| Band | First Occurrence | Repeated Rule |
|---|---|---|
| Up to 15 min | First 3 times allowed | Every 2 delays = 25% |
| Up to 30 min | First 2 times = 10% | Every delay = 25% |
| More than 30 min | First time = 25% | Every delay = 50% |
| 60+ min | First time = 50% | Every delay = full day + warning |
| Missing punch | Half-day deduction each time | N/A |

## Oracle Monthly Value Mapping (By Total Late Hours)

Use exact match when available; otherwise use nearest lower bracket.

| Late Hours | Oracle Value |
|---|---|
| 4 | 0.37 |
| 8 | 0.74 |
| 12 | 1.11 |
| 16 | 1.482 |
| 24 | 2.22 |

## Outputs

### Monthly Summary

Per employee totals including: present/absent/leave/mission days, lateness counters, late minutes/hours, Oracle value, worked/shortage hours, deductions, payroll note, and review flag.

### Daily Exceptions

Per employee/day details including: check-in/out, worked vs required hours, late/early minutes, Oracle reason, final status, penalty action/percent, Oracle value, exception note, and review flag.

### Export

Single workbook with sheets:

- `monthly_summary`
- `daily_exceptions`
- `processing_log`
