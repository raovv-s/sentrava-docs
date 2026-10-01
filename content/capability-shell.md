---
title: Shell
slug: capability-shell
category: Capabilities
---

# Shell

Sentrava C2 supports two shell interaction modes: one-shot command execution and interactive PTY shell.

## One-shot: `shell`

Runs a single command on the target and returns output as a task result. Available for all agent modes and transport types.

```
sentrava [session] > shell id
sentrava [session] > shell whoami
sentrava [session] > shell cat /etc/os-release
```

The command is executed by the agent, output is collected, and the result is returned to the server. The operator sees the result in the CLI.

## Interactive PTY: `shell-interactive` / `ish`

Opens a full interactive PTY session on the target. Input and output stream bidirectionally through the established agent connection.

```
sentrava [session] > shell-interactive
sentrava [session] > ish
```

### Key bindings inside the interactive shell

| Key | Action |
|---|---|
| `Ctrl+Q` | Exit interactive shell and return to REPL |
| All other keys | Forwarded to the remote PTY |

### Requirements

Interactive shell has strict requirements:

| Requirement | Detail |
|---|---|
| Transport | mTLS only — requires a persistent session-mode connection |
| Agent mode | Must be generated with `--agent-mode session` |
| Agent OS | Linux only — Windows agents do not support PTY |

Generate a session-mode agent:

```sh
sentrava > generate --agent-mode session --listener <ip>:4433
```

The shell capability is only registered in the agent binary when both `transport == mtls` and `mode == session`. For other combinations the capability is absent and `shell-interactive` is not available.

## Shell vs. session mode

| Mode | Shell command | Interactive shell |
|---|---|---|
| Beacon (default) | Yes | No |
| Session (`--agent-mode session`) | Yes | Yes (mTLS only) |

## Windows agents

Use `shell` for one-shot commands on Windows agents:

```
sentrava [session] > shell whoami
sentrava [session] > shell ipconfig /all
sentrava [session] > shell net user
```

Interactive PTY (`shell-interactive`) is not available on Windows agents. There is no `ConPTY` support in the current codebase.

## Note on task storage

One-shot `shell` results are stored as tasks in the database and retrievable after the fact. Interactive `shell-interactive` input and output are **not** stored as tasks — they stream live through the agent connection and are not persisted.
