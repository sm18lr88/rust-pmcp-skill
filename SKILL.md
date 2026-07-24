---
name: rust-pmcp-skill
description: Build and audit production Rust MCP servers with PAIML PMCP 2.17 and cargo-pmcp 0.20. Use for Rust MCP tools, prompts, resources, stdio or HTTP transports, schemas, testing, deployment, or migration from rmcp.
---
Use PAIML `pmcp`/`cargo-pmcp`, not `rmcp`, unless the repository requires `rmcp`.

## Workflow

1. Inspect `Cargo.toml`, `Cargo.lock`, source, MSRV, and the installed `pmcp` feature set before changing code. Honor an existing lock; otherwise use `pmcp = "=2.17.0"`, `cargo-pmcp` 0.20.0, and Rust 1.91.
2. Check current official PMCP docs and the exact locked API before writing snippets. Compile first, then add focused tests.
3. For local servers, protect stdio protocol stdout; diagnostics go to stderr. Validate through the official SDK/client and MCP Inspector, not ad-hoc pipes alone.
4. Use typed inputs and truthful outputs. Runtime paths do not use `unwrap` or `expect`; add cancellation/progress only for real long-running work.
5. Read only the needed reference:
   - `references/pmcp-production-guide.md` for API, schemas, transport, and safety
   - `references/cargo-pmcp-workflow.md` for scaffold and CLI workflow
   - `references/testing-security-deploy.md` for protocol, snapshot, and security tests
   - `references/migration-rmcp-to-pmcp.md` for migration
   - `references/version-matrix.md` for PMCP 2.6-2.17 and cargo-pmcp 0.15-0.20 adoption decisions
   - `references/sources.md` for official-source checks

## When NOT to use

Do not use for non-MCP Rust services, browser/UI work, or generic CLI apps with no MCP surface.
