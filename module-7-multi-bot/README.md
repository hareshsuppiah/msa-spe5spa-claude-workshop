# Module 7: Multi-bot ecosystem (extension)

**Time: 15 minutes · optional, post-class**

## Why another bot?

Your load-bot from Module 6 answers to you and Pat. That is the right audience for the raw training-load report. But a real high-performance team has other audiences with very different needs:

| Audience | What they want | How often |
|----------|----------------|-----------|
| Head coach | One-page PDF, traffic-light flags | weekly |
| S&C lead | Detailed player-level session data, thresholds, prescription suggestions | every session |
| Academy director / board | Squad-level trend narrative, monthly KPIs, no tactics | monthly |
| Parents of U16s | Short text update on their child's wellness and involvement | fortnightly |

If you put all four audiences into one bot, the bot ends up muddled and every message needs a "who are you?" clarification. The professional pattern is **one bot per audience**, each with its own persona, scope, and skillset.

This module adds a second bot - the **coach-comms bot** - that takes the same underlying data and produces a short tactical narrative for the head coach, phrased for a human who has ten seconds to read it on the sideline.

## Architecture

```
                          [ shared data/ folder ]
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
    load-bot/CLAUDE.md      comms-bot/CLAUDE.md        (future bots...)
          │                         │
    weekly-load-report        coach-brief skill
    skill (PDFs)              (short text + emoji)
          │                         │
    Telegram: Pat             Telegram: Head coach
    & S&C staff               + Assistant coach
```

Both bots share the same project folder and the same data. They differ in **who they answer to** and **which skills they invoke**.

## Step 1: register a second bot with BotFather

Same as Module 6. Use `/newbot` again. Name it something like `Northfield Coach Brief Bot`, username `northfield_coach_NF123_bot`. Save the token.

## Step 2: add it to `.env`

Open `.env` and add a second line:

```
TELEGRAM_BOT_TOKEN=... (your load-bot token from Module 6)
TELEGRAM_COMMS_TOKEN=... (your new coach-brief token)
```

## Step 3: wire the comms-bot

Each bot gets its own sub-folder with its own `CLAUDE.md`:

```
module-7-multi-bot/
├── load-bot/CLAUDE.md    (already written - read this for reference)
└── comms-bot/CLAUDE.md   (already written)
```

Open both and compare. Notice how they differ:

- **load-bot** is technical: talks to S&C staff, uses jargon, defaults to full PDFs.
- **comms-bot** is brief: talks to the head coach, uses short sentences, avoids raw numbers where a traffic-light would do, uses (sparingly) emoji because the coach reads on his phone between sessions.

This is the key pattern. **Context shapes behaviour.** Same model, same data, different CLAUDE.md → different personality.

## Step 4: configure the second plugin instance

```
claude telegram:configure --profile comms --token-env TELEGRAM_COMMS_TOKEN
```

This registers the second bot under a profile named `comms`. The load-bot runs under the default profile.

## Step 5: allowlist the coach

On your phone, from a test account representing the head coach (or ask a classmate to help), send `/start` to the new bot. Then:

```
claude telegram:access --profile comms
```

Approve.

## Step 6: build the `coach-brief` skill

The skill is already scaffolded at `skills/coach-brief/SKILL.md`. Read it. It expects the same cleaned GPS data but produces a totally different output: a 3-sentence message, no PDF, no tables. Just "squad did X, Y was high, Z to watch on Friday".

Start Claude Code and ask:

```
Produce the coach brief for this week using the coach-brief skill.
```

Verify the output in the terminal. If it is too long, iterate - brevity is the whole point.

## Step 7: start both bots

In one terminal:

```
claude
> Start the load-bot listening on Telegram.
```

In a second terminal tab (`+` in VS Code's terminal panel):

```
claude --profile comms
> Start the comms-bot listening on Telegram.
```

Now send `weekly report` to the load-bot. You get a PDF. Send the same thing to the comms-bot. You get a three-sentence brief. Same data, two outputs, two audiences. No context-switching effort from you.

## What this unlocks

Once you have this pattern, the list of bots is bounded only by how many audiences your team has. Realistic production set for a professional club:

- **Load-bot** (S&C staff) - weekly load PDFs, per-session flags
- **Comms-bot** (head coach + assistants) - 3-line briefs
- **Board-bot** (academy director) - monthly KPI one-pager
- **Parent-bot** (parents, opt-in) - fortnightly wellness and involvement note
- **Scouting-bot** (recruitment staff) - talent-ID combine data on demand

Each one is a folder with a CLAUDE.md, optional skills, and a Telegram profile. Adding a new one is 30 minutes of work, not a week.

## The budget conversation

If you are reading this and thinking "I want to take this to my club", here is the rough cost model to put in front of a director of performance:

- **Infrastructure (VPS):** £10/month
- **Claude subscription:** Claude Max at ~£80-150/month per analyst seat, or Claude for Enterprise for team-level access. Budget one seat for the analyst who owns the bots.
- **Telegram:** free
- **Typst:** free

Versus the analyst time you save:

- Weekly load report: ~1 hour × 40 training weeks = 40 hours/year
- Coach brief: ~30 min × 40 = 20 hours/year
- Board report: ~2 hours × 12 = 24 hours/year
- Parent updates: ~1 hour × 20 = 20 hours/year

That is roughly **100 hours/year saved per analyst**, for a few hundred pounds of subscriptions. The ROI conversation is short.

The real win is not the time. It is that the report gets written **every single week**, even the weeks when the analyst is at a tournament, sick, or on leave. Institutional reliability is the thing the subscription buys.

## Done

You built two bots. You could now build twenty. The end.

Return to `README.md` at the repo root for recap.
