# Skill compatibility notes

This bundle is intentionally a skill, not a plugin.

## Required layout

```text
rust-pmcp-skill/
  SKILL.md
  references/
  scripts/
  templates/
```

`SKILL.md` contains only metadata and routing instructions; details live in references for progressive disclosure.

## Codex

Codex reads skills from `.agents/skills`, `$HOME/.agents/skills`, `/etc/codex/skills`, and managed/system locations. It loads `name`, `description`, and path first, then reads `SKILL.md` when invoked.

This skill includes optional `agents/openai.yaml` metadata. It does not declare MCP dependencies or install hooks.

## OpenCode

OpenCode discovers skills in `.opencode/skills`, `~/.config/opencode/skills`, and compatible `.agents/skills`/`.claude/skills` locations. The directory name must match the `name` in frontmatter.

## Portability rules used here

- Folder name: `rust-pmcp-skill`
- Frontmatter name: `rust-pmcp-skill`
- Lowercase + hyphen only.
- `description` is concise, trigger-rich, valid UTF-8, and contains 1 through 1024 Unicode characters.
- The body is navigational; references hold detailed guidance for progressive disclosure.
- The validator applies independent generous safety caps: raw file <= 256 KiB, frontmatter <= 16 KiB, and body <= 240 KiB. It does not impose a whole-file 1024-byte cap.
- No plugin manifest, app mapping, commands, install hooks, or hidden side effects.
