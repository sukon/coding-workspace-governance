<!-- BEGIN CODING WORKSPACE GOVERNANCE -->
## Coding workspace governance

- Before creating or invoking reusable developer tooling, tests, flashing, debugging, capture, conversion, or packaging procedures, read `TOOLS.md` and search for an existing capability.
- Reuse or extend existing tooling before creating overlapping helpers.
- Put reusable developer utilities under `tools/`.
- Put test cases, test-only scripts, fixtures, mocks, and test data under `tests/` unless an established repository convention explicitly overrides this.
- Put disposable logs, traces, dumps, generated responses, captures, scratch output, and intermediate artifacts under `temp/`.
- Do not create helper scripts, tests, or temporary files in the repository root.
- When a reusable tool or procedure is added or materially changed, update `TOOLS.md` in the same task with purpose, usage, inputs, outputs, dependencies, and constraints.
- Before finishing, verify workspace placement, remove unnecessary disposable files created by the current task, and ensure `TOOLS.md` is current.
- Never store secrets in `TOOLS.md`; document environment variable names or secret-manager references instead.
<!-- END CODING WORKSPACE GOVERNANCE -->
