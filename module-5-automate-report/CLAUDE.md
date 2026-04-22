# Module 5 context

This module teaches skills and Typst. The skill `weekly-load-report` is already written; the student's job is to run it, read the output, and understand the pattern.

## Rules for this module

- When the student asks for the weekly report, invoke the `weekly-load-report` skill rather than writing a bespoke script.
- If the cleaned CSV does not exist, run the cleaning tool from Module 4 first (or clean inline with the same rules).
- Always write the PDF to the module folder unless the student specifies otherwise.
- After compiling the PDF, print a short terminal summary with:
  - total players included
  - how many are flagged amber/red for load change
  - file path of the PDF

## Do not do

- Do not modify the Typst template in the skill folder unless the student explicitly asks. That template is the "brand" - changing it silently will confuse the coach.
- Do not suggest alternative tools (Quarto, R Markdown, LaTeX). Typst is the chosen standard.
