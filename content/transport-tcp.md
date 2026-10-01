---
title: TCP Transport
slug: transport-tcp
category: Transports
---

# TCP Transport

The TCP transport uses AES-256-GCM encryption over a raw TCP connection. A shared key is generated at generate time and embedded in the agent binary. There is no certificate-based enrollment — the shared key is the trust anchor.

<div class="callout callout-info"><strong>Production ready.</strong><p>TCP transport uses AES-256-GCM encryption with a per-agent shared key embedded at build time via ldflags. Verified end-to-end in lab environments.</p></div>

## How it works

1. A 32-byte random shared key is generated when you run `generate --transport tcp`.
2. The key is embedded in the agent binary as a hex-encoded ldflag.
3. The server starts a TCP listener with the same key.
4. All communication between the agent and server is encrypted with AES-256-GCM using that key.

## Start a listener

The listener is started automatically by `generate` when `--transport tcp` is specified. To start one manually:

```sh
sentrava > listeners start tcp <host:port> <64-char-hex-key>
```

## Generate an agent

```sh
sentrava > generate --transport tcp --listener <ip>:5555
```

The generator creates the shared key, starts the listener, and embeds the key in the agent binary.

## Embedded credentials

| Ldflag variable | Value | Encoding |
|---|---|---|
| `embeddedSharedKey` | AES-256 key | 64-char hex string |
| `embeddedServer` | Server address | XOR ciphertext + key (hex) |
| `embeddedAgentID` | Agent UUID | XOR ciphertext + key (hex) |
| `embeddedOperationID` | Operation UUID | XOR ciphertext + key (hex) |

## Differences from mTLS

| Feature | mTLS | TCP |
|---|---|---|
| Authentication | Mutual TLS certificates | Shared key |
| Enrollment check | Server-side per check-in | Key validity only |
| Revocation | Immediate, server-enforced | Not supported |
| Persistent results | Yes (disk-backed) | No |
| Interactive shell | No | No |
| Windows support | Yes | Yes |

## Troubleshooting

**HTTP agent 400 on beacon (wrong transport)**

If you start a TCP agent against an HTTP listener, check-ins fail with a 400. Stop the old listener, regenerate the agent with the correct transport, and start a matching listener.

**Shared key mismatch**

The listener and agent must use the same key. If you lose the key, stop the listener, regenerate the agent, and start a new listener.
