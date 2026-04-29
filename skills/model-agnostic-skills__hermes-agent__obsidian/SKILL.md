---
name: hermes-agent__obsidian
description: Obsidian Vault
version: 1.0.0
author: Converted from Claude Code skill by model-agnostic-skills
original_repo: unknown
converted_at: 2026-04-29
compatible_models: [deepseek, gpt-4o, gpt-4.5, claude-3.5-sonnet, claude-4, qwen-max, qwen-plus, gemini-2.5-pro]
compatible_frameworks: [openclaw, cursor, continue-dev, windsurf]
tags: [coding, review]
---

> **Model-Agnostic**: This skill has been converted from Claude Code. It works with any LLM backend.
---
name: obsidian
description: Obsidian Vault
version: 1.0.0
author: Converted from Your coding agent skill by model-agnostic-skills
original_repo: unknown
converted_at: 2026-04-29
compatible_models: [deepseek, gpt-4o, gpt-4.5, claude-3.5-sonnet, claude-4, qwen-max, qwen-plus, gemini-2.5-pro]
compatible_frameworks: [openclaw, cursor, continue-dev, windsurf]
tags: [tool]
---

> **Model-Agnostic**: This skill has been converted from Your coding agent. It works with any LLM backend.
---
name: obsidian
description: Read, search, and create notes in the Obsidian vault.
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/Documents/Obsidian Vault`.

Note: Vault paths may contain spaces - always quote them.

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# All notes
find "$VAULT" -name "*.md" -type f

# In a specific folder
ls "$VAULT/Subfolder/"
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# By filename
find "$VAULT" -name "*.md" -iname "*keyword*"

# By content
grep -rli "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
echo "
New content here." >> "$VAULT/Existing Note.md"
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.


