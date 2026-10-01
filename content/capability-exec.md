---
title: Exec
slug: capability-exec
category: Capabilities
---

# Exec

The exec capability runs arbitrary commands on the target and returns their output as a task result. It is available for all transports and agent modes (beacon and session).

## Usage

```
sentrava [session] > shell <command>
```

Despite using the `shell` CLI keyword, exec dispatches to the agent's exec capability which runs the command directly (not through a shell). To use shell features (pipes, redirects, glob expansion), invoke the shell explicitly:

```
sentrava [session] > shell bash -c "cat /etc/passwd | grep root"
sentrava [session] > shell cmd.exe /c "dir C:\Users"
```

## Examples

```
sentrava [session] > shell id
sentrava [session] > shell uname -a
sentrava [session] > shell hostname
sentrava [session] > shell cat /etc/os-release
sentrava [session] > shell bash -c "find /home -name '*.ssh' -type d 2>/dev/null"
```

Windows:

```
sentrava [session] > shell whoami
sentrava [session] > shell ipconfig /all
sentrava [session] > shell net user
sentrava [session] > shell cmd.exe /c "systeminfo"
```

## Output

Command output (stdout and stderr combined) is captured and stored as a task result in the server database. Results survive agent restart and are available for review after the session ends.

## Timeout

Commands inherit the agent's task timeout. Long-running commands that exceed the timeout are killed by the agent.

## Task persistence

Exec tasks are persisted to the database. View past results:

```
sentrava [session] > tasks list
```

## Difference from interactive shell

The `shell` command is a one-shot exec: it runs the command, collects output, and returns. It does not provide a persistent shell environment. Environment changes (like `cd`) do not persist between invocations.

For an interactive shell with persistent state, use [shell-interactive](capability-shell.html) (mTLS session mode, Linux agents only).
