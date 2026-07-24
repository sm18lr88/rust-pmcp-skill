# PMCP SDK and cargo-pmcp version matrix

Use this historical matrix when reviewing existing PMCP code and tooling. The SDK and CLI have separate version streams: the GitHub `v0.20.0` release is `cargo-pmcp` 0.20.0, while the `pmcp` crate baseline is 2.17.0. A repository lockfile wins. For new work, pin `pmcp = "=2.17.0"`, use `cargo-pmcp` 0.20.0, require Rust 1.91 or later, and select only the features that the implementation uses.

## PMCP SDK

| Version | Release date | Material change | Adopt or defer |
|---|---:|---|---|
| 2.6.0 | 2026-04-21 | Typed client and list helpers. | Preserve as a historical migration baseline. |
| 2.7.0 | 2026-05-10 | TLS advisory remediation. | Adopt for maintained servers. |
| 2.8.0 | 2026-05-16 | HTTP 401 handling and MSRV 1.91. | Adopt the MSRV/HTTP changes only when the project requires the transport; local stdio stays lean. |
| 2.9.0 | 2026-05-30 | Configuration toolkit and `CallToolResult::rejected`. | Do not add configuration surface merely because it exists. |
| 2.10.0 | 2026-06-21 | Task lifecycle. | Defer without a real asynchronous job lifecycle. |
| 2.11.0 | 2026-06-30 | WASM and task HTTP. | Defer without a real WASM deployment or task HTTP use case. |
| 2.12.0 | 2026-07-05 | `ToolOutput` and full-envelope bypass. | Adopt only when a client needs envelope-level behavior and tests cover it. |
| 2.13.0 | 2026-07-05 | Poll classifier. | Defer unused task-polling behavior. |
| 2.14.0 | 2026-07-08 | Diagnostic detail. | Preserve diagnostic compatibility tests when applicable. |
| 2.15.0 | 2026-07-10 | `structuredContent` and warn-only cached output validation; crate `rust-version = "1.91.0"`. | Default for new work: truthfully advertise `outputSchema` only for structured output. |
| 2.17.0 | 2026-07-19 | Client host handlers and truthful derived capabilities; transport actor; tool-aware peer sampling; opt-in Agent Skills surface. | Default for new work. Add host callbacks, peer sampling, or Agent Skills only for a tested consumer. |

The 2.16 changes were rolled into the published 2.17.0 crate; no `pmcp 2.16.0` package was published.

## cargo-pmcp CLI

| Version | Release date | Material change | Adopt or defer |
|---|---:|---|---|
| 0.15.0 | 2026-05-28 | Google Cloud Run, config-driven SQL scaffold, strict target resolution, and deploy-root discovery. | Historical baseline; preserve `--manifest-path` behavior when invoking outside the project root. |
| 0.16.0 | 2026-06-08 | Azure Container Apps and ingress-ready HTTP scaffold defaults. | Adopt when Azure is the selected target; replace permissive origins with an explicit production policy. |
| 0.17.x | 2026-06-21 to 2026-07-10 | Workbook tooling and successive PMCP scaffold-pin synchronization. | Historical; inspect generated pins because scaffolds can lag the SDK release. |
| 0.18.0 | 2026-07-19 | Published CLI package without a dedicated changelog entry at the 0.20 tag. | Do not infer behavior from the version number; inspect exact source/help when maintaining a lock. |
| 0.19.0 | 2026-07-21 | Remote package capture/import/approve lifecycle and an offline GraphQL contract seam. | Use only for a real pmcp.run package workflow. |
| 0.20.0 | 2026-07-22 | Rust CloudFormation rendering/apply for supported standard scaffolds; custom stacks retain CDK fallback. | Default CLI baseline; require real target acceptance before production renderer cutover. |

## Source record

The dates and release notes above are anchored to published crate metadata, the official changelog, and release tags where available. Verify future updates against all three before revising this matrix.

- [Official 2.6.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.6.0), [Cargo 2.6.0](https://crates.io/crates/pmcp/2.6.0)
- [Official 2.7.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.7.0), [Cargo 2.7.0](https://crates.io/crates/pmcp/2.7.0)
- [Official 2.8.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.8.0), [Cargo 2.8.0](https://crates.io/crates/pmcp/2.8.0)
- [Official 2.9.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.9.0), [Cargo 2.9.0](https://crates.io/crates/pmcp/2.9.0)
- [Official 2.10.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.10.0), [Cargo 2.10.0](https://crates.io/crates/pmcp/2.10.0)
- [Official 2.11.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.11.0), [Cargo 2.11.0](https://crates.io/crates/pmcp/2.11.0)
- [Official 2.12.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.12.0), [Cargo 2.12.0](https://crates.io/crates/pmcp/2.12.0)
- [Official 2.13.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.13.0), [Cargo 2.13.0](https://crates.io/crates/pmcp/2.13.0)
- [Official 2.14.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.14.0), [Cargo 2.14.0](https://crates.io/crates/pmcp/2.14.0)
- [Official 2.15.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.15.0), [Cargo 2.15.0](https://crates.io/crates/pmcp/2.15.0)
- [Official 2.17.0 tag](https://github.com/paiml/rust-mcp-sdk/releases/tag/v2.17.0), [Cargo 2.17.0](https://crates.io/crates/pmcp/2.17.0), [published Cargo manifest](https://docs.rs/crate/pmcp/2.17.0/source/Cargo.toml)
- [cargo-pmcp 0.15-0.20 changelog](https://github.com/paiml/rust-mcp-sdk/blob/v0.20.0/cargo-pmcp/CHANGELOG.md), [0.20.0 release](https://github.com/paiml/rust-mcp-sdk/releases/tag/v0.20.0), [Cargo 0.20.0](https://crates.io/crates/cargo-pmcp/0.20.0)
