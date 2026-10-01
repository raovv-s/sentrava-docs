---
title: mTLS Transport
slug: transport-mtls
category: Transports
---

# mTLS Transport

mTLS is the default and fully supported transport. It uses mutual TLS: both the server and the agent present certificates during the handshake. The agent's certificate is embedded at compile time and never written to disk.

## How enrollment works

A generated agent carries its own unique TLS certificate and private key. On first check-in, the server validates:

1. **CA trust** — the agent cert is signed by the server's CA
2. **AgentID** — the embedded AgentID matches an enrollment record in the database
3. **OperationID** — the AgentID belongs to the correct operation
4. **Status** — the enrollment record is active (not pending, revoked, or expired)

A CA-signed certificate alone is not enough. An unknown AgentID is rejected even with a valid signature.

## Start a listener

```sh
# From the operator CLI
sentrava > listeners start mtls <host:port>

# Example: listen on all interfaces, port 4433
sentrava > listeners start mtls 0.0.0.0:4433
```

## Generate an agent

```sh
# Default: mTLS transport, beacon mode
sentrava > generate --listener <ip>:4433

# Session mode: keeps connection open, tasks delivered immediately
sentrava > generate --agent-mode session --listener <ip>:4433
```

The generator embeds:

- Agent TLS certificate and private key
- Server CA certificate
- Server address (`<ip>:4433`)
- AgentID and OperationID (XOR-obfuscated in the binary)

## Embedded credentials

All credentials are injected via Go ldflags at build time:

| Ldflag variable | Value | Encoding |
|---|---|---|
| `embeddedCert` | Agent TLS certificate | Base64 PEM |
| `embeddedKey` | Agent TLS private key | Base64 PEM |
| `embeddedCA` | Server CA certificate | Base64 PEM |
| `embeddedServer` | Server address | XOR ciphertext + key (hex) |
| `embeddedAgentID` | Agent UUID | XOR ciphertext + key (hex) |
| `embeddedOperationID` | Operation UUID | XOR ciphertext + key (hex) |

The XOR obfuscation hides the server address and identity strings from `strings ./agent`.

## Revocation

Revoke an agent to prevent further check-ins immediately:

```sh
sentrava > agents revoke <agent-id>
```

Revocation is enforced server-side on every check-in. A revoked agent cannot reconnect regardless of its credentials.

## Persistent result delivery

mTLS agents use disk-backed result persistence. Task results are saved to `<agent-dir>/.state/results/` before transmission. If the agent exits before the server acknowledges receipt, results survive restart and are retransmitted on next run.

## Ports and defaults

| Service | Default address |
|---|---|
| Agent mTLS listener | `127.0.0.1:4433` (loopback) |
| Operator gRPC | `127.0.0.1:50051` |

Use an explicit `--listener <external-ip>:4433` to accept connections from remote targets.
