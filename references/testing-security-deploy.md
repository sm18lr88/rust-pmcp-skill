# Testing, security, and deployment checklist

Use this after implementation and before delivery.

## Unit tests

For each tool:

- Successful request with realistic inputs.
- Input-validation failure for missing/invalid fields.
- Upstream/service failure mapped to a safe MCP error.
- Authorization/permission failure when relevant.
- Serialization snapshot or schema snapshot for stable external contracts.

## Integration tests

- Start server with stdio or HTTP transport.
- Initialize MCP session.
- List tools/prompts/resources.
- Call each tool through the MCP protocol, not just the Rust function.
- Verify `is_error`/error codes, `structuredContent`, and canonical JSON text when a tool truthfully advertises structured output.
- Test cancellation/progress only for tools that perform real long-running work.
- Test request size limits and malformed JSON.

## PMCP 2.15+ output, PMCP 2.17 callbacks, and stdio tests

- For each structured tool that truthfully advertises `outputSchema`, snapshot dual emission: `structuredContent` plus canonical JSON text. Assert schema drift produces the expected PMCP warning; cached-output validation is warn-only and never rejects or mutates the server result.
- If a client performs its own output validation, test its separate rejection behavior at the client boundary rather than attributing that rejection to the server.
- For text-only tools, assert the response remains text-only and does not advertise a made-up `outputSchema`.
- If a tool returns `ToolOutput::Result`, snapshot the full protocol response and prove that its intentional response-middleware bypass does not omit required content.
- For local stdio servers, use a custom transport or harness that captures protocol bytes and stderr independently. Snapshot initialization, `tools/list`, a successful tool result, and a validation failure in request order.
- Drive at least one path with the official SDK/client and `mcp-inspector --cli`; ad-hoc pipe tests alone cannot establish client framing compatibility.
- If the server uses peer sampling, elicitation, or roots, register the matching client host handler and test the callback over a real duplex transport. For tool-aware sampling, pair `PeerHandle::sample_with_tools` with `ClientBuilder::on_sampling_with_tools`.

## Property/fuzz tests

Add when the tool parses user input, URI templates, query languages, filters, or schema mappings:

- `proptest` for valid/invalid generated inputs.
- Fuzz parsers and converters when a panic or regex DoS would be serious.
- Add regression tests for every bug discovered by fuzzing.

## Static quality gates

Use at minimum:

```bash
cargo fmt --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo test --doc --workspace --all-features
cargo audit
cargo deny check
```

For PMCP scenario testing, add:

```bash
cargo pmcp test generate --server <server>
cargo pmcp test run --server <server> --detailed
cargo pmcp test check <url> --format json
cargo pmcp test conformance <url> --strict --format json
```

## Security checklist

- No generic shell, SQL, filesystem, browser, or HTTP fetch tools.
- Explicit allowlists for files, hosts, methods, paths, and MIME types.
- Canonicalize paths and enforce roots after canonicalization.
- Reject symlink escapes unless intentionally allowed.
- Apply timeouts, size limits, and pagination.
- Redact secrets in logs and errors.
- Do not store bearer tokens in project files.
- For HTTP, require auth except local-only dev servers.
- For CORS, use explicit origins; avoid wildcard in production.
- Add rate limiting/backpressure for expensive tools.
- Document side effects in tool descriptions and annotations.

## Deployment checklist

- Build with minimal PMCP features.
- Commit `Cargo.lock` for binary servers.
- Add a health/readiness check if the platform supports it.
- Include service account/IAM permissions in code or IaC, not prose only.
- Add structured logs and metrics.
- Pin external API versions.
- Provide rollback instructions and schema compatibility notes.
- Include MCP client configuration examples for stdio and HTTP.
- Keep HTTP/OAuth/WASM/Tasks/sampling/elicitation out of a release unless the product has a documented use case and capability-specific tests.
- With cargo-pmcp 0.20, verify whether AWS/pmcp.run deployment took the Rust CloudFormation renderer or custom-stack CDK fallback, then run a real post-deploy MCP smoke test. Do not treat renderer golden tests as a substitute for target acceptance.

## README requirements for generated servers

Every server README should include:

- What the server does and what data it can access.
- Required env vars and secrets.
- How to run locally over stdio and/or HTTP.
- MCP client config snippets.
- Tool table with names, descriptions, inputs, outputs, annotations.
- Test commands.
- Security model and limitations.
- Deployment instructions.
