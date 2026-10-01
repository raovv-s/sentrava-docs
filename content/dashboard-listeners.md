---
title: Listeners
slug: dashboard-listeners
category: Dashboard
---

# Listeners

The Listeners section of the dashboard shows all configured agent listeners and their runtime state.

## What a listener record shows

| Field | Meaning |
|---|---|
| ID | Unique listener identifier |
| Type | Transport protocol: `mtls`, `tcp`, or `http` |
| Address | The bind address and port (e.g. `0.0.0.0:4433`) |
| Status | `running`, `stopped`, or `error` |
| Started | Timestamp of when the listener was started |

<div class="callout callout-warning"><strong>A displayed listener record is not proof that a socket is accepting traffic.</strong><p>Confirm runtime status independently. A process restart, port conflict, or firewall rule can prevent an agent from connecting even if the listener record shows "running".</p></div>

## Starting a listener from the CLI

Listeners can be managed from both the dashboard and the CLI:

```sh
# mTLS listener (default transport)
sentrava > listeners start mtls 0.0.0.0:4433

# TCP listener with a shared key
sentrava > listeners start tcp 0.0.0.0:5555 <64-char-hex-key>

# HTTP listener with a shared key
sentrava > listeners start http 0.0.0.0:8888 <64-char-hex-key>
```

When you use `generate`, the appropriate listener is started automatically.

## Stopping a listener

From the CLI:

```sh
sentrava > listeners list
sentrava > listeners stop <listener-id>
```

Stopping a listener does not disconnect agents that already have an established session. It prevents new agents from connecting.

## Verification

A running listener shows a socket in `ss` or `netstat`:

```sh
ss -tlnp | grep 4433
```

If the port is not listed, the listener may have failed to bind (port conflict, permission denied for ports < 1024, or wrong interface).

## Listener and agent alignment

Each agent binary is compiled with a specific server address. If you stop a listener and start a new one on a different address or port, existing deployed agents will fail to connect. Regenerate agents for the new listener address.
