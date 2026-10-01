---
title: Generate Options
slug: generate-options
category: Reference
---

# Generate Options

The `generate` command compiles and packages a configured agent binary. All generate options are specified inside the CLI REPL.

```
sentrava > generate --help
```

## Core flags

| Flag | Default | Description |
|---|---|---|
| `--listener <host:port>` | (required) | Server address the agent will connect to |
| `--transport <transport>` | `mtls` | Transport: `mtls`, `tcp`, or `http` |
| `--os <os>` | `linux` | Target OS: `linux` or `windows` |
| `--arch <arch>` | `amd64` | Target architecture: `amd64` |
| `--agent-mode <mode>` | `beacon` | Agent communication mode: `beacon` or `session` |
| `--sleep <duration>` | `30s` | Beacon interval (e.g. `30s`, `2m`) |
| `--jitter <pct>` | `10` | Jitter percentage applied to sleep interval |
| `--no-activate` | off | Do not auto-activate the agent record after generate |

## Transport flags

| Flag | Required for | Description |
|---|---|---|
| `--profile <name>` | HTTP transport | C2 profile to use (e.g. `teams-http`) |

## OPSEC flags

| Flag | Default | Description |
|---|---|---|
| `--opsec <preset>` | `none` | OPSEC preset: `none`, `basic`, or `full` |
| `--opsec-checks <list>` | (all) | Comma-separated guardrail checks: `sandbox,av,env` |

## Examples

```sh
# Linux mTLS, beacon mode (default)
sentrava > generate --listener 192.168.1.10:4433

# Linux mTLS, session mode
sentrava > generate --agent-mode session --listener 192.168.1.10:4433

# Linux TCP transport
sentrava > generate --transport tcp --listener 192.168.1.10:5555

# Linux HTTP with C2 profile masquerading
sentrava > generate --transport http --profile teams-http --listener 192.168.1.10:8888

# Windows mTLS
sentrava > generate --os windows --arch amd64 --listener 192.168.1.10:4433

# Basic OPSEC (guardrails + validator)
sentrava > generate --opsec basic --listener 192.168.1.10:4433

# Full OPSEC, session mode
sentrava > generate --opsec full --agent-mode session --listener 192.168.1.10:4433

# Generate without auto-activating
sentrava > generate --no-activate --listener 192.168.1.10:4433
```

## Generated package contents

```
~/.local/share/sentrava/client/packages/<package-id>/
├── sentrava-agent          configured binary (Linux)
├── sentrava-agent.exe      configured binary (Windows, if --os windows)
└── manifest.json           operator reference (non-secret metadata)
```

The `manifest.json` contains the AgentID, OperationID, listener address, transport, and generate timestamp. It does not contain private keys or the shared key.

<div class="callout callout-warning"><strong>A generated package is a credential-bearing artifact.</strong><p>Copying the binary to another machine transfers the ability to present the same credentials. Key possession does not prove physical device identity. Protect and revoke agent packages accordingly.</p></div>

## Enrollment policy

| Mode | Activation |
|---|---|
| Default | Agent is auto-activated; connects immediately |
| `--no-activate` | Enrollment record created in `pending` state; requires `agents activate <id>` |

Each generated agent is cryptographically bound to a specific operation and target scope. The server enforces this binding at checkin time.

## Binary compilation

`generate` invokes `go build` on the stock agent binary source with the appropriate ldflags. The agent binary returned is a configured, statically-linked (or CGO_ENABLED=0) binary for the target platform. The compilation happens on the operator machine, not the server.
