---
name: prove-bug
description: Reproduce a reported software bug, write a behavior-focused regression test that fails before a fix, implement the smallest fix, and preserve real command output plus comparable browser evidence. Use when the user wants proof that a specific bug disappeared.
---

# Codex Proof

“Don’t just show me the diff. Show me the bug disappearing.”

Work locally in the user's authorized repository. Read its AGENTS.md and scripts first. Never change an unrelated repo, overwrite existing edits, install new dependencies without authorization, upload private evidence, or claim coverage beyond the exercised behavior. This plugin supplies a workflow and recorder; the host agent writes the test and fix using available tools. No API keys or MCP server required.

## Workflow

1. Translate the bug report into a concrete interaction, expected result, actual result, seed data, and environment. Resolve an essential missing detail before guessing. Choose a small deterministic reproduction with existing packages.
2. Preserve the starting revision or a scoped copy of the affected files and record their hashes. Keep all evidence in a new task-specific directory. Never reset the user's checkout to demonstrate a bug.
3. Write a regression test against the expected user-visible behavior. Run it on the preserved before version; inspect the failure to ensure it is the reported assertion failure, not a missing dependency, syntax error, environment failure, or timeout. If it passes, do not label it reproduced: revise the reproduction or report the blocker.
4. For visible bugs, use the user's supported browser tool to follow the exact actions with synthetic/local data. Save a genuine before screenshot and observed DOM values. Record browser, URL, viewport and actions. Stop if navigation or capture is unavailable; report that limitation and continue independent testing.
5. Fix the cause with the smallest reasonable edit. Keep the same test assertions and seed data. Re-run the regression test and relevant adjacent checks. Do not weaken assertions to make a pass.
6. Repeat the exact browser actions at the same viewport and data on the fixed revision. Capture after evidence and assert the observed value. Check console errors. Distinguish a browser assertion from a unit test or screenshot.
7. Package command argv, timestamps, exit codes, unedited stdout/stderr, source hashes, screenshot hashes, the patch, and explicit limits. State what passed and what remains untested. Never fabricate outputs, animate a fake agent session, or say “verified” when only a build passed.

## Recorder

The bundled `scripts/proof.py` uses Python 3's standard library. Run it from the target repo with an explicit argv after `--`. It does not use shell evaluation. The command is still executable code: only run commands appropriate to the authorized task.

```sh
python3 /path/to/skill/scripts/proof.py run --out evidence/issue-123 --phase before --source src/cart.js -- node --test tests/cart.test.js
# Implement fix, then repeat with --phase after and the same regression assertions.
python3 /path/to/skill/scripts/proof.py report --out evidence/issue-123 --bug 'Cart loses remaining total after removal' --limits 'One deterministic flow; no payment/backend coverage.' --artifact before.png --artifact after.png
```

The recorder returns the actual command exit code. A before failure is expected only after you inspect it. Its report observes a fail/pass pair; it cannot decide whether assertions are meaningful. Review raw logs. Timeout or executable launch errors are never a valid reproduction.

## Final handoff

Lead with the behavior change, regression result and browser observations. Link the test, patch and evidence. Include environment and limitations. If a phase is blocked, say which one and do not imply completion. Keep sensitive source, data, cookies and credentials out of shareable output. Ask before publishing, posting, or installing into global configuration.
