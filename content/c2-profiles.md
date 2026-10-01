---
title: C2 Profiles
slug: c2-profiles
category: Reference
---

# C2 Profiles

C2 profiles shape the HTTP transport's traffic to resemble legitimate web activity. Each profile defines the User-Agent header, URI paths, beacon interval, and any additional HTTP headers the agent sends.

Profiles are YAML files stored in the `profiles/` directory at the repository root.

## Available profiles

| Profile | Masquerades as | Beacon interval |
|---|---|---|
| `teams-http` | Microsoft Teams presence polling | 45 s |
| `analytics-http` | Google Analytics beacon | 30 s |
| `cloudflare-http` | Cloudflare RUM telemetry | 60 s |
| `default-http` | Generic HTTP | 60 s |
| `lab-http` | Generic HTTP (fast, for testing) | 5 s |

## Profile YAML format

```yaml
name: teams-http
user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Teams/1.6.0.30111"
uri_paths:
  - /api/presence/v1/me
  - /api/messaging/v1/poll
  - /api/messaging/v1/ack
beacon_sec: 45
headers:
  X-MS-Client-Version: "1.6.0.30111"
  Accept: "application/json"
  Content-Type: "application/json"
```

### Fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Profile identifier (matches the filename without `.yaml`) |
| `user_agent` | string | HTTP User-Agent header value |
| `uri_paths` | list of strings | URI paths used for check-in requests (cycled or selected) |
| `beacon_sec` | integer | Default beacon interval in seconds |
| `headers` | map | Additional HTTP headers added to every request |

## File layout

```
profiles/
├── teams-http.yaml
├── analytics-http.yaml
├── cloudflare-http.yaml
├── default-http.yaml
└── lab-http.yaml
```

## Using a profile

Specify the profile name (without `.yaml`) at generate time:

```sh
sentrava > generate --transport http --profile teams-http --listener <ip>:8888
sentrava > generate --transport http --profile analytics-http --listener <ip>:8888
sentrava > generate --transport http --profile cloudflare-http --listener <ip>:8888
```

At generate time, the profile's `user_agent`, `uri_paths`, and `headers` are serialized to JSON, base64-encoded, and embedded in the agent binary via the `embeddedHTTPProfile` ldflag. The `beacon_sec` from the profile is used as the default sleep interval unless overridden with `--sleep`.

## Custom profiles

Create a new YAML file in `profiles/` following the format above. Use the filename (without `.yaml`) as the `--profile` argument. The profile is read from disk at generate time — no server restart is needed.

```yaml
name: custom-cdn
user_agent: "Amazon CloudFront"
uri_paths:
  - /cdn-cgi/trace
  - /health
beacon_sec: 90
headers:
  Accept: "*/*"
```

```sh
sentrava > generate --transport http --profile custom-cdn --listener <ip>:8888
```

## Notes

- Profiles only affect HTTP transport agents. mTLS and TCP agents ignore profile settings.
- The payload body is always AES-256-GCM encrypted regardless of profile. Profile fields only shape the HTTP headers and URI.
- Choose the profile that best matches the target environment's expected traffic patterns. HTTP profile selection significantly improves beacon traffic blending during authorized engagements.
