#!/usr/bin/env python3
"""
Claude Code Skill → Model-Agnostic SKILL.md Converter

Converts CLAUDE.md / Claude-specific skill files into generic SKILL.md
that works with any LLM backend (DeepSeek, GPT, Claude, Qwen, etc.)

Usage:
    python claude-to-skills.py <path-to-skill-dir>
    python claude-to-skills.py --batch <path-to-skills-root>

Rules applied:
    1. Strip Claude-specific syntax (@mentions, claude_ prefixed tools)
    2. Replace CLAUDE.md → SKILL.md
    3. Genericize tool use instructions
    4. Remove model-specific assumptions (Anthropic-only features)
    5. Add model-agnostic compatibility metadata
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime

# Mapping rules for Claude-specific → generic
CLAUDE_TO_GENERIC = {
    # Tool names
    r'\bclaude_code\b': 'coding_agent',
    r'\bclaude\s+computer\s+use\b': 'browser_automation',
    r'\bAnthropic\b': 'Any LLM provider',
    r'\bClaude\s+3.5\b': 'LLM',
    r'\bClaude\s+3\b': 'LLM',
    r'\bClaude\b(?! Code)': 'The agent',
    r'\bCLAUDE\.md\b': 'SKILL.md',

    # Model-specific instructions
    r'Use the claude-specific format': 'Use your standard tool format',
    r'as claude would': 'following best practices',
    r'claude\[': 'agent[',
    r'anthropic/claude': 'your LLM provider',
    r'Claude Code agent': 'coding agent',

    # API references
    r'Anthropic API': 'LLM API',
    r'Claude API': 'LLM API',
    r'"claude-3-5-sonnet': '"your-model-here',

    # File patterns
    r'\.claude/': '.agent/',
    r'CLAUDE\.md': 'SKILL.md',
}

SKILL_TEMPLATE = """---
name: {name}
description: {description}
version: 1.0.0
author: Converted from Claude Code skill by model-agnostic-skills
original: {original_repo}
converted_at: {converted_at}
compatible_models: [deepseek, gpt-4o, gpt-4.5, claude-3.5-sonnet, claude-4, qwen-max, qwen-plus, gemini-2.5-pro]
compatible_frameworks: [openclaw, cursor, continue-dev, windsurf]
tags: [{tags}]
---

{body}
"""

def collect_skills_dir(skill_dir: Path) -> list[dict]:
    """Scan a skill directory for source files to convert."""
    skills = []
    
    for md_file in sorted(skill_dir.glob("**/*.md")):
        if md_file.name == "README.md":
            continue
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        if len(content.strip()) < 10:
            continue
        
        # Determine skill type from path
        rel = md_file.relative_to(skill_dir)
        parts = rel.parts
        
        skill_info = {
            "source": str(md_file),
            "name": parts[-2] if len(parts) > 1 else md_file.stem,
            "content": content,
            "original_repo": skill_dir.name,
        }
        skills.append(skill_info)
    
    return skills

def detect_skill_metadata(content: str, name: str) -> dict:
    """Extract metadata from skill content."""
    # Extract first heading as title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else name.replace("-", " ").title()
    
    # Extract description from first paragraph
    desc_match = re.search(r'^#\s+.+\n\n(.+?)(?:\n\n|\n#)', content, re.MULTILINE | re.DOTALL)
    desc = desc_match.group(1).strip().replace("\n", " ")[:200] if desc_match else f"Model-agnostic skill for {title.lower()}"
    
    # Detect tags from content
    tags = []
    tag_patterns = {
        "coding": r'\b(code|coding|programming|development|debug|refactor)\b',
        "agent": r'\b(agent|autonomous|loop|task)\b',
        "design": r'\b(design|ui|ux|html|css|layout)\b',
        "testing": r'\b(test|testing|qa|verify)\b',
        "docs": r'\b(docs|documentation|readme|write)\b',
        "review": r'\b(review|pr|pull.request|inspect)\b',
        "planning": r'\b(plan|architecture|design.pattern|structure)\b',
    }
    for tag, pattern in tag_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            tags.append(tag)
    
    if not tags:
        tags = ["tool"]
    
    return {"title": title, "description": desc, "tags": tags}

def convert_skill(content: str) -> str:
    """Apply conversion rules to strip Claude-specific patterns."""
    result = content
    
    # Apply regex replacements
    for pattern, replacement in CLAUDE_TO_GENERIC.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # Remove Claude-specific blocks
    lines = result.split("\n")
    cleaned = []
    skip_block = False
    
    for line in lines:
        # Skip Claude-only service references
        if re.search(r'(use\s+the\s+anthropic|claude\s+only|requires\s+claude)', line, re.IGNORECASE):
            continue
        # Skip API key references to Anthropic
        if re.search(r'(ANTHROPIC_API_KEY|set.*anthropic)', line, re.IGNORECASE):
            continue
        
        # Add model-agnostic notes where appropriate
        if re.search(r'(AI|LLM|model)\s+(should|must|can|will)\s+(generate|create|write)', line, re.IGNORECASE):
            line += " (Any capable LLM)"
        
        cleaned.append(line)
    
    result = "\n".join(cleaned)
    
    # Add model-agnostic compatibility note at top
    compat_note = "\n\n> **Model-Agnostic**: This skill has been converted from Claude Code. It works with any LLM — DeepSeek, GPT-4o, Claude, Qwen, Gemini.\n"
    if compat_note not in result:
        # Insert after first heading
        first_heading = re.search(r'^#\s+.+\n', result, re.MULTILINE)
        if first_heading:
            pos = first_heading.end()
            result = result[:pos] + compat_note + result[pos:]
    
    return result

def convert_skill_dir(skill_dir: str, output_dir: str):
    """Convert all skills in a directory."""
    skill_path = Path(skill_dir)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    skills = collect_skills_dir(skill_path)
    converted = []
    
    for skill in skills:
        meta = detect_skill_metadata(skill["content"], skill["name"])
        body = convert_skill(skill["content"])
        
        # Build SKILL.md
        skill_content = SKILL_TEMPLATE.format(
            name=skill["name"],
            description=meta["description"],
            original_repo=skill["original_repo"],
            converted_at=datetime.now().strftime("%Y-%m-%d"),
            tags=", ".join(meta["tags"]),
            body=body,
        )
        
        # Write output
        skill_out_dir = out_path / skill["name"]
        skill_out_dir.mkdir(parents=True, exist_ok=True)
        (skill_out_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
        
        converted.append({
            "name": skill["name"],
            "title": meta["title"],
            "tags": meta["tags"],
        })
    
    return converted

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    target = Path(sys.argv[1])
    batch = "--batch" in sys.argv
    output = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else "output_skills"
    
    if not target.exists():
        print(f"Error: {target} not found")
        sys.exit(1)
    
    if batch:
        # Batch mode: scan multiple skill directories
        all_converted = []
        for skill_dir in sorted(target.iterdir()):
            if not skill_dir.is_dir():
                continue
            if any((skill_dir / f).exists() for f in ["SKILL.md", "CLAUDE.md"]):
                name = skill_dir.name
                out = os.path.join(output, name)
                result = convert_skill_dir(str(skill_dir), out)
                all_converted.extend(result)
                print(f"✅ {name}: converted ({len(result)} files)")
        
        print(f"\n🎉 Total: {len(all_converted)} skills converted to {output}/")
    else:
        # Single dir mode
        result = convert_skill_dir(str(target), output)
        for r in result:
            print(f"✅ {r['name']}: {r['title']} [{', '.join(r['tags'])}]")
        print(f"\n🎉 {len(result)} skills converted to {output}/")

if __name__ == "__main__":
    main()
