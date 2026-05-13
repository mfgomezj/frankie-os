# Global Shared Skills — Gentleman Stack v1.26.5

## Compact Rules (auto-injected)

### LLM-First Standards
- **Intent Recognition**: Always prioritize the `project_key` and `intent` fields in every interaction.
- **Context Injection**: Use the `.atl/_shared` directory for rules that must survive session compactions.
- **Zero-Dependency**: Favor pre-compiled binaries for Engram and Hermes over local language runtimes (Go/Python) when available.

### Persistence Protocol
- **Postgres-First**: Primary memory target is the local/cloud Postgres instance via Hermes v2.0 adapters.
- **Sync Rule**: Local `mem_save` must trigger a background sync to the shared semantic layer.

### Hermes v2.0 Adapters
- Support for: `gemini-cli`, `cursor-agent`, `vscode-copilot`, `antigravity-orchestrator`.
- Connection String: Must follow the `postgresql://user:pass@host:port/db` format.
