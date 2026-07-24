# MCP client config snippets

Adapt paths and URLs to the generated server.

## Stdio

The server must reserve stdout for MCP protocol frames. Send `tracing` output and diagnostics to stderr.

```json
{
  "mcpServers": {
    "my-rust-server": {
      "command": "/absolute/path/to/target/release/my-rust-server",
      "args": [],
      "env": {
        "RUST_LOG": "info"
      }
    }
  }
}
```

## Streamable HTTP

Use this only for a real remote deployment with an approved HTTP authentication and origin policy. Do not add HTTP/OAuth solely to provide an alternate local transport.

```json
{
  "mcpServers": {
    "my-rust-server": {
      "url": "https://my-server.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MCP_TOKEN}"
      }
    }
  }
}
```

Client-specific schema differs. Inspect the target client's current MCP configuration docs before finalizing.
