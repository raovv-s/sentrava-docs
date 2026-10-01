---
title: Dashboard Overview
slug: dashboard-overview
category: Dashboard
---

# Dashboard Overview

The web dashboard is an optional frontend to the Sentrava C2 teamserver. It provides a graphical view of operations, sessions, tasks, listeners, and agents.

## Access

```
https://127.0.0.1:8080
```

Default credentials are set on the server's first run. The admin password is displayed in the server startup log.

<div class="callout callout-info"><strong>Browser trust and operator login are separate steps.</strong><p>First, trust the server's TLS certificate in your browser (self-signed by the server CA). Then log in with your operator web credentials. The dashboard does not use the operator mTLS certificate — that is CLI-only.</p></div>

## Authentication model

Web sessions use an opaque, `Secure`, `HttpOnly` cookie issued by the server. On every request the server rechecks:

- Current operator permissions
- Disabled / revoked state
- CSRF token validity for mutating requests

Restarting the server invalidates all in-memory web sessions — operators must log in again.

## Dashboard sections

| Section | What it shows |
|---|---|
| Sessions | Active and historical agent sessions; task dispatch |
| Tasks | Task queue, results, and execution history |
| Listeners | Running listeners and their configuration |
| Agents | Enrolled agent records, enrollment status |
| Operations | Operations, their scope, and closure state |
| Builds | Generated agent packages and their manifests |
| Timeline | Chronological audit log of all administrative actions |

## HTTPS certificate

The server presents a self-signed TLS certificate issued by its own CA. Your browser will warn on first visit. To suppress the warning, import the server CA into your browser's trust store:

```sh
# On Debian/Kali — import CA using NSS tools
certutil -A -n "SentravaCA" -t "CT,," -i ./certs/ca.crt -d ~/.pki/nssdb
```

## Dashboard vs. CLI

Both the CLI and the dashboard connect to the same server backend. Actions taken in either interface are reflected in the other in real time. The CLI uses gRPC mTLS; the dashboard uses HTTPS with cookie auth.

## Disabling the dashboard

If you do not need the web interface, you can disable the HTTPS listener. The gRPC operator API remains available for CLI use.

See [Listeners](dashboard-listeners.html), [Agents](dashboard-agents.html), and [Sessions](dashboard-sessions.html) for section-specific detail.
