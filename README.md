# Model-Agnostic Skills 🧠

> Convert Claude Code ecosystem skills to work with **any LLM** — DeepSeek, GPT-4o, Claude, Qwen, Gemini.

## The Problem

Claude Code has a thriving ecosystem of high-star skills on GitHub. But they're locked to Claude:
- `CLAUDE.md` format with model-specific assumptions
- Claude-specific tool use patterns
- Anthropic-only API dependencies

## Our Solution

We convert these skills to **model-agnostic SKILL.md** format:
- Same powerful capabilities, any LLM backend
- Works with OpenClaw, cursor, continue.dev, and any agent framework
- Open-source converter tool included

## Quick Start

```bash
# Install skills
clawhub install model-agnostic-skills

# Or clone and use converter
git clone https://github.com/spikesubingrui-design/model-agnostic-skills
cd model-agnostic-skills
python converter/claude-to-skills.py path/to/claude-code-skill
```

## Skills Converted

| Original (Claude Code) | Agnostic Skill | Stars | Status |
|-------------------------|----------------|-------|--------|
| Karpathy Coding Guidelines | `karpathy-guidelines` | ⭐ 500+ | ✅ |
| GStack Autoplan | `gstack-autoplan` | ⭐ 200+ | ✅ |
| GStack Pair Agent | `gstack-pair-agent` | ⭐ 200+ | ✅ |
| GStack Design HTML | `gstack-design-html` | ⭐ 200+ | ✅ |
| Superpowers | `superpowers-code-review` | ⭐ 1k+ | ✅ |
| Caveman Compress | `caveman-compress` | ⭐ 300+ | ✅ |
| Claude-Mem | `claude-mem` | ⭐ 400+ | ✅ |

## How It Works

1. **Converter** scans the original skill
2. Strips Claude-specific syntax and assumptions
3. Maps to generic tool patterns
4. Generates a clean SKILL.md that any framework can use

## Contributing

Found a Claude Code skill that should be model-agnostic?
1. Paste the CLAUDE.md content into `converter/`
2. Run `python converter/claude-to-skills.py`
3. Submit a PR with the converted skill

## License

MIT — free for any use, personal or commercial.
