# cargo-pmcp workflow

Use this when creating, testing, or deploying PMCP servers with the PAIML CLI.

## Availability

Use an already approved `cargo-pmcp` installation or project toolchain. Do not add a global installation as part of routine server work. Check the command and target package version before relying on a generated layout:

```bash
cargo pmcp --version
cargo pmcp --help
```

For greenfield work without an existing toolchain constraint, use `cargo-pmcp` 0.20.0.

## New workspace-first flow

Prefer this for greenfield work:

```bash
cargo pmcp new my-mcp-workspace
cd my-mcp-workspace
cargo pmcp add server myserver --template minimal
```

Common templates change over time. Current docs mention minimal, calculator, complete/complete-calculator, and sqlite-explorer patterns. Check `cargo pmcp add server --help` before committing to a template.

For config-driven servers, 0.20 also provides single-crate scaffold kinds:

```bash
cargo pmcp new my-sql-server --kind sql-server
cargo pmcp new my-openapi-server --kind openapi-server
cargo pmcp new my-workbook --kind workbook-server
```

Generated dependency pins can lag the release. Inspect and compile the generated manifest before adapting it.

Pin the generated server's dependency exactly before implementation:

```toml
[dependencies]
pmcp = { version = "=2.17.0", features = ["macros", "schema-generation"] }
```

Require Rust 1.91 or later, then compile before adapting generated code.

## Development

```bash
cargo pmcp doctor
cargo pmcp dev --server myserver
```

Use the development transport only when it matches the deployment case. For local stdio servers, test the actual stdio transport and preserve stdout protocol framing.

## Client connection

```bash
cargo pmcp connect --server myserver --client claude-code
cargo pmcp connect --server myserver --client inspector
```

If the target client is not Claude Code, inspect current CLI support:

```bash
cargo pmcp connect --help
```

For Codex/OpenCode projects, still emit copy-paste MCP client config examples in README/docs. Do not assume a client's MCP config path; ask or inspect the repo.

## Tests

Generate scenarios from advertised capabilities, then run them:

```bash
cargo pmcp test generate --server myserver
cargo pmcp test run --server myserver --detailed
cargo pmcp test check http://localhost:3000 --format json
cargo pmcp test conformance http://localhost:3000 --strict --format json
```

For MCP Apps, also run `cargo pmcp test apps <url> --mode <host> --format json` against the actual target host profile.

For approved remote endpoints with a real load-test requirement:

```bash
cargo pmcp loadtest init https://my-server.example.com
cargo pmcp loadtest run https://my-server.example.com --vus 20 --duration 60
```

## Security

Run MCP-specific scans before an approved remote deployment:

```bash
cargo pmcp pentest http://localhost:3000
cargo pmcp pentest http://localhost:3000 --profile deep
cargo pmcp pentest http://localhost:3000 --fail-on medium
```

Treat findings as release blockers unless the user explicitly accepts risk.

## Schema

Use schema export/diff for compatibility control:

```bash
cargo pmcp schema --help
```

Store exported schemas under `schemas/` or `scenarios/` when API stability matters. Diff schemas in CI before releases.

## Packages, agents, and teams

Use these only when the requested product shape needs them:

```bash
cargo pmcp agent new my-agent
cargo pmcp team dev
cargo pmcp package inspect ./bundle.pmcp
```

The 0.19+ remote package lifecycle (`capture`, `import`, and `approve`) is a thin client of pmcp.run. Treat it as a remote platform operation, not a local package build.

## Deploy

For a real approved remote deployment, a typical sequence is:

```bash
cargo pmcp deploy init --target aws-lambda --oauth cognito
cargo pmcp validate deploy
cargo pmcp deploy --target-type aws-lambda
cargo pmcp deploy logs --tail
cargo pmcp deploy metrics --period 24h
cargo pmcp deploy test --verbose
```

Use `--target-type` for a deployment backend; top-level `--target` selects a named target and older deploy uses may retain it as a compatibility alias. Use `--manifest-path` when invoking deploy outside the project root.

In 0.20, unmodified standard `pmcp-run` and `aws-lambda` scaffolds can synthesize CloudFormation through the Rust `pmcp-cfn-renderer`; the AWS path can also apply it without Node, npm, or CDK. A hand-modified `deploy/lib/stack.ts` falls back to the legacy CDK path. Before a production cutover, run a real target acceptance test and account for the documented renderer gaps: unbounded stack polling, manual recovery from `ROLLBACK_COMPLETE`, inline template-size headroom, and the pinned Lambda Web Adapter layer for built-in servers.

Azure Container Apps is also available through `deploy init --target azure-container-apps` and `deploy --target-type azure-container-apps`; it uses `az containerapp up --source` and does not require local Docker.

Targets evolve. Always check `cargo pmcp deploy --help` and project `.pmcp/deploy.toml` before editing. Do not introduce HTTP, OAuth, WASM, Tasks, sampling, or elicitation solely because the CLI exposes them.

## When not to use cargo-pmcp

Use direct `pmcp` APIs when:

- The repo already has a custom workspace layout.
- The user asked for a library crate, not a scaffolded workspace.
- You are patching a small existing server.
- The project must avoid CLI-generated structure.

Even then, keep cargo-pmcp-compatible test scenarios and schema exports where practical.
