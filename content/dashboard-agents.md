---
title: Agents
slug: dashboard-agents
category: Dashboard
---

# Agents

The Agents section of the dashboard shows enrolled agent records and their current enrollment state.

<div class="callout callout-info"><strong>Enrollment state and session state are different.</strong><p>An agent can be enrolled (have a valid database record) without having an active session. A prepared enrollment record is not an authorized live session.</p></div>

## Enrollment states

| State | Meaning |
|---|---|
| `pending` | Agent has a record but has not been explicitly activated |
| `active` | Agent is authorized to check in and create sessions |
| `revoked` | Agent is permanently blocked from connecting |

By default, generated agents require explicit activation before they can establish sessions. The `--no-activate` flag preserves this behavior. The default `generate` command auto-activates the agent for convenience.

## Managing agents from the CLI

```sh
# List all agents
sentrava > agents list

# List agents including inactive ones
sentrava > agents list --status all

# Activate a pending agent
sentrava > agents activate <agent-id>

# Revoke an agent (immediate, fail-closed)
sentrava > agents revoke <agent-id>

# Show agent detail
sentrava > agents status <agent-id>
```

## Revocation

Revoking an agent is immediate and server-enforced. On the next check-in attempt, the server rejects the connection regardless of the agent's certificate validity. There is no way to un-revoke — regenerate the agent if you need to re-authorize it.

## Agent record fields

| Field | Meaning |
|---|---|
| AgentID | UUID embedded in the agent binary at generate time |
| OperationID | Operation the agent belongs to |
| Hostname | Display name set at generate time (metadata only) |
| OS / Arch | Target platform |
| Transport | `mtls`, `tcp`, or `http` |
| Status | `pending`, `active`, or `revoked` |
| Last seen | Timestamp of last successful check-in |

<div class="callout callout-warning"><strong>Hostname is display metadata only.</strong><p>The hostname field is set at generate time and reflects the operator's intended target. It is never verified against the actual machine. Do not use it to identify a physical device.</p></div>

## Agent packages

Generated agent packages are stored at:

```
~/.local/share/sentrava/client/packages/<package-id>/
├── sentrava-agent          configured binary (Linux)
├── sentrava-agent.exe      configured binary (Windows, if generated)
└── manifest.json           operator reference (does not contain private keys)
```

`manifest.json` is a human-readable reference file. The actual credentials are compiled into the agent binary via ldflags and are not separately readable from the package directory.
