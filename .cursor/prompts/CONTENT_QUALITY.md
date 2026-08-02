# Content quality — agent index

Use these files whenever generating or improving tutorials, labs, interviews, quizzes, or cheatsheets.

| Priority | File | Purpose |
|----------|------|---------|
| 1 | `.cursor/rules/00-foundation/09-content-quality-standard.mdc` | Always-on quality bar (labs, interview, anti-patterns) |
| 2 | `.cursor/prompts/tutorial-format-linux.md` | Canonical tutorial body for **all** technologies |
| 3 | `.cursor/prompts/tutorials/create_tutorial.md` | End-to-end tutorial generation prompt |
| 4 | `.cursor/prompts/tutorials/create_lab.md` | Standalone + in-tutorial lab design |
| 5 | `.cursor/prompts/tutorials/create_interview_questions.md` | Interview guides and in-page Qs |
| 6 | `.cursor/prompts/tutorials/improve_tutorial.md` | Raise an existing page to the bar |
| 7 | `.cursor/prompts/tutorials/review_tutorial.md` | Pass/fail review checklist |
| 8 | `AGENTS.md` | Repo entry point + scripts |

## Agent preference

Prefer **Codex** for content generation until the user explicitly changes the agent.

## Competitor quality bar (do not copy content)

Match the *standard* of:

- GeeksforGeeks — clear definitions, examples, progressive depth  
- Microsoft Learn / AWS Skill Builder — outcome-driven modules, validation  
- Linux Foundation — production-flavoured labs  

Do **not** plagiarise. Write original REBASH content in British English.

## Quick lab test

Before marking a lab done, mentally paste Task 1’s commands into a clean shell on the documented OS. If a step needs “figure it out” for a required flag, rewrite the lab.
