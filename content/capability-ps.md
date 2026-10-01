---
title: Process List
slug: capability-ps
category: Capabilities
---

# Process List

The `ps` capability retrieves a snapshot of running processes from the target and returns it as a task result.

## Usage

```
sentrava [session] > ps
```

## Output format

The process list is returned as a table with columns depending on the target platform:

| Column | Description |
|---|---|
| PID | Process ID |
| PPID | Parent process ID |
| Name | Process name (executable filename) |
| User | Owner of the process |
| Arch | Process architecture (x64/x86) |

## Examples

```
sentrava [session] > ps
```

The output is formatted in the CLI and stored as a task result in the database.

## Use cases

Common post-exploitation uses for the process list:

- Identify security tools (AV, EDR, monitoring agents) running on the target
- Find high-value processes to target for injection or credential harvesting
- Enumerate user-owned processes to understand who is logged in
- Identify parent/child process relationships

## Platform notes

- **Linux:** reads from `/proc` filesystem — no additional privileges required for public process information
- **Windows:** uses Windows API process enumeration

## Task persistence

The process list snapshot is stored as a task result. You can retrieve it later:

```
sentrava [session] > tasks list
```

Results are associated with the session and persisted in the server's SQLite database.

## Limitations

The snapshot represents point-in-time state. Processes created or terminated after the task was sent will not appear. Send the task again to refresh.
