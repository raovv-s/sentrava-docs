---
title: Installation
slug: installation
category: Getting started
---

# Installation

## Requirements

| Component | Requirement | Purpose |
|---|---|---|
| Go | 1.21+ | All binary builds |
| C compiler | GCC | Server SQLite driver (`CGO_ENABLED=1`) |
| Python 3 | Any recent version | Windows agent delivery helper |
| Linux/amd64 | Server and operator machine | Verified runtime platform |

The agent can be cross-compiled for Windows with `CGO_ENABLED=0`. The server requires `CGO_ENABLED=1` for the SQLite driver.

## Build the Go components

```sh
# Server (CGO required for SQLite)
CGO_ENABLED=1 go build -o ./bin/sentrava-server ./cmd/server

# Operator CLI
go build -o ./bin/sentrava-client ./cmd/client

# Stock agent binary (unconfigured — used as base for generate)
go build -o ./bin/sentrava-agent ./cmd/agent
```

Or use the provided Makefile targets:

```sh
make release-server      # builds server with CGO
make build               # builds all three binaries
```

## Build the dashboard (optional)

The web dashboard is a separate frontend served as static files. The server reads from the configured `dashboard/dist` directory at runtime.

```sh
cd dashboard
npm ci
npm run build
```

## Verify the build

```sh
./bin/sentrava-server --help
./bin/sentrava-client --help
./bin/sentrava-agent --version 2>/dev/null || echo "stock binary built"
```

## First run

On first startup the server generates its PKI (CA, server cert, operator cert) and initializes the SQLite database:

```sh
./bin/sentrava-server
```

Default paths:

| Resource | Default location |
|---|---|
| Database | `./sentrava.db` (current directory) |
| PKI directory | `./certs/` |
| gRPC operator API | `127.0.0.1:50051` |
| Dashboard HTTPS | `127.0.0.1:8080` |
| Agent mTLS listener | `127.0.0.1:4433` (default, loopback only) |

Use `--db` and `--certs` flags to override the database and PKI paths:

```sh
./bin/sentrava-server --db /opt/sentrava/sentrava.db --certs /opt/sentrava/certs
```

## Next steps

- [Quick start](quick-start.html) — get a session in five minutes
