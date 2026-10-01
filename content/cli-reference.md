---
title: CLI Reference
slug: cli-reference
category: Reference
---

# CLI Reference

The operator CLI (`sentrava-client`) is an interactive REPL. All commands described here are available after connecting to the server. Always inspect the built binary's help for exact flags — a preset name or command in this document may differ from an older or newer binary.

```sh
./bin/sentrava-client --help
```

## Top-level commands

```
help                    Show available commands
exit / quit             Disconnect and exit the CLI
back                    Return to top-level context from a session
```

## Operations

```
operations create <name> --target <ip>   Create an operation with a scope target
operations list                          List all operations
operations close <id>                    Close an operation (prevents further check-ins)
```

## Listeners

```
listeners list
listeners start mtls <host:port>
listeners start tcp <host:port> <hex-key>
listeners start http <host:port> <hex-key>
listeners stop <id>
```

## Generate

```
generate [flags]
```

See [Generate options](generate-options.html) for the full flag reference.

## Agents

```
agents list
agents list --status all
agents activate <id>
agents revoke <id>
agents status <id>
```

## Sessions

```
sessions list
sessions use <id>
sessions kill <id>
```

## In-session commands (after `sessions use <id>`)

### Identity and system

```
whoami
ps
```

### Command execution

```
shell <command>
shell-interactive
ish
```

### Port forwarding

```
portfwd add --local <port> --remote <host:port>
portfwd list
portfwd stop <forwarder-id>
```

### Tasks

```
tasks list
```

## Server connection flags

```sh
./bin/sentrava-client --server 192.168.0.199:50051 --certs-dir ./certs
```

| Flag | Default | Description |
|---|---|---|
| `--server` | `127.0.0.1:50051` | gRPC server address |
| `--certs-dir` | `./certs` | Directory containing operator cert and CA |

## Configuration files

Saved settings are read from `~/.config/sentrava/client.json` (or `$XDG_CONFIG_HOME/sentrava/client.json`). The setting priority is: **explicit flag → saved config → safe default**.

```sh
./bin/sentrava-client configure-local --help
```
