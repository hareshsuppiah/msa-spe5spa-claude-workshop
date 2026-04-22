# Module 1: Terminal basics

**Time: 10 minutes**

## Why this module exists

Everything you will do in this workshop - and in a lot of modern sport-analytics work - happens at a **terminal**. It is the prompt you type commands into. It feels intimidating for about ten minutes and then it becomes the most efficient tool you own.

There is a second reason for starting here: **Claude Code lives in the terminal**. You cannot run Claude Code from a graphical menu; you type `claude` and it launches inside the terminal. If you are not comfortable with `cd` and `ls`, you will not be comfortable with Claude Code.

This module is the ten-minute vaccine.

## 1. Find your terminal

In your Codespace, look at the bottom of the VS Code window. You should see a panel labelled **TERMINAL**. If you cannot see it, press **Ctrl + `** (the backtick, top-left of your keyboard).

You should see a prompt that looks something like:

```
vscode ➜ /workspaces/msa-spe5spa-claude-workshop $
```

That is the shell. The `$` is where your typing appears.

## 2. Where am I?

Type:

```
pwd
```

`pwd` = **print working directory**. The terminal always has a "current location" in the filesystem. Every command you type runs from that location. Think of it as which folder a file explorer has open.

You should see `/workspaces/msa-spe5spa-claude-workshop`.

## 3. What is in this folder?

```
ls
```

`ls` = **list**. You will see the module folders, the `data/` folder, and the README. Want more detail?

```
ls -la
```

The `-la` adds "long format" and "all files including hidden ones". You will now see `.devcontainer`, `.gitignore`, `CLAUDE.md`. Files starting with `.` are hidden by default.

## 4. Move around

```
cd data
ls
```

`cd` = **change directory**. You are now in `data/`, and `ls` shows the CSV files. To go back up one level:

```
cd ..
```

Two dots means "parent". One dot means "here". To jump back to the repo root from anywhere:

```
cd /workspaces/msa-spe5spa-claude-workshop
```

## 5. Peek at a file

```
head data/squad_roster.csv
```

`head` shows the first ten lines of a file. Add `-20` to see twenty:

```
head -20 data/gps_training_messy.csv
```

## 6. Count things

```
wc -l data/gps_training_messy.csv
```

`wc -l` = **word-count, count lines**. Useful when someone sends you a CSV and says "I'm not sure how many sessions are in there".

## 7. Search

```
grep "NF015" data/gps_training_messy.csv
```

`grep` pulls every line that contains the text you give it. This is how analysts find one player's rows out of thousands.

## 8. Git - your safety net

This repo is a Git repository. Git tracks every change you make, and lets you undo anything. You do not need to become a Git expert today, but you should know one command:

```
git status
```

This tells you what files you have changed since the last saved version. If you ever break something and want to start fresh, Claude Code can help you recover using `git restore`.

## Cheat sheet

| Command | What it does |
|---------|--------------|
| `pwd` | Where am I? |
| `ls` / `ls -la` | List files (hidden too) |
| `cd folder` | Move into a folder |
| `cd ..` | Move up one folder |
| `head file` | First ten lines |
| `cat file` | Whole file |
| `wc -l file` | Count lines |
| `grep "text" file` | Search for text |
| `git status` | What have I changed? |
| `clear` | Wipe the terminal screen |

## Done

You can move around, peek at files, and search. That is enough.

```
cd /workspaces/msa-spe5spa-claude-workshop/module-2-first-chat
cat README.md
```

Or just open `module-2-first-chat/README.md` in the editor sidebar.
