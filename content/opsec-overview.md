---
title: OPSEC Overview
slug: opsec-overview
category: OPSEC
---

# OPSEC Overview

<div class="callout callout-info"><strong>Defense in depth.</strong><p>OPSEC modules are designed to increase operational security during authorized engagements. Use --opsec full for maximum protection. Always validate in your target environment.</p></div>

Sentrava C2 includes a set of optional security hardening modules for the agent binary. These are selected at generate time and compiled into the agent via ldflags. Disabled modules consume no registry slot and produce no runtime overhead.

## Module categories

**Pre-flight checks** run before the agent begins beaconing. If a check fails and `KillOnDetection` is enabled, the agent exits immediately. By default (with `--opsec basic` or `--opsec full`), detections are logged and the agent continues.

**Runtime protections** operate during the agent's lifecycle — masking memory during sleep, validating the server's TLS certificate fingerprint, and monitoring for debugging.

## Available modules

| Module | Category | What it does |
|---|---|---|
| `guardrails` | Pre-flight | Detects sandboxes, AV products, and hostile environments |
| `validator` | Pre-flight | Pins the server TLS certificate fingerprint; detects sinkholes |
| `sleepmask` | Runtime | XOR-masks agent memory and applies page protection during sleep |
| `canary` | Runtime | Anti-debug: monitors `TracerPid`, timing anomalies, `LD_PRELOAD` |
| `polymorph` | Runtime | AES-GCM re-encrypts the agent config block at startup |

## Presets

```
--opsec none    No modules (default)
--opsec basic   guardrails + validator
--opsec full    All five modules
```

See [Presets](opsec-presets.html) for the full preset reference, and [Modules](opsec-modules.html) for per-module detail.

## KillOnDetection

By default all presets leave `KillOnDetection` off. When a detection occurs, the agent logs it and continues. Set `KillOnDetection = true` only when you explicitly want the agent to self-terminate on detection:

```sh
# KillOnDetection is not exposed as a CLI flag by default.
# It can be set in a custom generate invocation via the underlying ldflag.
```

## Platform support

All five modules are Linux-specific. Windows agents compile with stub implementations that are no-ops. The `sleepmask` memory page protection (`mprotect` + `madvise(MADV_DONTNEED)`) is Linux-only by design.

## How modules are registered

Modules are registered in the agent's capability registry only when their corresponding flag is `true`. The registration happens in `main()` before `core.New()`, so the ordering is deterministic regardless of Go package init ordering.
