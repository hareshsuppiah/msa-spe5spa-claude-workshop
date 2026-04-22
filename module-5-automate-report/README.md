# Module 5: Automate the weekly report with Skills + Typst

**Time: 20 minutes**

## Why this module exists

In Module 4 you built a cleaning tool. In a real week, Pat sends the GPS file, you clean it, then you manually open Excel, make a pivot table, paste three charts, write three sentences for the coach, save a PDF, and email it. That is an hour a week. Fifty hours a year.

This module replaces that hour with two things:

1. A **skill** - a reusable instruction packet Claude can invoke any time it needs to generate a training-load report.
2. A **Typst template** - a standardised, branded one-page PDF layout that the skill fills in.

Together they mean "write the weekly report" becomes one sentence to Claude and you get a PDF back.

## What is a skill?

A skill is a folder containing a `SKILL.md` file (plus any supporting files like templates, reference data, or helper scripts). Claude Code sees every skill in your project on startup. When you ask it to do something that matches a skill's description, Claude invokes the skill - which just means "follow the instructions in the SKILL.md".

Think of a skill as **a recipe with shared kitchen equipment**. The recipe is the markdown. The equipment is the Typst template, helper scripts, example outputs. Anyone on your team can trigger the same recipe by asking Claude the same kind of question, and they get the same kind of result.

Skills live in `skills/<skill-name>/` at the project root. Open the repo's `skills/` folder - you will see `weekly-load-report/` is already there.

## What is Typst?

Typst is a modern typesetting system - think LaTeX but with sensible syntax. You write a `.typ` file describing what the document should look like, feed it data, and `typst compile` produces a PDF. It is already installed in your Codespace.

We use Typst (not Word, not Quarto) for three reasons:

- **Standardised output:** the report looks the same every week, regardless of who runs it.
- **Deterministic:** the same data in, the same PDF out. Auditable.
- **Scriptable:** an agent can render one without opening a GUI.

## Open the skill

```
cat /workspaces/msa-claude-code-workshop/skills/weekly-load-report/SKILL.md
```

Read it. It has three parts:

1. **Frontmatter** (YAML at the top): a `name` and `description`. Claude reads the description to decide when the skill applies. If the description says "produces a one-page training-load PDF report for the head coach", Claude will trigger this skill the moment someone asks for a load report.

2. **Instructions**: step-by-step prose telling Claude what data to load, what to aggregate, what thresholds count as a red flag, how to fill the Typst template, where to save the output.

3. **Artifacts**: the `template.typ` and any helper scripts. Relative paths inside the skill folder.

## Run the skill

Start Claude Code from the repo root (skills are always resolved from project root):

```
cd /workspaces/msa-claude-code-workshop
claude
```

Then ask:

```
Please produce the weekly training-load report for this week. Save the PDF to module-5-automate-report/weekly_report_2026-04-22.pdf.
```

Watch the transcript. You will see Claude:

- Recognise that the `weekly-load-report` skill matches your request.
- Read the SKILL.md.
- Run the cleaning tool (or use an already-clean file if you pass one).
- Aggregate per-player totals for the week.
- Compare to the previous week's totals from `data/gps_training_week_prior.csv`.
- Identify any player whose weekly distance is up or down by more than the threshold set in the skill.
- Fill in the Typst template and compile it.
- Print a short text summary to the terminal.

Open the PDF. You should see a Northfield FC-branded page with a summary paragraph, a table of players with weekly totals and change-from-last-week, and a few players highlighted amber/red for load spikes.

## Why this is such a big deal

You just reduced "write the weekly report" to one sentence. The skill has:

- The output format locked in (coach gets the same layout every week)
- The thresholds locked in (no more "did I use 15% or 20% this week?")
- The file path conventions locked in (future-you, 6 months from now, can always find the report)

And the **skill is in Git**. When the S&C lead joins next season, she clones the repo, runs the same command, and gets the same report. Your institutional knowledge is no longer trapped in your head.

## Customise the skill (stretch)

Open `skills/weekly-load-report/SKILL.md` in the editor. Try changing one thing:

- Swap the red-flag threshold from ±20% to ±15%.
- Add a second section to the PDF showing the team-average wellness score from `data/athlete_wellness.csv`.
- Change the report heading colour from navy to the Northfield FC primary (say, forest green).

Re-run the skill. Verify the PDF updates accordingly.

This is the pattern: **the skill is a text file, edited by humans, read by Claude, producing a deterministic output.** You version-control it; you review changes to it; your team trusts it.

## Done

You have gone from "Pat sends me a file" to "the system sends a PDF". The only thing left is removing the last manual step - you opening the file and typing into Claude.

That is Module 6.

```
cd /workspaces/msa-claude-code-workshop/module-6-telegram-bot
```
