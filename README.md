# rust-pmcp-skill

A portable Agent Skill for building and reviewing production Rust MCP servers with PAIML's `pmcp` crate and `cargo-pmcp` tooling.

## Contents

- `SKILL.md` is a concise navigation entry point for Codex/OpenCode discovery.
- `references/` holds guidance that agents load on demand: PMCP server design, the PMCP 2.6-2.17 and cargo-pmcp 0.15-0.20 version matrix, the cargo-pmcp workflow, testing/security/deployment, and rmcp-to-pmcp migration.
- `templates/snippets/` holds small snippets for agents to adapt after they check the repository's locked SDK version.
- `scripts/validate_skill.py` validates structure, Unicode metadata, and independent safety caps, using only the standard library.
- `scripts/test_validate_skill.py` has boundary tests for the validator contract.

## Install

Clone the repository so the skill folder stays named `rust-pmcp-skill`:

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

OpenCode also discovers `.agents/skills`, so in most setups the Codex repo-scoped or user-scoped install path works for both.

## Validate

```bash
python scripts/validate_skill.py .
python -m unittest scripts/test_validate_skill.py -v
```

## Notes for maintainers

- Keep `SKILL.md` concise and navigational. Move detail into `references/` for progressive disclosure.
- The `description` is the only compact field: it must contain 1 through 1024 Unicode characters. There is no whole-file 1024-byte cap.
- Independent safety caps permit a raw `SKILL.md` up to 256 KiB, frontmatter up to 16 KiB, and a body up to 240 KiB.
- Update `references/version-matrix.md` and `references/sources.md` whenever PMCP or cargo-pmcp releases a new major or minor version.
- This is a skill, not a plugin. It has no install hooks or runtime side effects.
