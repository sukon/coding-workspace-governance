# TOOLS.md Registry Format

Use `TOOLS.md` as the repository's human-readable capability registry. Optimize for discovery by future developers and coding agents.

## Required top-level sections

```markdown
# Tool Registry

## Capability Index

| Capability | Tool / Procedure | Path / Command | Notes |
| --- | --- | --- | --- |

## Tools and Procedures
```

## Entry template

Use one entry per reusable capability or coherent multi-command tool.

```markdown
### <Capability or Tool Name>

**Purpose:** <What problem this solves.>

**Path / command:** `<tools/path.py>` or `<external command>`

**Use when:**
- <Trigger or scenario>
- <Trigger or scenario>

**Usage:**
```bash
<representative command>
```

**Inputs / arguments:**
- `<arg>`: <meaning>

**Outputs:**
- <persistent output and location, if any>
- Transient logs: `temp/...`

**Requirements:**
- <dependency, programmer, runtime, adapter, environment variable, etc.>

**Notes / constraints:**
- <important limitation, compatibility rule, or reason not to create another overlapping tool>
```

## Update rules

- Update an existing entry when extending a tool.
- Add a new entry only for a genuinely new reusable capability.
- Keep the Capability Index synchronized with detailed entries.
- Prefer stable repository-relative paths.
- Keep example commands executable and current.
- Never include secrets. Refer to environment variable names instead.
- Record external utilities too when their invocation is part of the repository workflow, such as a vendor programmer or debugger.
- Register reusable test procedures even when the test implementation itself lives under `tests/`.

## Good capability names

Prefer behavior-oriented names that are easy to search:

- STM32 firmware flashing
- nRF52 recovery and programming
- UART functional test
- GNSS NMEA validation
- RTCM capture and decode
- Serial log collection
- Firmware package generation

Avoid vague names such as `helper`, `misc`, `tool2`, or `debug stuff`.
