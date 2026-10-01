---
title: OPSEC Modules
slug: opsec-modules
category: OPSEC
---

# OPSEC Modules

Each module is a discrete Go package compiled into the agent when enabled. Modules register themselves with the agent's capability registry at startup and are invoked by the agent core at appropriate lifecycle points.

## guardrails

**Category:** Pre-flight check  
**Ldflag:** `embeddedOpsecGuardrails=true`

Runs environment checks before the agent begins beaconing. Detections are logged; with `KillOnDetection` enabled the agent exits.

Checks include:

- **Sandbox detection** — virtual machine indicators, low uptime, minimal process count
- **AV process detection** — scans the process list for known security products including CrowdStrike, SentinelOne, Carbon Black, ESET, Malwarebytes, Sophos, and Bitdefender
- **Environment guardrails** — unusual `PATH`, missing expected directories, non-interactive session indicators

Specific checks can be selected at generate time:

```sh
# Only sandbox and AV checks
generate --opsec basic --opsec-checks sandbox,av --listener <ip>:4433

# All checks
generate --opsec full --listener <ip>:4433
```

## validator

**Category:** Pre-flight check  
**Ldflag:** `embeddedOpsecValidator=true`, `embeddedOpsecServerHash=<sha256-hex>`

Pins the SHA-256 fingerprint of the server's TLS certificate. On every check-in, the agent recomputes the peer certificate fingerprint and rejects connections to any server that does not match the pinned hash. This detects TLS interception and sinkholes.

The server cert hash is computed at generate time and embedded in the agent binary.

## sleepmask

**Category:** Runtime memory protection  
**Ldflag:** `embeddedOpsecSleepMask=true`

Protects agent memory during the beacon sleep interval.

**OnPreSleep:**
1. XOR-masks the agent's memory region with a random key
2. Calls `mprotect(PROT_NONE)` to make the pages inaccessible
3. Calls `madvise(MADV_DONTNEED)` to release the physical pages to the OS — forensic tools find no resident memory during sleep

**OnPostSleep:**
1. Calls `mprotect(PROT_READ|PROT_WRITE)` to restore access
2. Re-randomizes the memory region and key (pages are zero-filled after `MADV_DONTNEED` — decryption is not needed)

Linux-only. Windows and macOS compile with no-op stubs.

## canary

**Category:** Runtime anti-debug  
**Ldflag:** `embeddedOpsecCanary=true`

Monitors for debugging and tracing indicators:

- `/proc/self/status` `TracerPid` field — non-zero means a debugger is attached
- Timing anomalies — sleep/wake cycle takes significantly longer than expected
- `LD_PRELOAD` environment variable set

## polymorph

**Category:** Runtime config protection  
**Ldflag:** `embeddedOpsecPolymorph=true`

At startup, reads the embedded config block and re-encrypts it with a freshly generated AES-256-GCM key. The plaintext config never persists in the binary's data segment after initialization. This complicates static analysis of a captured agent binary.

## Module ID reference

Modules are addressed in the capability registry by these IDs:

| Module | Registry ID |
|---|---|
| sleepmask | `opsec.sleepmask` |
| guardrails | `opsec.guardrails` |
| validator | `opsec.validator` |
| canary | `opsec.canary` |
| polymorph | `opsec.polymorph` |
