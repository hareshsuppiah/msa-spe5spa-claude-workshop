---
name: weekly-load-report
description: Produces the Northfield FC one-page weekly training-load PDF report for the head coach. Aggregates cleaned GPS data per player across the training week, compares to the previous week, flags load spikes, and renders a standardised Typst PDF.
---

# Weekly training-load report

## When to use this skill

Use this skill when the user asks for the "weekly load report", "coach's weekly report", "training-load PDF", or anything that sounds like they want this week's training-load summary for the head coach. Default squad is U23 unless the user says otherwise.

## Inputs

- `data/gps_training_clean.csv` - the current week, cleaned by the Module 4 tool. If this file does not exist, run the cleaner first (rules in `../../module-4-build-a-tool/README.md`) or clean inline using the same rules.
- `data/gps_training_week_prior.csv` - the previous week, tidy by construction.
- `data/squad_roster.csv` - player-to-squad/position map.

If the user passes a different file path for the current week, use that instead.

## What the skill produces

A one-page PDF at the path the user specified (default `weekly_report_<iso-date-of-monday>.pdf` in the current working directory).

The PDF contains, in order:

1. **Header:** "Northfield FC - Weekly Training Load" and the week range (e.g. "20-26 April 2026").
2. **Top-line paragraph:** 2-3 sentences summarising total squad distance, number of sessions, and how the week compares to last week at squad level.
3. **Player table:** one row per player in the chosen squad, sorted by total_distance_m descending. Columns: player_id, position, sessions, total_distance_km, high_speed_running_m, sprint_distance_m, delta_vs_prev_pct. Rows coloured:
   - red if `|delta_vs_prev_pct| > 20`
   - amber if `15 < |delta_vs_prev_pct| <= 20`
   - uncoloured otherwise
4. **Footer:** generated timestamp and the phrase "Synthetic data - teaching use only".

## Aggregation rules

- Week runs Monday to Sunday.
- Only include the current squad (default U23).
- `total_distance_km` = sum of `total_distance_m` across the week, divided by 1000, rounded to 1 decimal.
- `high_speed_running_m` and `sprint_distance_m` = sums across the week, rounded to 0.
- `delta_vs_prev_pct` = `(current_total_distance - prev_total_distance) / prev_total_distance * 100`, rounded to 1 decimal. If a player has no previous-week data, display `-` and do not flag.

## How to fill the template

The Typst template lives at `template.typ` next to this SKILL.md. It expects a JSON blob at `report_data.json` (same folder) with this shape:

```json
{
  "week_label": "20-26 April 2026",
  "squad": "U23",
  "summary_paragraph": "Two pitch sessions this week...",
  "rows": [
    {"player_id": "NF001", "position": "CB", "sessions": 2, "total_distance_km": 14.2, "hsr_m": 980, "sprint_m": 320, "delta_pct": 3.1, "flag": "none"},
    ...
  ],
  "generated_at": "2026-04-26T19:41:00+10:00"
}
```

Write `report_data.json` in this skill folder, then compile with:

```
typst compile skills/weekly-load-report/template.typ <output-pdf-path>
```

Typst resolves `report_data.json` relative to the template file; do not change that path.

## Post-run summary

After producing the PDF, print a short terminal summary:

```
✅ Wrote: <path>
Squad: <squad>
Week: <week_label>
Players included: <n>
Flagged red: <n>
Flagged amber: <n>
```

If no red or amber flags, say "No load flags this week." explicitly - silence looks like a bug.

## Safety

- Never include player real names, only `NF###` IDs. (This repo has no real names, but the rule stands for when you adapt this to a real club.)
- Never write the PDF to a tracked location. Keep it inside the relevant module folder or `outputs/`.
