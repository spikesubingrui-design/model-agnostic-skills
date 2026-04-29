---
name: hermes-agent__plan
description: Plan Mode
version: 1.0.0
author: Converted from Claude Code skill by model-agnostic-skills
original_repo: unknown
converted_at: 2026-04-29
compatible_models: [deepseek, gpt-4o, gpt-4.5, claude-3.5-sonnet, claude-4, qwen-max, qwen-plus, gemini-2.5-pro]
compatible_frameworks: [openclaw, cursor, continue-dev, windsurf]
tags: [coding, agent, design, testing, review, planning]
---

> **Model-Agnostic**: This skill has been converted from Claude Code. It works with any LLM backend.
---
name: plan
description: Plan Mode
version: 1.0.0
author: Converted from Your coding agent skill by model-agnostic-skills
original_repo: unknown
converted_at: 2026-04-29
compatible_models: [deepseek, gpt-4o, gpt-4.5, claude-3.5-sonnet, claude-4, qwen-max, qwen-plus, gemini-2.5-pro]
compatible_frameworks: [openclaw, cursor, continue-dev, windsurf]
tags: [coding, agent, design, testing, review, planning]
---

> **Model-Agnostic**: This skill has been converted from Your coding agent. It works with any LLM backend.
---
name: plan
description: "Plan mode: write markdown plan to .hermes/plans/, no exec."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow]
    related_skills: [writing-plans, subagent-driven-development]
---

# Plan Mode

Use this skill when the user wants a plan instead of execution.

## Core behavior

For this turn, you are planning only.

- Do not implement code.
- Do not edit project files except the plan markdown file.
- Do not run mutating terminal commands, commit, push, or perform external actions.
- You may inspect the repo or other context with read-only commands/tools when needed.
- Your deliverable is a markdown plan saved inside the active workspace under `.hermes/plans/`.

## Output requirements

Write a markdown plan that is concrete and actionable.

Include, when relevant:
- Goal
- Current context / assumptions
- Proposed approach
- Step-by-step plan
- Files likely to change
- Tests / validation
- Risks, tradeoffs, and open questions

If the task is code-related, include exact file paths, likely test targets, and verification steps.

## Save location

Save the plan with `write_file` under:
- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

Treat that as relative to the active working directory / backend workspace. Hermes file tools are backend-aware, so using this relative path keeps the plan with the workspace on local, docker, ssh, modal, and daytona backends.

If the runtime provides a specific target path, use that exact path.
If not, create a sensible timestamped filename yourself under `.hermes/plans/`.

## Interaction style

- If the request is clear enough, write the plan directly.
- If no explicit instruction accompanies `/plan`, infer the task from the current conversation context.
- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
- After saving the plan, reply briefly with what you planned and the saved path.


