# PMCP production guide

Use this when generating or reviewing Rust MCP server code.

## Current baseline

For greenfield work, use `pmcp = "=2.17.0"` with Rust 1.91 or later. Existing `Cargo.lock`, `Cargo.toml`, declared MSRV, and enabled feature set win: inspect all four before changing an established server. Confirm the exact 2.17 API against the official documentation and source before copying a macro or builder pattern. See [version-matrix.md](version-matrix.md) and [sources.md](sources.md).

## Preferred APIs

Prefer these PMCP APIs for new code:

- `pmcp::{Server, ServerBuilder, ServerCapabilities}` for the server.
- `#[mcp_tool]`, `#[mcp_server]`, and `#[mcp_prompt]` behind the `macros` feature for concise, schema-derived handlers.
- `TypedTool`, `TypedToolWithOutput`, `tool_typed`, or `tool_typed_sync` when macros are not appropriate.
- `RequestHandlerExtra` for request metadata, cancellation/progress, peer notifications, and middleware-provided extensions.
- `pmcp::Result<T>` plus `pmcp::Error` constructors for protocol-facing errors.
- `ToolOutput::Result` only when the implementation intentionally owns the complete result response: it bypasses response middleware.

Avoid legacy `rmcp` examples unless the user explicitly requests the official `rmcp` SDK instead of PAIML PMCP.

## Dependency policy

Start lean and add features only when needed:

```toml
[dependencies]
pmcp = { version = "=2.17.0", features = ["macros", "schema-generation"] }
tokio = { version = "1", features = ["rt-multi-thread", "macros", "signal"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
schemars = "1"
thiserror = "2"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "fmt"] }
```

Feature selection:

- Local assistant over stdio: `macros`, `schema-generation`, and `validation` only when the tool needs PMCP's warn-only cached-output validation.
- HTTP/OAuth: add an HTTP transport and authentication feature only for a real remote endpoint with its own threat model and integration tests.
- Browser/client websocket, MCP Apps/widgets, Agent Skills, WASM, Tasks, sampling, and elicitation: defer unless the product has a concrete consumer and tests for the capability.
- `full`: prototype-only; remove it before production unless every enabled capability has a use case.

For a binary MCP server, commit `Cargo.lock`.

## Tool design

Every tool should have:

1. A short verb-noun tool name (`search_docs`, `create_ticket`, `get_invoice`).
2. A narrow description that includes side effects and preconditions.
3. Strongly typed input and output structs when the result is structured.
4. `#[schemars(deny_unknown_fields)]` or equivalent schema strictness when supported.
5. Field descriptions, ranges/enums, and examples where helpful.
6. Annotations:
   - `read_only` for no mutation.
   - `destructive` for data/file/remote mutation.
   - `idempotent` when repeated calls are safe.
   - `open_world` when it accesses external systems.

Do not expose raw shell, SQL, filesystem, or network access as a generic tool. Wrap specific, validated operations.

## Output schemas and result middleware

Since PMCP 2.15, advertise `outputSchema` only when the tool actually returns truthful structured output. Emit both `structuredContent` and canonical JSON text for that output. PMCP's cached-output validation logs warnings for schema drift; it never rejects or mutates the server result. A client may validate and reject separately at its own boundary. Never declare a fabricated `serde_json::Value` schema just to make a tool look structured. A text-only result remains text-only and has no `outputSchema`.

`ToolOutput::Result` is an escape hatch for a deliberately complete response. It bypasses response middleware, so use it only when that bypass is part of the contract and cover the serialized result in an integration snapshot. Ordinary typed tool results should keep normal response middleware active.

## Macro pattern

Use this as the default shape after compile-checking the exact PMCP 2.17 syntax in the target project:

```rust
use pmcp::mcp_server;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Clone)]
pub struct AppServer;

#[derive(Debug, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
pub struct AddArgs {
    #[schemars(description = "Left operand")]
    pub a: f64,
    #[schemars(description = "Right operand")]
    pub b: f64,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct AddOutput {
    pub sum: f64,
}

#[mcp_server]
impl AppServer {
    /// Add two numbers.
    #[mcp_tool(
        description = "Add two numbers",
        annotations(read_only = true, idempotent = true)
    )]
    async fn add(&self, args: AddArgs) -> pmcp::Result<AddOutput> {
        Ok(AddOutput { sum: args.a + args.b })
    }
}
```

Register with the 2.17 `ServerBuilder` API documented by the locked dependency. Do not turn an uncompiled reference snippet into a project API contract.

## Error handling

- Use domain errors internally (`thiserror` or `anyhow::Context` at boundaries).
- Convert to `pmcp::Error` only at the MCP boundary.
- Return validation errors for malformed input and internal errors only for unexpected failures.
- Include actionable, non-secret error messages.
- Never leak tokens, file contents outside allowed roots, DB credentials, stack traces, or raw upstream responses that may contain secrets.

## Async and state

- Prefer immutable `Arc<T>` services and short-lived locks.
- Avoid holding `Mutex`/`RwLock` guards across `.await`.
- Use `tokio::sync` for async locks and `parking_lot` for purely synchronous state.
- Bound concurrency with semaphores or rate limiters for remote APIs.
- Add timeouts around network calls.

## Client host callbacks and peer requests

- PMCP 2.17 derives client `sampling`, `elicitation`, and `roots` capabilities from handlers registered through `ClientBuilder`; do not advertise a host capability without its handler.
- Use `PeerHandle::sample_with_tools` with `ClientBuilder::on_sampling_with_tools` only when a server handler genuinely needs an in-request client round trip with tool-use blocks.
- Exercise peer callbacks over a real duplex transport. PMCP 2.17's transport actor keeps response routing live while request handling remains serialized; do not add lock or polling workarounds for the pre-2.17 transport design.

## Transport

- Use stdio for desktop/CLI clients. Protocol bytes are the only stdout output; send tracing and diagnostics to stderr.
- Use Streamable HTTP only for a real remote/cloud server.
- Enable DNS rebinding protection, strict allowed origins, CORS only where needed, auth, request size limits, and security headers for HTTP.
- Avoid old SSE-only transport unless a client requires it.

## Observability

- Initialize `tracing_subscriber` with `EnvFilter`.
- Include request/tool names and correlation IDs when available.
- Log starts/stops/errors, not arguments that may contain secrets.
- For HTTP production, expose health/readiness separately from MCP if the platform supports it.

## Review checklist

- Type-safe schemas for every tool/prompt.
- No unbounded user-controlled filesystem/network/shell.
- Runtime paths do not use `unwrap`, `expect`, or panic.
- `outputSchema` is truthful: structured output emits `structuredContent` plus canonical JSON text, while text-only results omit it.
- Cached-output validation warnings are tested as non-mutating server observability; any client-side rejection is tested separately.
- `ToolOutput::Result` uses are intentional and snapshot-tested because they bypass response middleware.
- HTTP/OAuth/WASM/Tasks/Agent Skills/sampling/elicitation are absent unless a documented use case requires them.
- Client host capabilities are backed by registered handlers, and any peer callback is tested over a duplex transport.
- All side effects are annotated and documented.
- Tests exercise schema, success, validation failure, auth failure, and representative upstream errors.
- `cargo fmt`, `cargo clippy -- -D warnings`, `cargo test` pass.
