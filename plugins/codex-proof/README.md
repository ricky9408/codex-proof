# Codex Proof · portable plugin

Don’t just show me the diff. Show me the bug disappearing.

Independent local coding workflow for Codex. This package contains a portable `plugin.json`, the `prove-bug` skill, and its Python evidence recorder. No API key, remote server, or MCP setup required. The host agent supplies coding and browser tools; this skill guides their use and records real command evidence.

To install, extract the plugin into an authorized repo's `plugins/codex-proof/` and add a repo marketplace entry as described in the [official packaging instructions](https://developers.openai.com/plugins/build/plugins). The companion Codex Proof source ZIP already supplies this marketplace, plus a reproducible sample and evidence. Install and enable via the supported host's local Plugins Directory. This package does not install itself globally.

Prompt: “Use Codex Proof to reproduce this bug, add a regression test, fix it, and show before/after evidence: [report].”

Python 3 is required for the recorder. No dependencies are installed by this package. Read `skills/prove-bug/SKILL.md` for the workflow and commands. Evidence is local, reviewable output; it is not signed attestation or a guarantee of general correctness. Do not share private code or production data. Host discovery, temporary installation/enabling and app-server skill loading were verified with Codex CLI 0.151.0. Model-backed agent invocation was not tested.

Not affiliated with or endorsed by OpenAI. License selection is pending; no license grant is included.
