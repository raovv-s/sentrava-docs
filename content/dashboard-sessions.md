---
title: Sessions
slug: dashboard-sessions
category: Dashboard
---

# Sessions

The Sessions section of the dashboard shows active and historical agent sessions, the task queue for each session, and task results.

## Session lifecycle

A session begins when an active agent checks in and the server creates a session record. The session remains open until:

- The agent is revoked
- The operation is closed
- The agent stops checking in and the session times out
- The session is explicitly killed with `sessions kill <id>`

## Dashboard response codes

| Outcome | Meaning |
|---|---|
| TLS or network failure | The browser has not established a trusted HTTPS connection |
| HTTP 401 | A valid authenticated web session is required — log in again |
| HTTP 403 | The request fails permission, CSRF, or route policy |

## CLI session commands

```sh
# List active sessions
sentrava > sessions list

# Select a session to work in
sentrava > sessions use <session-id>

# Kill a session
sentrava > sessions kill <session-id>
```

## Working in a session

After `sessions use <id>`, the prompt changes to `sentrava [session] >` and all commands execute in the context of that session:

```
sentrava [session] > whoami
sentrava [session] > ps
sentrava [session] > shell id
sentrava [session] > portfwd add --local 9090 --remote 192.168.1.100:22
```

Exit the session context:

```
sentrava [session] > back
```

## Task results

Tasks are stored in the database and associated with the session. View past results from the dashboard Tasks tab or from the CLI:

```
sentrava [session] > tasks list
```

Results survive agent restart (for mTLS agents with persistent result delivery). The server acknowledges receipt and deletes the on-disk result file only after confirmation.

## Operations and sessions

Sessions belong to an operation. Closing an operation prevents further check-ins from agents in that operation. Use `operations close <id>` to end an operation and terminate all associated sessions.

```sh
sentrava > operations list
sentrava > operations close <operation-id>
```

## RBAC

The dashboard enforces role-based access control. An operator can only view and interact with sessions belonging to operations they are authorized for. A rendered button in the dashboard does not grant permission that the server would deny — the server re-checks authorization on every mutating request.
