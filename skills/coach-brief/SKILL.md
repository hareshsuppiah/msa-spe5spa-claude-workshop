---
name: coach-brief
description: Produces a 3-sentence weekly training-load brief for the head coach, phrased for quick reading on a phone. No PDF, no tables - just a short message with traffic-light emoji for flagged players.
---

# Coach brief

## When to use this skill

Use this skill when the user (via the comms-bot profile) asks for "the brief", "weekly brief", "coach update", or similar. Not for technical staff - the `weekly-load-report` skill is for them.

## Inputs

Same inputs as `weekly-load-report`:

- `data/gps_training_clean.csv` (or equivalent - clean the messy file first if needed)
- `data/gps_training_week_prior.csv`
- `data/squad_roster.csv`
- `data/athlete_wellness.csv` (use the last 7 days to cross-check flagged players)

## Output

A single text message (no file attachment) with exactly this shape:

- **Sentence 1:** one-line on the week at squad level (sessions completed, trend vs last week).
- **Sentence 2:** the players to watch, each with a traffic-light emoji and a one-phrase reason. Maximum 3 players in this sentence.
- **Sentence 3:** the "what to do about it" line - usually "worth a conversation with Kira before Friday" or "nothing to flag, squad is on plan".

Example (good):

> Squad completed 3 sessions this week, total load up 4% on last week. 🔴 NF014 (WM) is +22% on last week - tough Wednesday; 🔴 NF021 (FW) is -21%, missed Friday. Worth a quick call with Pat before Friday's session.

Example (bad - too long, too technical):

> The U23 squad completed three training sessions totalling 362.4km of cumulative distance across 22 players, with weekly totals up 4.2% relative to the prior training week. NF014 recorded a weekly delta of +22.4% driven primarily by elevated high-speed-running on Wednesday's MD-3 session...

## Rules

- Maximum three traffic-light players. If there are more flags, pick the three largest absolute deltas.
- Use 🔴 / 🟡 / 🟢 only. No other emoji.
- No PDF. No tables. No attachments.
- If nothing is flagged, say "nothing to flag, squad is on plan" in sentence 3. Do not go silent.
- Do not hedge with "maybe" or "possibly". The coach reads between sessions; he needs clarity.

## Safety

- Never include real names. `NF###` IDs only.
- If the coach asks for a specific player's details that would reveal medical information (e.g. "is NF014 injured?"), redirect to Kira or Pat rather than answering from load/wellness data alone.
