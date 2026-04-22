# Module 4 context

This module asks Claude to help a student build a deterministic GPS cleaning tool.

## Rules for this module

- Use Python with pandas. Do not switch to R or another language unless the student asks.
- Keep the script readable: a `main()` function and small helpers, not one giant block.
- The student is learning to **review** code as much as to write it. Prefer shorter, clearer scripts over clever one-liners.
- Never silently drop rows. Every dropped row must be logged to the summary.
- The cleaning rules are agreed with the student in the chat - do not invent new rules mid-script. If you think a rule is missing, ask.

## Do not do

- Do not auto-generate unit tests unless explicitly asked.
- Do not write a full CLI framework (argparse etc.) unless asked - a simple script with hard-coded paths is fine for this exercise.
- Do not push changes to Git; the student commits manually.

## Teaching moments to lean into

- If the student asks you to just "fix it", prompt them back with "what counts as fixed?". This is the skill they are here to learn.
