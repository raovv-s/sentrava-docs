---
title: OPSEC Presets
slug: opsec-presets
category: OPSEC
---

# OPSEC Presets

Presets are named collections of OPSEC modules selected at generate time with the `--opsec` flag. They are shortcuts; you can also enable individual modules with explicit flags.

## Preset reference

| Preset | Modules enabled | KillOnDetection |
|---|---|---|
| `none` | None (default) | Off |
| `basic` | guardrails, validator | Off |
| `full` | guardrails, validator, sleepmask, canary, polymorph | Off |

`KillOnDetection` is **off** by default for all presets. Detections are logged and the agent continues running. This is intentional — silent kill-on-detect makes debugging harder and does not improve operational security in most scenarios.

## Usage

```sh
# No OPSEC (default — same as omitting --opsec)
sentrava > generate --opsec none --listener <ip>:4433

# Basic: environment and certificate checks only
sentrava > generate --opsec basic --listener <ip>:4433

# Full: all five modules
sentrava > generate --opsec full --listener <ip>:4433
```

## Combining presets with other flags

```sh
# Full OPSEC, session mode, Windows target
sentrava > generate --opsec full --agent-mode session --os windows --arch amd64 --listener <ip>:4433

# Basic OPSEC with HTTP transport and profile
sentrava > generate --opsec basic --transport http --profile teams-http --listener <ip>:8888
```

## Important notes

- **Presets are applied at compile time.** Changing OPSEC settings requires regenerating the agent.
- **Preset names can change independently of the verified enrollment workflow.** Always read the help for the exact built binary rather than assuming a preset name implies a specific behavior.
- **sleepmask is Linux-only.** When `--opsec full` is used to generate a Windows agent, the sleepmask module compiles to a no-op stub.
- **Validate independently.** A preset name and a passing build are not evidence that a protection is effective on a given target. Test each module against your target environment.

## Per-module guardrail checks

With `--opsec basic` or `--opsec full`, you can specify which guardrail checks to run:

```sh
# Sandbox detection only
generate --opsec basic --opsec-checks sandbox --listener <ip>:4433

# Sandbox + AV detection
generate --opsec basic --opsec-checks sandbox,av --listener <ip>:4433

# All checks (default with --opsec full)
generate --opsec full --opsec-checks sandbox,av,env --listener <ip>:4433
```

See [Modules](opsec-modules.html) for per-module behavior detail.
