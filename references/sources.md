# Sources to re-check when updating this skill

Last checked: 2026-07-24 for `pmcp 2.17.0`, `cargo-pmcp 0.20.0`, and Rust 1.91.

Primary:

- PMCP landing/docs: https://paiml.github.io/rust-mcp-sdk/
- PMCP crate docs: https://docs.rs/pmcp
- PMCP crate: https://crates.io/crates/pmcp
- PAIML rust-mcp-sdk repository: https://github.com/paiml/rust-mcp-sdk
- cargo-pmcp README: https://github.com/paiml/rust-mcp-sdk/blob/main/cargo-pmcp/README.md
- PMCP examples README: https://github.com/paiml/rust-mcp-sdk/blob/main/examples/README.md
- PMCP changelog: https://github.com/paiml/rust-mcp-sdk/blob/main/CHANGELOG.md
- PMCP 2.17.0 tag: https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.17.0
- PMCP 2.17.0 Cargo page: https://crates.io/crates/pmcp/2.17.0
- PMCP 2.17.0 published manifest: https://docs.rs/crate/pmcp/2.17.0/source/Cargo.toml
- cargo-pmcp 0.20.0 release: https://github.com/paiml/rust-mcp-sdk/releases/tag/v0.20.0
- cargo-pmcp 0.20.0 Cargo page: https://crates.io/crates/cargo-pmcp/0.20.0
- cargo-pmcp 0.20.0 changelog: https://github.com/paiml/rust-mcp-sdk/blob/v0.20.0/cargo-pmcp/CHANGELOG.md
- cargo-pmcp 0.20.0 renderer gate: https://github.com/paiml/rust-mcp-sdk/blob/v0.20.0/docs/runbooks/cfn-renderer-switch-gate.md

Skill format:

- Codex skills: https://developers.openai.com/codex/skills
- OpenAI API skills: https://developers.openai.com/api/docs/guides/tools-skills
- OpenCode skills: https://opencode.ai/docs/skills/

Update process:

1. Inspect the repository's `Cargo.toml`, `Cargo.lock`, Rust MSRV, and enabled PMCP features before treating this baseline as applicable.
2. Check the exact release tag, changelog, Cargo page, and published manifest for version, `rust-version`, feature names, macro syntax, and examples.
3. Check `cargo-pmcp` command names in the approved local toolchain.
4. Update `version-matrix.md`, production/testing/migration references, and templates together. Preserve older versions as historical guidance.
5. Run `scripts/validate_skill.py`, `python -m unittest scripts/test_validate_skill.py -v`, link checks, and the available compile check.
