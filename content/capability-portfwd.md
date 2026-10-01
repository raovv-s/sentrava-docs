---
title: Port Forwarding
slug: capability-portfwd
category: Capabilities
---

# Port Forwarding

Port forwarding tunnels TCP traffic through the agent to a host reachable from the target but not directly from the operator machine.

<div class="callout callout-info"><strong>Requires an active session.</strong><p>Port forwarding commands are only available when you have selected a session with <code>sessions use &lt;id&gt;</code>.</p></div>

## How it works

The operator opens a local TCP port. When a client connects to that local port, traffic is forwarded through the agent's C2 channel to the specified remote host and port. The remote host is resolved and contacted by the agent on the target network.

## Commands

```sh
# Add a forwarder: local port 9090 → target's 192.168.1.100:22
sentrava [session] > portfwd add --local 9090 --remote 192.168.1.100:22

# List active forwarders
sentrava [session] > portfwd list

# Stop a specific forwarder
sentrava [session] > portfwd stop fwd-9090-192.168.1.100-22
```

## Examples

### SSH tunneling

Reach an internal SSH server at `192.168.1.100:22` through the agent:

```sh
sentrava [session] > portfwd add --local 9090 --remote 192.168.1.100:22
# Then from the operator machine:
ssh -p 9090 user@127.0.0.1
```

### RDP tunneling

```sh
sentrava [session] > portfwd add --local 3389 --remote 127.0.0.1:3389
# Connect your RDP client to 127.0.0.1:3389
```

### Internal web service

```sh
sentrava [session] > portfwd add --local 8080 --remote 10.10.10.5:80
# Then browse to http://127.0.0.1:8080
```

## Port restrictions

Ports below 1024 require root on Linux. Use ports `>= 1024` for the local listener side of port forwarding.

## Forwarder IDs

Forwarder IDs are derived from the local port and remote address in the format `fwd-<localport>-<remote-host>-<remote-port>`. Use `portfwd list` to see the exact ID if you need to stop a forwarder.

## Cleanup

Forwarders are stopped when you kill the session or the agent disconnects. Use `portfwd stop` to stop an individual forwarder while the session remains active.

```sh
sentrava [session] > portfwd list
sentrava [session] > portfwd stop fwd-9090-192.168.1.100-22
```
