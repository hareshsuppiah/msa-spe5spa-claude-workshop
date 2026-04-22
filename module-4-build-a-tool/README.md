# Module 4: Build a GPS data cleaning tool

**Time: 20 minutes**

## The scenario

It is 7pm on a Wednesday. Pat, the Northfield FC sport scientist, has just emailed you `gps_training_messy.csv`. It is this week's training-load export from the GPS vendor. You need to hand a tidy, validated version to the S&C lead by the morning so she can plan Friday's intensity.

Open the file in VS Code and eyeball it. You will notice:

- Mixed date formats (`2026-04-22`, `22/04/2026`, `22 Apr 2026`) in the same column
- The `session` column has "MD-3 HIGH INTENSITY", "md-3 high intensity", "Md-3 High Intensity" - case and spacing chaos
- Some `player_id` values have trailing whitespace (`"NF015 "`)
- Most Wednesday rows have an empty `max_speed_ms` - the GPS firmware glitched and lost that field for one session
- A few rows have `total_distance_m` values over 25,000 - clearly the unit came off and recorded nonsense
- At least one duplicate row
- Empty rows at the bottom

A professional cleaning tool handles all of these deterministically. A bad cleaning tool silently drops rows and you only find out when the coach asks "why is my striker missing from Wednesday?".

## What you are going to build

A Python script, `clean_gps.py`, that reads `data/gps_training_messy.csv`, produces a tidy output `data/gps_training_clean.csv`, and prints a short plain-English summary of exactly what it changed and why.

We are going to build it **with Claude**, not alone. Our job is to direct, review, and verify. Claude does the typing.

## Start a Claude Code session

From the repo root:

```
cd /workspaces/msa-spe5spa-claude-workshop/module-4-build-a-tool
claude
```

## Step 1: describe the problem before asking for code

A classic beginner mistake is to open with "write me a python script that cleans this CSV". Claude will guess at what "clean" means, produce something plausible, and you will spend twenty minutes fixing its assumptions.

Instead, start with this:

```
I have a messy GPS training CSV at ../data/gps_training_messy.csv. Before you write any code, read the file and list every data-quality issue you can see in it. Do not fix anything yet.
```

Claude will read the file, scan for issues, and reply with a list. Read that list carefully. If it missed something, tell it. If it made up a problem that is not really there, say so. **This back-and-forth is the work.**

## Step 2: agree on the cleaning rules

Now you decide, row by row, how each issue should be handled. Prompt something like:

```
Good list. Here is how I want each handled:

- Mixed date formats: parse all of them, output ISO 8601 (YYYY-MM-DD).
- Inconsistent session labels: normalise to lowercase with underscores (e.g. "md-3_high_intensity").
- Trailing whitespace on player_id: strip it.
- Missing max_speed_ms: keep the row but set max_speed_ms to NA, do not drop the row.
- total_distance_m > 18000 metres: flag as implausible, drop the row, and log which player/session was dropped.
- Duplicate rows (same date + player_id + session): keep the first occurrence, drop the rest.
- Empty rows: drop.

The script should print a short summary at the end showing: rows read, rows written, rows dropped (and why).

Write the script in Python using pandas. Put it in clean_gps.py in this folder.
```

Notice how specific that prompt is. Every rule is explicit. No guessing.

## Step 3: review the code before running it

Claude will produce `clean_gps.py`. **Before you run it, open it and read it.** This is non-negotiable. Two minutes of reading saves twenty minutes of debugging mystery output.

Look for:

- Does it actually implement every rule you asked for?
- Does it drop rows silently anywhere?
- Does the summary it prints match the rules?

If you see something wrong, tell Claude:

```
You are filtering on max_speed_ms being null instead of just flagging it - please change it to preserve those rows.
```

## Step 4: run it

```
python clean_gps.py
```

You should see a summary print out. Something like:

```
Read: 347 rows from ../data/gps_training_messy.csv
Dropped: 2 duplicate rows
Dropped: 3 implausible total_distance_m values (>18000m):
  - NF024 on 2026-04-22 (MD-3 high intensity): 30682.5m
  - NF047 on 2026-04-24 (MD-1 activation): 21199.8m
  - NF003 on 2026-04-20 (Recovery): 24401.6m
Dropped: 2 empty rows
Wrote: 340 rows to ../data/gps_training_clean.csv
```

That is a good tool. It tells you exactly what happened.

## Step 5: verify

Open the clean file and spot-check:

```
head ../data/gps_training_clean.csv
```

- Dates should all be ISO 8601
- Session labels should be lowercase with underscores
- No trailing spaces on player IDs
- No rows with total_distance_m over 18,000

If anything looks off, loop back with Claude.

## Step 6 (stretch): write a test

Ask Claude:

```
Write a small test file test_clean_gps.py that feeds clean_gps.py a tiny synthetic input with each issue seeded, and asserts the output is correct.
```

Run it:

```
python test_clean_gps.py
```

A tool you trust is a tool that is tested. An analyst with tests will be taken seriously by the engineers in your club.

## What you learned

- **Prompt the problem, not the solution.** "Tell me what is wrong" gets you further than "fix this".
- **Agree on rules explicitly.** Every silent assumption is a future bug.
- **Read the code before running it.** Always.
- **Verify the output against what you expected.** Always.

These four habits separate an analyst who uses Claude well from one who uses it badly. They apply to every task in Modules 5-7.

## Done

You have a cleaning tool. Move on:

```
cd /workspaces/msa-spe5spa-claude-workshop/module-5-automate-report
```
