# Module 6: Your own Telegram bot

**Time: 20 minutes**

## The scenario

So far the pipeline is:

1. Pat emails you the GPS file.
2. *You* download it.
3. *You* open Claude Code and ask for the report.
4. *You* send the PDF back.

The bot removes you from steps 2-4. Pat sends the file to a Telegram chat; the bot receives it, runs the cleaning tool and the skill, and replies with the PDF.

At the end of this module **you will have your own Telegram bot running in your Codespace**, with your own token, and only people you allow can talk to it.

## What is a Telegram bot?

A Telegram bot is just an account Telegram lets you register programmatically. It has a username (e.g. `@northfield_load_bot`) and a **token** - a long secret string that grants API access to post and receive messages as that bot. Anyone can create one. It is free.

The bot itself is just a program that:

1. Polls Telegram for new messages sent to it.
2. Reacts (sends replies, downloads attachments, runs actions).

In our case, the "program" is Claude Code with a small Telegram plugin that relays messages to and from Claude.

## Step 1: make a bot with @BotFather

On your phone, open Telegram and search for **@BotFather** (the real one, verified with a blue tick). Start a chat and send:

```
/newbot
```

BotFather will ask for:

- **A name** for the bot (e.g. `Northfield Load Bot`). This is what appears in chat headers.
- **A username** ending in `bot` (e.g. `northfield_load_NF123_bot`). Must be unique across all of Telegram - add your initials/numbers. Save the username; you will need it.

BotFather replies with a message containing a token like:

```
7891234567:AAH...long-random-string
```

**Treat this like a password.** Anyone who has it can impersonate your bot.

## Step 2: store the token safely

In your Codespace terminal, from the repo root:

```
echo 'TELEGRAM_BOT_TOKEN=7891234567:AAH...your-token-here...' > .env
```

Replace the right-hand side with your actual token. The `.env` file is already in `.gitignore` so it will not be committed.

Verify:

```
cat .env
```

You should see your token. Now check Git is ignoring it:

```
git status
```

`.env` should **not** appear. If it does, stop and tell the instructor.

## Step 3: install the plugin

In the terminal:

```
claude plugin install telegram
```

(If you get a prompt about permissions, accept.)

Then register your token with the plugin:

```
claude telegram:configure
```

Follow the prompts. Paste the token when asked. The plugin will ping Telegram's API to confirm the token is valid and the bot exists.

## Step 4: allowlist yourself

By default the bot ignores everyone. You need to tell it who is allowed to message it.

Open Telegram on your phone. Start a chat with your bot (search for its username, or tap the BotFather link). Send:

```
/start
```

Back in the Codespace terminal:

```
claude telegram:access
```

This shows a list of pending pairings. You should see your own Telegram user. Approve it. Now the bot will listen to you and ignore everyone else.

## Step 5: start the bot

```
claude
```

Then at the Claude Code prompt:

```
Start listening on Telegram. When I send you a GPS CSV, run the weekly-load-report skill on it and reply with the PDF and a short summary.
```

You should see Claude acknowledge, and a line like `telegram:listen polling started`.

## Step 6: test it from your phone

On your phone, in the chat with your bot:

- Send `hello`. The bot should reply with something sensible.
- Send the file `data/gps_training_messy.csv` as an attachment. (From Codespaces, right-click the file and "Download" to get it on your phone, or AirDrop/email yourself. In the real workflow Pat sends it from wherever he is.)

The bot should:

1. Acknowledge receipt.
2. Say what it is about to do ("cleaning, aggregating, compiling report").
3. Reply with a PDF and a short text summary.

Open the PDF on your phone. It should be the same standardised report you saw in Module 5.

## What to do when it breaks

It will break at some point. Typical issues:

- **Bot does not reply:** check the Codespace terminal. Is Claude Code still running? Has your Codespace paused (inactive > 30 min)? Restart it.
- **"Not allowed":** you did not complete the allowlist step. Run `claude telegram:access` again.
- **PDF is empty or missing rows:** you probably sent a file with a different column layout. Ask Claude to check the schema and tell you what is missing.

## What you learned

- A Telegram bot is a program that listens for messages and reacts.
- Tokens are secrets. They live in `.env`, never in Git.
- Claude Code + the Telegram plugin turns your skill into a phone-accessible service for your team.
- Because this is running in your Codespace, it stops when the Codespace pauses. In production you would run it on a VPS so it stays up overnight.

## Production notes (read this before you try it at work)

Running the bot in a Codespace is fine for learning. For an actual club:

- Use a **VPS** (DigitalOcean, Hetzner, an always-on Mac mini on the network). £5-10/month.
- Use a **paid Claude plan** - Pro minimum; Max or Enterprise if the bot is handling real volume.
- Put the bot in a **Docker container** with the plugin's allowlist baked in. Claude Code has a `claude docker` wrapper that makes this easy.
- Review the **Anthropic data policy** with your club's data officer before connecting to anything with real athlete data.
- Consider a **local LLM** via Ollama for the most sensitive workflows where data cannot leave the club's infrastructure. Slower but fully private.

## Done

You have a live Telegram bot. That is remarkable. Twenty minutes ago you had never started Claude Code.

Module 7 extends this with a second bot for coach-facing comms. It is optional and runs as post-class extension material.

```
cd /workspaces/msa-claude-code-workshop/module-7-multi-bot
```
