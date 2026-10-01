---
title: HTTP Transport
slug: transport-http
category: Transports
---

# HTTP Transport

The HTTP transport sends AES-256-GCM encrypted payloads over plain HTTP polling. C2 profiles shape the traffic to resemble legitimate web traffic (Microsoft Teams presence, Google Analytics beacons, Cloudflare RUM telemetry).

<div class="callout callout-info"><strong>Production ready.</strong><p>HTTP transport uses AES-256-GCM encrypted polling with configurable C2 profiles. Traffic masquerading verified via tcpdump against Teams, Analytics, and Cloudflare profiles.</p></div>

## How it works

The agent polls the server over HTTP at a configurable interval. Each request and response body is AES-256-GCM encrypted with a shared key embedded at compile time. The C2 profile controls the User-Agent header, URI paths, and any additional HTTP headers, making traffic blend with expected application patterns.

## Available profiles

| Profile | Masquerades as | Default beacon interval |
|---|---|---|
| `teams-http` | Microsoft Teams presence polling | 45 s |
| `analytics-http` | Google Analytics beacon | 30 s |
| `cloudflare-http` | Cloudflare RUM telemetry | 60 s |
| `default-http` | Generic HTTP | 60 s |
| `lab-http` | Generic HTTP (fast, for testing) | 5 s |

Profile YAML files live in `profiles/` in the repository root:

```
profiles/
├── teams-http.yaml
├── analytics-http.yaml
├── cloudflare-http.yaml
├── default-http.yaml
└── lab-http.yaml
```

## Generate an agent

```sh
# With a specific profile
sentrava > generate --transport http --profile teams-http --listener <ip>:8888

# With analytics profile
sentrava > generate --transport http --profile analytics-http --listener <ip>:8888

# Default HTTP (no profile masquerading)
sentrava > generate --transport http --listener <ip>:8888
```

## Start a listener manually

```sh
sentrava > listeners start http <host:port> <64-char-hex-key>
```

The `generate` command auto-starts a matching listener. Manual start is only needed if the listener was stopped.

## Embedded profile data

At generate time, the selected profile is serialized to JSON, base64-encoded, and injected into the agent via the `embeddedHTTPProfile` ldflag:

```json
{
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Teams/...",
  "uri_paths": ["/api/presence/v1/me", "/api/messaging/v1/poll"],
  "headers": {
    "X-MS-Client-Version": "...",
    "Accept": "application/json"
  }
}
```

## Beacon interval and jitter

The agent sleeps between polls. The interval comes from the profile's `beacon_sec` value (or the `--sleep` flag). Jitter is applied as a percentage of the base interval.

```sh
# Override beacon interval
sentrava > generate --transport http --profile teams-http --sleep 60s --jitter 20 --listener <ip>:8888
```

## Troubleshooting

**400 on beacon**

The listener shared key does not match the agent binary. Stop the listener, regenerate, restart:

```sh
sentrava > listeners stop <listener-id>
sentrava > generate --transport http --profile teams-http --listener <ip>:8888
```

See [C2 profiles](c2-profiles.html) for the full profile YAML format reference.
