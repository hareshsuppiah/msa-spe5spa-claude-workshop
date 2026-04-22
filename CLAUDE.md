# Project context for Claude

This is the MSA Claude Code workshop repo. Everything in it is a learning exercise for Master of Sport Analytics students who are new to Claude Code.

## Fictional setting

We are a performance analytics team at **Northfield FC**, an academy-level soccer club. The club runs one senior squad (22 players, U23) and two academy squads (U18, U16). We handle:

- GPS training-load monitoring (sessions logged in the `data/` folder)
- Strength and conditioning screening (weekly tests)
- Athlete wellness check-ins (daily short-form)
- Talent ID combine scores (pre-signing assessment)
- Automated communication to coaches, support staff, and parents

All data in this repo is synthetic and generated for teaching. There are no real athletes here.

## What the students are building towards

A Telegram-fronted Claude Code workflow where:

1. The sport scientist uploads an end-of-session GPS export to their Telegram bot.
2. The bot validates the file, cleans it, rolls it up, flags high-risk spikes.
3. The bot triggers a skill that renders a standardised PDF report using Typst.
4. The bot returns the PDF and a short written summary to the relevant audience (head coach, S&C lead, or academy director) with appropriate tone.

## Conventions

- **Units:** distances in metres, speeds in m/s, loads in arbitrary units (AU) from the vendor.
- **Dates:** ISO 8601 (`YYYY-MM-DD`).
- **Player IDs:** `NF###` where `###` is a zero-padded number. No real names in data.
- **Reports:** generated with Typst using templates under `skills/*/template.typ`.
- **Language:** British English (organisation, colour, analyse).

## How to help students

Students in this workshop are new to Claude Code. When they ask you to do something:

- Explain *what* you are about to do before you do it.
- Prefer smaller, reviewable steps over one large change.
- Show them the command or the diff, never just assert that you "did it".
- If they ask for something that would commit a secret (like a Telegram bot token) to git, refuse and explain why.

## Safety

- Never write a real bot token, API key, or personal data to a tracked file.
- `.env` is gitignored; all secrets live there.
- Synthetic data only. If a student pastes what looks like real athlete data, stop and ask them to confirm it is synthetic or anonymised.
