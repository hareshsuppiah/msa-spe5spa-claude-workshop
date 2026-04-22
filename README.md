# MSA Claude Code Workshop

**Master of Sport Analytics, La Trobe University**
**Subject:** SPE5SPA - Sports Project A
**Session:** Week 8, Wednesday AM (29 April 2026)

Welcome. Over the next ninety minutes (and a bit more in your own time) you will go from "I have never touched a terminal" to "I have my own Telegram bot that reads a GPS export, runs quality checks, and produces a standardised PDF training-load report for my coach."

You are building something that real performance analysts in soccer academies, academy systems, and high-performance units use every week. We are using synthetic data and a toy scenario, but the shape of the workflow is real.

## The scenario you are building for

You work as a performance analyst at **Northfield FC**, a fictional academy-level soccer club.

- Your sport scientist, Pat, runs on-field GPS units during every training session. After the session, Pat exports a CSV from the GPS vendor's software.
- That CSV lands in your hands. Some fields are messy. Some sessions have dropped units. You need to sanity-check it, roll it up into weekly totals per player, flag anyone whose load is spiking, and send a one-page report to the head coach before the next morning.
- Today, Pat does this by sending you the file in WhatsApp at 9pm. You do it by hand and email a spreadsheet back at 11pm.
- By the end of this workshop, Pat sends the file to **your** Telegram bot. The bot cleans it, scores it, flags the risky spikes, renders a PDF, and sends it back to the coach - in the time it took you to read this paragraph.

Every module in this workshop exists to build one piece of that pipeline.

## What you need before the session

- A **GitHub account** (free - github.com/signup)
- A **Claude account with paid access**: either a Claude Pro or Max subscription, or Claude Console API credits. The free tier will not carry you through Modules 4-7.
- A phone with **Telegram** installed (Modules 6 and 7). Any recent iPhone/Android works.

A full student-facing prep guide is in the LMS announcement you received three days before class. If you did not see it, flag on Teams.

## Modules

| # | Module | What you learn | Time |
|---|--------|----------------|------|
| 1 | Terminal basics | Move around, peek at files, use Git | 10 min |
| 2 | Your first Claude Code conversation | What Claude Code is, how it differs from the chat interface, what "tools" and "agents" mean | 15 min |
| 3 | CLAUDE.md and giving context | How to tell Claude about your project so it stops guessing | 10 min |
| 4 | Build a data cleaning tool | Work with Claude to clean messy GPS data | 20 min |
| 5 | Automate the weekly report | Introduce **Skills**; build a Typst-powered training-load PDF | 20 min |
| 6 | Your own Telegram bot | Wire the skill to a bot Pat can message | 20 min |
| 7 | Multi-bot ecosystem (extension) | Add a second bot for coach/board comms | 15 min |

Modules 1-5 run live during the 90-minute session. Modules 6-7 are walked through at the end; you will usually complete them either at the end of the session or in the following week.

## How to start

1. Click the green **Code** button at the top of this repo.
2. Select the **Codespaces** tab.
3. Click **Create codespace on main**.
4. Wait roughly 90 seconds. A VS Code editor opens in your browser, and a terminal pane appears at the bottom. You will see "Installing Python libraries", "Installing Typst", "Installing Claude Code CLI" scroll past. This only happens the first time.
5. When you see a `$` prompt, you are ready. Open `module-1-terminal/README.md` in the editor and start reading.

## Folder structure

```
msa-spe5spa-claude-workshop/
├── .devcontainer/         # Codespace build config
├── CLAUDE.md              # Shared project instructions Claude reads first
├── data/                  # Synthetic scenario datasets
├── skills/                # Reusable skills Claude can invoke (Module 5+)
├── module-1-terminal/
├── module-2-first-chat/
├── module-3-claude-md/
├── module-4-build-a-tool/
├── module-5-automate-report/
├── module-6-telegram-bot/
└── module-7-multi-bot/
```

Each module folder has a `README.md` with the walkthrough, plus a local `CLAUDE.md` from Module 3 onwards that teaches context layering.

## About the infrastructure choice

We are using **GitHub Codespaces** for this workshop. This is not the production setup you would run in a club. In a real high-performance team you would host your Claude Code + bot on a **cheap VPS** (DigitalOcean, Hetzner, a spare Mac mini on the club's network) so the bot stays running overnight when Codespaces would have paused.

Codespaces is the teaching-friendly shortcut. The workflow you learn here transfers exactly - the VPS setup is the same commands run on a different box.

## About Claude plans

Some features in this workshop - particularly running agents for longer tasks in Modules 4-7 - will hit the limits of the free Claude plan. You need **at least Claude Pro** to get through the full session comfortably. In a professional setting, your club would pay for a **Claude Max** or **Claude for Enterprise** subscription; the cost (roughly a fraction of one staff salary) is repaid in hours of analyst time per week.

We will come back to this at the end of Module 7 with concrete numbers you can take to a director of performance.

---

Ready? Open `module-1-terminal/README.md`.
