# rust-pmcp-skill

Portable Agent Skill for building and reviewing production Rust MCP servers using PAIML's `pmcp` crate and `cargo-pmcp` tooling.

## Contents

- `SKILL.md` — concise navigation entry point for Codex/OpenCode discovery.
- `references/` — on-demand guidance for PMCP server design, the PMCP 2.6-2.17 and cargo-pmcp 0.15-0.20 version matrix, cargo-pmcp workflow, testing/security/deployment, and rmcp-to-pmcp migration.
- `templates/snippets/` — small snippets for agents to adapt after checking the repository's locked SDK version.
- `scripts/validate_skill.py` — standard-library validation of structure, Unicode metadata, and independent safety caps.
- `scripts/test_validate_skill.py` — boundary tests for the validator contract.

## Install

Clone the repository so the skill folder remains named `rust-pmcp-skill`:

```bash
git clone https://github.com/sm18lr88/rust-pmcp-skill.git
```

### OpenAI Codex

Repo-scoped:

```bash
mkdir -p .agents/skills
cp -R rust-pmcp-skill .agents/skills/rust-pmcp-skill
```

User-scoped:

```bash
mkdir -p ~/.agents/skills
cp -R rust-pmcp-skill ~/.agents/skills/rust-pmcp-skill
```

### OpenCode

Repo-scoped:

```bash
mkdir -p .opencode/skills
cp -R rust-pmcp-skill .opencode/skills/rust-pmcp-skill
```

User-scoped:

```bash
mkdir -p ~/.config/opencode/skills
cp -R rust-pmcp-skill ~/.config/opencode/skills/rust-pmcp-skill
```

OpenCode also discovers `.agents/skills`, so the Codex repo/user install path works for both in most setups.

## Validate

```bash
python scripts/validate_skill.py .
python -m unittest scripts/test_validate_skill.py -v
```

## Notes for maintainers

- Keep `SKILL.md` concise and navigational; move detail into `references/` for progressive disclosure.
- The `description` is the only compact field: it must contain 1 through 1024 Unicode characters. There is no whole-file 1024-byte cap.
- Independent safety caps permit a raw `SKILL.md` up to 256 KiB, frontmatter up to 16 KiB, and body up to 240 KiB.
- Update `references/version-matrix.md` and `references/sources.md` whenever PMCP or cargo-pmcp releases a new major/minor version.
- This is a skill, not a plugin; it has no install hooks or runtime side effects.
