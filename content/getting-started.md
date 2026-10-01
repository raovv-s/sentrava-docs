---
title: Getting Started
slug: getting-started
category: Getting started
---

# Getting Started with Sentrava C2

<div class="callout callout-info"><strong>Authorized security testing only.</strong><p>Use Sentrava only within a documented authorization boundary. Keep test databases, PKI, and credentials separate from any existing installation.</p></div>

Sentrava C2 is a command-and-control framework for authorized red team operations. It provides a gRPC-based teamserver with mTLS operator authentication, an operator CLI, a web dashboard, and a configurable agent binary that embeds its credentials at compile time.

## Architecture

The framework has four components that operate together:

| Component | Binary | Role |
|---|---|---|
| Teamserver | `sentrava-server` | Hosts gRPC operator API, HTTPS dashboard, and agent listeners |
| Operator CLI | `sentrava-client` | Interactive REPL for managing operations, agents, and sessions |
| Agent | `sentrava-agent` | Implant binary deployed on the target; connects back to the teamserver |
| Dashboard | `dashboard/dist/` | Web frontend served by the teamserver's HTTPS listener |

## Transport options

Three transport layers are supported:

- **mTLS** (default) — mutual TLS; the agent's certificate is embedded at build time and validated against server enrollment records
- **TCP** — AES-256-GCM encrypted TCP; a shared key is embedded at build time
- **HTTP** — AES-256-GCM encrypted HTTP polling with C2 profile masquerading

## Supported platforms

- **Server and operator CLI:** Linux/amd64
- **Agent (Linux):** Linux/amd64 — fully supported, all capabilities available
- **Agent (Windows):** Windows/amd64 — mTLS transport; interactive shell requires a Linux agent

## How an operation works

1. Start the teamserver; it initializes its PKI and SQLite database on first run.
2. Connect with the operator CLI and create an operation with a target scope.
3. Generate an agent package — the CLI compiles and signs an agent binary with embedded credentials.
4. Deploy the agent binary to the target.
5. The agent connects back; the server verifies enrollment; a session appears in the CLI.
6. Run tasks against the session: `whoami`, `shell`, `ps`, `portfwd`, and more.

## Next steps

- [Installation](installation.html) — build requirements and steps
- [Quick start](quick-start.html) — get a session in five minutes
- [mTLS transport](transport-mtls.html) — enrollment and certificate binding detail
