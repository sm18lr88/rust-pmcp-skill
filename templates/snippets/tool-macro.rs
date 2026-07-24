// Adapt after checking the repository's locked `pmcp` version, feature set, and Rust MSRV.
// Requires pmcp features: ["macros", "schema-generation"].

use pmcp::mcp_server;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Clone)]
pub struct ExampleServer;

#[derive(Debug, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
pub struct EchoArgs {
    #[schemars(description = "Text to echo back")]
    pub text: String,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct EchoOutput {
    pub text: String,
}

#[mcp_server]
impl ExampleServer {
    /// Echo text without mutation.
    #[mcp_tool(
        description = "Echo text without mutation",
        annotations(read_only = true, idempotent = true)
    )]
    async fn echo(&self, args: EchoArgs) -> pmcp::Result<EchoOutput> {
        let text = args.text.trim();
        if text.is_empty() {
            return Err(pmcp::Error::validation("text must not be empty"));
        }
        Ok(EchoOutput {
            text: text.to_owned(),
        })
    }
}
